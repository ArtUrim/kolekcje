export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',

  ssr: true,

  devtools: {
    enabled: true
  },

  runtimeConfig: {
    public: {
      apiBase: '/api'
    }
  },

  css: [
    '@/assets/styles/main.css'
  ],

  modules: [
    'vuetify-nuxt-module',
    '@nuxtjs/i18n'
  ],

  vuetify: {
    moduleOptions: {},
    vuetifyOptions: {
      locale: {
        locale: 'pl',
        fallback: 'en',
        messages: {
          pl: {
            $vuetify: {
              close: 'zamknij',
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
              close: 'close',
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
      { code: 'pl', name: 'Polski', file: 'pl.json' },
      { code: 'en', name: 'English', file: 'en.json' },
      { code: 'it', name: 'Italiano', file: 'it.json' }
    ],

    langDir: 'locales/',

    strategy: 'prefix_and_default',

    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root'
    }
  },

  nitro: {
    preset: 'static',

    prerender: {
      crawlLinks: true,
      routes: ['/']
    },

    devProxy: {
      '/api': 'http://connector:5000'
    }
  }
})
