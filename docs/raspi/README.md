# Installation & Integration Guide: moode.audio + Kolekcje

This comprehensive guide describes how to configure your Raspberry Pi running **moode.audio** to also serve the **kolekcje** web application (`[gitlab.com/ArtUrim/kolekcje](https://gitlab.com/ArtUrim/kolekcje)`).

This setup integrates the **kolekcje** frontend directly into moode.audio's built-in **Nginx** server, runs the backend services containerized, and configures a smart-shutdown daemon.

---

## Architecture Overview

* **Frontend:** Served as pre-rendered static files by moode.audio's host **Nginx** from `/kolekcje/front`.
* **Backend & DB:** The database and connector run inside containerized environments (Docker/Podman).
* **System Controls:** A **smart-shutdown** system daemon is enabled on the host to manage clean power-offs.

---

## Step 1: Prepare the Frontend (Nuxt Prerender)

Before moving files to the Raspberry Pi, you need to generate the static files of the **kolekcje** frontend.

1. Navigate to your frontend source directory on your local machine:
```bash
cd /path/to/kolekcje/frontend

```


2. Build and pre-render the static files:
```bash
npx nuxt build --prerender

```


*Note: This command generates static assets inside the local `.output/public` (or `dist`) directory.*
3. Transfer these files to your Raspberry Pi:
```bash
# Create the target directory on your Raspberry Pi
ssh ${USER}@moode.lan "sudo mkdir -p /kolekcje/front && sudo chown -R ${USER}:${USER} /kolekcje"

# Sync the prerendered files to the target folder
rsync -avz .output/public/ ${USER}@moode.lan:/kolekcje/front/

```



---

## Step 2: Configure Built-in Nginx

Rather than deploying a containerized reverse-proxy, we configure moode.audio's native Nginx instance to serve **kolekcje** alongside its own web UI.

1. SSH into your Raspberry Pi:
```bash
ssh ${USER}@moode.lan

```


2. Modify file `/etc/nginx/nginx.conf`
```diff
diff -r New/etc/nginx/nginx.conf Old/etc/nginx/nginx.conf
33,34c33,34
< 	# access_log off;
< 	access_log /var/log/nginx/access.log;
---
> 	access_log off;
> 	#access_log /var/log/nginx/access.log;
```
This change is required for the *Step 4: Enable Smart-Shutdown Service* - the activity on
the webpages is watched by new entries in the **nginx** logs.

3. Modify configuration of the **moode** service in the **nginx** - grab only traffic for a
   specific host (*moode.lan* or *moode.local*).
```diff
diff -r New/etc/nginx/sites-available/moode-http.conf Old/etc/nginx/sites-available/moode-http.conf
7c7
< 	server_name moode.lan moode.local;
---
> 	server_name _; # Matches any hostname
```

**Note**: This change would be effective only when the local *DNS* server (on a router or
*pi.hole*) get the speficic rules for the pair of **FQDN**s: *moode.lan* and
*kolekcje.lan* (or the *local* ones).

4. Creatre a configuration for new *sub*service **kolekcje**. For that copy these two files
`nginx/etc/nginx/kolekcje-locations.conf` and `nginx/etc/nginx/sites-available/kolekcje-http.conf`.

5. Enable the configuration and test Nginx:
```bash
# Enable site
sudo ln -sf /etc/nginx/sites-available/kolekcje /etc/nginx/sites-enabled/

# Verify syntax
sudo nginx -t

# Reload Nginx to apply changes
sudo systemctl reload nginx

```



---

## Step 3: Run Connector & DB from Containerized Environment

Prepare the containerized backend services using Docker/Podman on the Raspberry Pi.

1. Ensure Docker and Docker Compose are installed, following the
[instruction](https://docs.docker.com/engine/install/debian/).


2. Create a deployment directory.  Example:
```bash
mkdir -p ~/kolekcje
cd ~/kolekcje

```

3. Copy a `kolekcje/compose-moode.yml` file to newlyy created directory

4. Start the services:
```bash
docker compose -f compose-moode up -d

```

### DB backup

Good practises recommend to make a DB backup periodically. The command for that in our
environment

```bash
docker exec mariadb mariadb-dump -u example -p'example' katalog > dbKolekcjeBck_$(date +"%d%m%Y_%H:%M").sql
```

---

## Step 4: Enable Smart-Shutdown Service

To ensure safe system cut-offs, configure and enable the **smart-shutdown** daemon on the host.

1. Paste the following configuration template (adjust the path to your execution script).
The template is in`systemctl/smart-shutdown.service`. Copy it to `/etc/systemctl/system`
directory

2. Copy the python script `systemctl/smart-shutdown.py` (check the configration for the
   Tasmota smart socket)

Add executable permissions to the script:
```bash
sudo chmod +x /usr/local/bin/smart-shutdown.py

```


3. Enable and start the systemd service:
```bash
sudo systemctl enable smart-shutdown.service
sudo systemctl daemon-reload
sudo systemctl start smart-shutdown.service

```



---

## Verification

To verify that your deployment was successful:

* Navigate to `[http://moode.lan](http://moode.lan)` (or your Raspberry Pi IP) to verify moode.audio is operating normally.
* Navigate to `[http://kolekcje.lan](http://kolekcje.lan)` to verify that your static Nuxt frontend is rendering and communicating with the backend container correctly.
