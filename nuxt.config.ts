// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  // Enable SSG (Static Site Generation)
  ssr: true,

  modules: [
    '@nuxt/content',
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/hints',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxtjs/i18n',
    '@nuxtjs/sitemap',
    'nuxt-site-config'
  ],

  // Vuetify configuration
  css: ['vuetify/styles', '@mdi/font/css/materialdesignicons.css'],

  build: {
    transpile: ['vuetify']
  },

  // i18n configuration
  i18n: {
    locales: [
      { code: 'en', iso: 'en-US', name: 'English', file: 'en.json' },
      { code: 'fr', iso: 'fr-FR', name: 'Français', file: 'fr.json' },
      { code: 'es', iso: 'es-ES', name: 'Español', file: 'es.json' },
      { code: 'de', iso: 'de-DE', name: 'Deutsch', file: 'de.json' }
    ],
    defaultLocale: 'en',
    strategy: 'prefix_except_default',
    lazy: true,
    langDir: 'locales/',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root'
    }
  },

  // Content configuration
  content: {
    documentDriven: false,
    markdown: {
      anchorLinks: false
    },
    locales: ['en', 'fr', 'es', 'de'],
    defaultLocale: 'en'
  },

  // Site configuration
  site: {
    url: 'https://thesocioscope.org',
    name: 'The Socioscope',
    description: 'Seeing How Societies Transform',
    defaultLocale: 'en'
  },

  // Sitemap configuration
  sitemap: {
    xsl: false
  },

  // App configuration
  app: {
    head: {
      htmlAttrs: {
        lang: 'en'
      },
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'The Socioscope',
      meta: [
        { name: 'description', content: 'Seeing How Societies Transform' },
        { name: 'format-detection', content: 'telephone=no' }
      ],
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
    },
    pageTransition: { name: 'page', mode: 'out-in' }
  },

  // TypeScript configuration
  typescript: {
    strict: false,
    typeCheck: false
  }
})
