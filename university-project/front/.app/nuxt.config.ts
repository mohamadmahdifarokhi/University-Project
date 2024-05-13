import {
  demoRules,
  documentationRules,
  landingRules,
} from './config/routes-rules'

export default defineNuxtConfig({
  extends: [
    /**
     * App layers: these are the layers that contains specific features
     * - landing: contains landing pages
     * - documentation: contains all /documentation pages
     */
    '../layers/landing',
    import.meta.env.ENABLE_DOCUMENTATION && '../layers/documentation',

    /**
     * This extends the base Tairo layer.
     *
     * Alternatively you can use the following:
     * ["gh:cssninjaStudio/tairo/layers/tairo#v1.4.0", {
     *    install: true,
     *    giget: { auth: import.meta.env.GITHUB_TOKEN },
     * }]
     *
     * @see https://github.com/unjs/c12#extending-config-layer-from-remote-sources
     *
     * This would allows you to create an empty git repository
     * with only your source code and no demo.
     */
    '../layers/tairo-layout-sidebar',
    '../layers/tairo-layout-collapse',
    '../layers/tairo-layout-topnav',
    '../layers/tairo',
    '@shuriken-ui/nuxt'
  ],

  modules: [
    /**
     * Swiper is a nuxt module that allows us to use swiper in nuxt
     * wich is a carousel component used in the demo
     * @see https://github.com/cpreston321/nuxt-swiper
     */
    'nuxt-swiper',
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    '@formkit/nuxt',
    '@nuxtjs/i18n',
    '@nuxt/image'
  ],

  css: [
    '~/assets/css/colors.css',
    '@fontsource-variable/fira-code/index.css',
    '@fontsource-variable/inter/index.css',
    '@fontsource-variable/karla/index.css',
    // '~/assets/style.css'
  ],

  app: {
    pageTransition: {
      mode: 'out-in',
      enterActiveClass: 'transition-opacity duration-200 ease-out',
      enterFromClass: 'opacity-0',
      enterToClass: 'opacity-100',
      leaveActiveClass: 'transition-opacity duration-75 ease-in',
      leaveFromClass: 'opacity-100',
      leaveToClass: 'opacity-0',
    },
    layoutTransition: {
      mode: 'out-in',
      enterActiveClass: 'transition-opacity duration-200 ease-out',
      enterFromClass: 'opacity-0',
      enterToClass: 'opacity-100',
      leaveActiveClass: 'transition-opacity duration-200 ease-in',
      leaveFromClass: 'opacity-100',
      leaveToClass: 'opacity-0',
    },
  },

  experimental: {
    // Write early hints when using node server.
    writeEarlyHints: false
    // // Render JSON payloads with support for revivifying complex types.
    // renderJsonPayloads: true,
    // // Render tags in of the head in a more performant way
    // headNext: true,
    // defaults: {
    //   useAsyncData: {
    //     // Use shallowRef in asyncData/fetch data
    //     deep: false,
    //   },
    // },
  },

  typescript: {
    tsConfig: {
      // Here you can customize the generated tsconfig.json file
    },
  },

  // nuxt behavior configuration
  runtimeConfig: {
    public: {
      GPT_SERVER_URL: process.env.VITE_GPT_SERVER_URL,
    },
  },

  routeRules: {
    ...demoRules,
    ...landingRules,
    ...(import.meta.env.ENABLE_DOCUMENTATION ? documentationRules : {}),
  },

  // nuxt build configuration
  nitro: {
    esbuild: {
      options: {
        target: 'esnext',
      },
    },
  },

  vite: {
    define: {
      // This enables vue-axe to work (used to check a11y - see .demo/plugins/vue-axe.ts)
      'import.meta.env.ENABLE_A11Y_AXE': import.meta.env.ENABLE_A11Y_AXE,
    },
    build: {
      target: 'esnext',
    },
    // Defining the optimizeDeps.include option prebuilds the dependencies, this avoid
    // some reloads when navigating between pages during development.
    // It's also useful to track them usage.
    optimizeDeps: {
      include: [
        '@vueform/slider',
        'v-calendar',
        // AddonCarouselIcon
        // AddonCarouselTeam
        'vue3-carousel',
        // AddonApexcharts
        'vue3-apexcharts',
        // AddonInputPhone
        'libphonenumber-js/max',
        'country-codes-list',
        // AddonInputPassword
        '@zxcvbn-ts/core',
        '@zxcvbn-ts/language-common',
        '@zxcvbn-ts/language-en',
        '@zxcvbn-ts/language-fr',
        // AddonMarkdownRemark
        'rehype-external-links',
        'rehype-raw',
        'rehype-sanitize',
        'rehype-stringify',
        'rehype-shikiji',
        'remark-gfm',
        'remark-parse',
        'remark-rehype',
        'unified',
        // useMultiStepForm
        'fast-copy',
        'vue3-smooth-dnd',
        'splitpanes',
        'mapbox-gl',
        '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.min.js',
        // DocComponentMeta
        // useDocumentationMeta
        'scule',
        // form validation
        '@vee-validate/zod',
        'vee-validate',
        'zod',
        // calendar app
        'date-fns',
        // profile edit page
        'imask',
      ],
    },
  },

  i18n: {
    locales: [
      {code: 'en', iso: 'en-US', dir: 'ltr', name: 'English'},
    ],
    defaultLocale: 'en',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root',
    },
  },

})
