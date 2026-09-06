// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',

    css: [
        '~/assets/main.css',
        'lenis/dist/lenis.css',
    ],

    runtimeConfig: {
        public: {
            apiBase:
                process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
            siteUrl:
                process.env.NUXT_PUBLIC_SITE_URL || 'https://dabro-sun.ru',
        },
    },


    app: {
        head: {
            htmlAttrs: {lang: 'ru'},
            meta: [{name: 'viewport', content: 'width=device-width, initial-scale=1'},],
        },
    },

    modules: [
        '@ant-design-vue/nuxt',
        '@pinia/nuxt',
        'pinia-plugin-persistedstate/nuxt',
    ],
})
