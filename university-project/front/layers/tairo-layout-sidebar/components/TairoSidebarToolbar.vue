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
      <!--      <slot name="title">{{ route.meta.title }}</slot>-->
      <!--      <slot name="title">Uuniversity Project</slot>-->
      <NuxtLink :to="localPath('/')" class="text-muted-800 dark:text-white flex items-center">
        <template>
          <span class="text-muted-800 dark:text-white hidden md:flex items-center">DASHBOARD</span>
          <!--    <img-->
          <!--      :src="'/img/accountract.png'"-->
          <!--      alt="GPT Logo"-->
          <!--      class="md:h-8 md:w-8 md:mb-1 sm:h-11 sm:w-12 h-11 w-12 sm:block hidden" &lt;!&ndash; Added classes to control visibility &ndash;&gt;-->
          <!--    />-->
        </template>
        <!--  <template v-else>-->
        <!--    <img-->
        <!--      :src="'/img/accountract.png'"-->
        <!--      alt="GPT Logo"-->
        <!--      class="md:h-8 md:w-8 md:mb-1 sm:h-11 sm:w-12 h-11 w-12 sm:block hidden ms-3" &lt;!&ndash; Added classes to control visibility &ndash;&gt;-->
        <!--    />-->
        <!--    <span class="text-muted-800 dark:text-white hidden md:flex items-center">ccountract</span>-->
        <!--  </template>-->
      </NuxtLink>


    </BaseHeading>


    <div class="ms-auto"></div>
    <TairoSidebarTools class="h-16"/>

  </div>
</template>
