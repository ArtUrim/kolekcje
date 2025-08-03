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
      locale: {
        locale: 'pl',
        fallback: 'en',
        messages: {
          pl: {
            $vuetify: {
              input: {
                clear: 'wyczyść'
              },
              dataFooter: {
                pageText: '{0}-{1} z {2}',
                itemsPerPageText: 'Wierszy na stronie:',
                itemsPerPageAll: 'Wszystkie',
                nextPage: 'Następna strona',
                prevPage: 'Poprzednia strona'
              }
            }
          },
          en: {
            $vuetify: {
              input: {
                clear: 'clear'
              },
              dataFooter: {
                pageText: '{0}-{1} of {2}',
                itemsPerPageText: 'Rows per page:',
                itemsPerPageAll: 'All',
                nextPage: 'Next page',
                prevPage: 'Previous page'
              }
            }
          }
        }
      }
    }
  },

  i18n: {
	  defaultLocale: 'pl',
    fallbackLocale: 'en',
	  locales: [
		  { code: 'en', name: 'English', file: 'en.json' },
		  { code: 'pl', name: 'Polski', file: 'pl.json' },
		  { code: 'it', name: 'Italiano', file: 'it.json' }
	  ],
	  // lazy: true,
    langDir: 'i18n/locales/',
    strategy: 'prefix_and_default',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root'
    }
  },

  // Build Configuration
  build: {
    transpile: [
      // Add any packages that need transpilation
    ]
  },

  modules: ['vuetify-nuxt-module', '@nuxtjs/i18n']
})
