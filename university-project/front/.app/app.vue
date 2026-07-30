<script setup lang="ts">
const route = useRoute()
const app = useAppConfig()
const { locale, locales } = useI18n()
const localeInfo = computed(() => locales.value.find((item: any) => item.code === locale.value))

/**
 * Global head configuration
 * @see https://nuxt.com/docs/getting-started/seo-meta
 */
useHead({
  title: () => route.meta?.title ?? '',
  titleTemplate: (titleChunk) => {
    return titleChunk
      // ? `${titleChunk} - ${app.tairo?.title}`
      ? `${titleChunk}`
      : `${app.tairo?.title}`
  },
  htmlAttrs: {
    lang: () => localeInfo.value?.iso || locale.value,
    dir: () => localeInfo.value?.dir || (locale.value === 'fa' ? 'rtl' : 'ltr'),
  },
  link: [
    {
      rel: 'icon',
      type: 'image/png',
      href: '/img/azad-pardis-logo.png',
    },
  ],

  meta: [
    {
      name: 'description',
      content: () =>
        route.meta.description
        ?? 'سامانه دانشگاهی مدیریت تولید، ذخیره و تبادل انرژی',
    },
    {
      name: 'twitter:card',
      content: 'summary_large_image',
    },
    {
      name: 'og:image:type',
      content: 'image/png',
    },
    {
      name: 'og:image:width',
      content: '1200',
    },
    {
      name: 'og:image:height',
      content: '630',
    },
    { name: 'og:image', content: '/img/azad-pardis-logo.png' },
  ],
})
</script>

<template>
  <div>
    <NuxtLayout>
      <NuxtLoadingIndicator color="rgb(var(--color-primary-500))" />
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
