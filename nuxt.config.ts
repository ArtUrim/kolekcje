// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  // Global CSS
  css: [
    '@/assets/styles/main.css'
  ],

  // Other configurations...
  modules: [
    // Add any required modules
  ],

  // Build Configuration
  build: {
    transpile: [
      // Add any packages that need transpilation
    ]
  }
})
