// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  // Global CSS
  css: [
    '@/assets/styles/main.css'
  ],

  // Other configurations...
  buildModules: [
       'vuetify-nuxt-module'
  ],

  vuetify: {
      moduleOptions: {
          /* module specific options */
      },
      vuetifyOptions: {
          /* vuetify options */
      }
  },

  // Build Configuration
  build: {
    transpile: [
      // Add any packages that need transpilation
    ]
  },

  modules: ['vuetify-nuxt-module']
})