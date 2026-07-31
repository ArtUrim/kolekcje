import os
import sys
import time
import subprocess
import select
import argparse
import requests

# --- CONFIGURATION ---
TASMOTA_IP = "192.168.0.225"  # IP address of the Tasmota Nous A1T smart plug
IDLE_LIMIT = 30*60         # HTTP traffic inactivity threshold (seconds)
AUDIO_MEMORY_WINDOW = IDLE_LIMIT
NGINX_LOG = "/var/log/nginx/access.log"
POLL_INTERVAL = 10         # Main loop sleep duration between system checks (seconds)


def check_hardware_audio():
    """Directly queries MPD and the HiFiBerry hardware for active playback.

    Returns:
        bool: True if audio is physically rendering/playing right now, else False.
    """
    try:
        # Method 1: Check MPD status via mpc (Moode's core player backend)
        mpc_status = subprocess.check_output(["mpc", "status"], text=True)
        if "[playing]" in mpc_status:
            return True
    except Exception as e:
        print(f"Error checking mpc status: {e}", file=sys.stderr)

    try:
        # Method 2: Fallback check for HiFiBerry ALSA digital sound interface status.
        status_file = "/proc/asound/card1/pcm0p/sub0/status"
        if os.path.exists(status_file):
            with open(status_file, "r") as f:
                if "RUNNING" in f.read():
                    print( "Check card status" )
                    return True
    except Exception:
        pass

    return False


def evaluate_audio_status(current_time, last_time_audio_heard):
    """Evaluates the state of the audio player against the historical memory window.

    Returns:
        tuple: (bool, str, float) -> (Is active in window?, Status string, Updated anchor timestamp)
    """
    audio_playing_now = check_hardware_audio()

    if audio_playing_now:
        last_time_audio_heard = current_time

    seconds_since_last_audio = current_time - last_time_audio_heard
    audio_is_active_in_window = seconds_since_last_audio < AUDIO_MEMORY_WINDOW

    if audio_playing_now:
        status_str = "PLAYING NOW"
    else:
        status_str = f"IDLE (Stopped {int(seconds_since_last_audio)}s ago)"

    return audio_is_active_in_window, status_str, last_time_audio_heard


def trigger_tasmota_shutdown(test_mode=False):
    """Transmits a delayed shutdown sequence to the Tasmota smart plug.
    
    Attempts to send the command up to 3 times in case of temporary network 
    or Wi-Fi connection issues before finally giving up.
    """
    if test_mode:
        print("[TEST MODE] Skipping Tasmota command: Would send Backlog Delay 300; Power 0")
        return

    url = f"http://{TASMOTA_IP}/cm?cmnd=Backlog%20Delay%20300%3B%20Power%200"
    max_attempts = 3
    retry_delay = 2  # Seconds to wait between retries

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Sending shutdown command to Tasmota (Attempt {attempt}/{max_attempts})...")
            requests.get(url, timeout=5)
            print("Tasmota shutdown command transmitted successfully.")
            return  # Success! Exit the function early.
        except Exception as e:
            print(f"Attempt {attempt} failed to reach Tasmota: {e}", file=sys.stderr)
            if attempt < max_attempts:
                print(f"Retrying in {retry_delay} seconds...", file=sys.stderr)
                time.sleep(retry_delay)
            else:
                print("Error: All 3 attempts to contact Tasmota failed.", file=sys.stderr)


def main():
    # --- ARGUMENT PARSING ---
    parser = argparse.ArgumentParser(
        description="Smart Monitoring and Shutdown script for Moode Audio + Tasmota."
    )
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        help="Run in dry-run test mode. Logs actions without shutting down or contacting Tasmota."
    )
    args = parser.parse_args()

    if args.test:
        print("=" * 60)
        print(" RUNNING IN DRY-RUN TEST MODE — HARDWARE SHUTDOWNS ARE DISABLED")
        print("=" * 60)
    else:
        print("Smart Shutdown script initiated safely (10s polling interval)...")

    # --- INITIALIZE LOG MONITORING ---
    try:
        log_file = open(NGINX_LOG, "r")
        # Jump directly to the end of the file to ignore historical boot traffic data
        log_file.seek(0, os.SEEK_END)
    except FileNotFoundError:
        print(f"Error: Nginx log file not found at {NGINX_LOG}. Exiting.", file=sys.stderr)
        sys.exit(1)

    current_now = time.time()
    last_http_activity = current_now
    last_time_audio_heard = current_now

    # Create a 60-second guard window at boot
    grace_period_end = current_now + 60

    try:
        while True:
            current_time = time.time()

            # --- 1. MONITOR HTTP TRAFFIC ---
            while True:
                ready_to_read, _, _ = select.select([log_file], [], [], 0.5)
                if ready_to_read:
                    line = log_file.readline()
                    if line:
                        last_http_activity = current_time
                        print(f"Nginx HTTP Request detected: {line.strip()[:50]}...")
                    else:
                        break
                else:
                    break

            nginx_idle_time = current_time - last_http_activity

            # --- 2. EVALUATE AUDIO PLAYBACK MEMORY ---
            audio_is_active_in_window, audio_status_str, last_time_audio_heard = evaluate_audio_status(
                current_time, last_time_audio_heard
            )
            # print( f"Current values: {current_time} {last_time_audio_heard}" )

            # Print state analysis on every iteration
            # print(f"Status -> Audio: {audio_status_str} | Window Active: {audio_is_active_in_window} | Nginx Idle: {int(nginx_idle_time)}s")

            # --- 3. EVALUATE SHUTDOWN ENFORCEMENT ---
            if current_time > grace_period_end:
                # print( f"Nginx staff: {IDLE_LIMIT} - {nginx_idle_time}" )
                if not audio_is_active_in_window and nginx_idle_time >= IDLE_LIMIT:
                    print("!" * 70)
                    print(f"CRITICAL: System inactivity threshold met! (10m audio idle + {int(nginx_idle_time)}s HTTP idle)")

                    # Execute Tasmota step (safely self-contained with test check inside)
                    trigger_tasmota_shutdown(test_mode=args.test)

                    if args.test:
                        print("[TEST MODE] Skipping OS hardware command: Would run 'sudo shutdown -h now'")
                        print("Resetting simulated activity clocks to prevent message spamming...")
                        print("!" * 70)
                        # Reset timestamps in test mode so the script loops normally instead of quitting
                        last_http_activity = time.time()
                        last_time_audio_heard = time.time()
                    else:
                        print("Shutting down operating system engine now.")
                        print("!" * 70)
                        os.system("sudo shutdown -h now")
                        break

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nScript stopped manually by user. Closing log file safely.")
    finally:
        log_file.close()


if __name__ == "__main__":
    main()
