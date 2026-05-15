export function useAPI<T>(
  url: string,
  options?: Parameters<typeof $fetch>[1],
) {
  const api = useNuxtApp().$api as typeof $fetch
  return api<T>(url, options)
}
