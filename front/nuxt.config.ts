// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  runtimeConfig: {
    public: {
      apiBase: 'http://connector:3000'
    }
  },

  // Global CSS
  css: [
    '@/assets/styles/main.css'
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
