export const useNetworkAdmin = () => {
  const userRole = useState<string>('user-role', () => {
    if (import.meta.server) {
      const headers = useRequestHeaders(['x-app-role'])
      return headers['x-app-role'] || 'standard'
    }
    return 'standard'
  })

  const triggerRestart = async (): Promise<void> => {
    try {
      const res = await fetch('/api/restart-router', { method: 'POST' })
      const data = await res.json()
      if (res.ok) {
        alert(`Success: ${data.message}`)
      } else {
        alert(`Failed: ${data.error}`)
      }
    } catch (err) {
      alert(`Restart Request Failed: ${(err as Error).message}`)
    }
  }

  // Expose state and functions to Vue components
  return {
    userRole,
    triggerRestart,
  }
}
