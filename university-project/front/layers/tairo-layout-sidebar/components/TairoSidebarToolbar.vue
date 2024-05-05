<script setup lang="ts">
import {useSidebar} from '../composables/sidebar'

const localPath = useLocalePath();
const {locale, locales} = useI18n()

const props = withDefaults(
  defineProps<{
    sidebar?: boolean
    horizontalScroll?: boolean
  }>(),
  {
    sidebar: true,
  },
)

const app = useAppConfig()
const {hasSubsidebar} = useSidebar()

const route = useRoute()

const showNavBurger = computed(() => {
  return (
    props.sidebar &&
    app.tairo.sidebar?.toolbar?.showNavBurger &&
    hasSubsidebar.value
  )
})
</script>

<template>
  <div
    class="relative z-50 mb-5 flex h-16 items-center gap-2"
    :class="props.horizontalScroll && 'pe-4 xl:pe-10'"
  >
    <TairoSidebarBurger v-if="showNavBurger" class="-ms-3"/>

    <BaseHeading
      v-if="app.tairo.sidebar?.toolbar?.showTitle"
      as="h1"
      size="2xl"
      weight="light"
      class="text-muted-800 dark:text-white"
    >
      <NuxtLink to="/dashboard" class="text-muted-800 dark:text-white flex items-center">
          <span class="text-muted-800 dark:text-white items-center">DASHBOARD</span>
      </NuxtLink>


    </BaseHeading>


    <div class="ms-auto"></div>
    <TairoSidebarTools class="h-16"/>

  </div>
</template>
