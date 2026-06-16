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
    },
    baseUrl: 'https://thesocioscope.org'
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
    defaultLocale: 'en',
    trailingSlash: true
  },

  // Sitemap configuration
  sitemap: {
    xsl: false
  },

  // Fonts configuration - handle network failures gracefully in CI
  fonts: {
    providers: {
      google: {
        experimental: {
          disableLocalFallbacks: false
        }
      }
    },
    defaults: {
      fallbacks: {
        serif: ['Georgia', 'Times New Roman', 'serif'],
        'sans-serif': ['Arial', 'Helvetica', 'sans-serif']
      }
    }
  },

  // Image configuration
  image: {
    baseURL: process.env.NODE_ENV === 'production' ? 'https://thesocioscope.org' : ''
  },

  // Runtime config — feature flags
  runtimeConfig: {
    public: {
      detailV2: true
    }
  },

  // App configuration
  app: {
    baseURL: '/',
    head: {
      htmlAttrs: {
        lang: 'en'
      },
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'The Socioscope',
      meta: [
        { name: 'description', content: 'Seeing How Societies Transform. Explore sustainable food initiatives, access research insights, and learn about transformative projects worldwide.' },
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'theme-color', content: '#1B5E20' },
        { name: 'robots', content: 'index, follow' },
        { name: 'googlebot', content: 'index, follow' },
        { property: 'og:title', content: 'The Socioscope' },
        { property: 'og:description', content: 'Seeing How Societies Transform. Explore sustainable food initiatives, access research insights, and learn about transformative projects worldwide.' },
        { property: 'og:type', content: 'website' },
        { property: 'og:url', content: 'https://thesocioscope.org' },
        { property: 'og:image', content: 'https://thesocioscope.org/og-image.png' },
        { property: 'og:image:width', content: '1200' },
        { property: 'og:image:height', content: '630' },
        { property: 'og:locale', content: 'en_US' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'The Socioscope' },
        { name: 'twitter:description', content: 'Seeing How Societies Transform. Explore sustainable food initiatives, access research insights, and learn about transformative projects worldwide.' },
        { name: 'twitter:image', content: 'https://thesocioscope.org/og-image.png' }
      ],
      link: [
        {
          rel: 'icon',
          type: 'image/x-icon',
          href: '/favicon.ico'
        },
        // Google Fonts — Lato + Playfair Display.
        // Direct link because @nuxt/fonts' Google provider currently throws
        // "provider.resolveFontFaces is not a function" in this version.
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Lato:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap'
        }
      ]
    },
    pageTransition: { name: 'page', mode: 'out-in' }
  },

  // Prerender concurrency — limits simultaneous page renders to avoid OOM
  // when each project page loads the full 14MB projects collection
  nitro: {
    prerender: {
      concurrency: 10,
      interval: 50
    },
    watchOptions: {
      ignored: ['**/public/data/**']
    }
  },

  watch: ['!public/data/**'],

  vite: {
    server: {
      watch: {
        ignored: ['**/public/data/**']
      }
    }
  },

  // TypeScript configuration
  typescript: {
    strict: false,
    typeCheck: false
  }
})
