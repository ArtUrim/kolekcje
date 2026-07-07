// composables/useHeartbeat.ts
export const useHeartbeat = () => {
  let timer: ReturnType<typeof setInterval> | null = null

  const startHeartbeat = () => {
    // Prevent multiple intervals from running simultaneously
    if (timer) return 

    // 5 minutes in milliseconds (5 * 60 * 1000)
    const FIVE_MINUTES = 300000 

    timer = setInterval(async () => {
      try {
        // Replace with your actual backend endpoint
        await $fetch('/api/keepalive', {
          method: 'POST',
          // Optional: Send session info if your backend requires it
          body: { timestamp: Date.now() } 
        })
        console.log('Heartbeat sent successfully.')
      } catch (error) {
        console.error('Failed to send heartbeat:', error)
      }
    }, FIVE_MINUTES)
  }

  const stopHeartbeat = () => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  // Clean up when the component using this composable unmounts
  onBeforeUnmount(() => {
    stopHeartbeat()
  })

  return {
    startHeartbeat,
    stopHeartbeat
  }
}
