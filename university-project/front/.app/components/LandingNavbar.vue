<script setup lang="ts">
const {x, y} = useWindowScroll()
const isSearchOpen = useState('search-open', () => false)
const isMobileOpen = ref(false)

const metaKey = useMetaKey()
const {open} = usePanels()
const localPath = useLocalePath();
const {t} = useI18n({useScope: "local"})
const app = useAppConfig()
const {locale, locales} = useI18n()
const config = useRuntimeConfig()

</script>

<template>
  <div
    class="group/nav ltablet:max-w-[1000px] ptablet:max-w-[47rem] fixed inset-x-0 top-0 z-50 mx-auto max-w-[350px] group-[&.scrolled]/landing:mt-2 group-[&:not(.scrolled)]/landing:mt-4 motion-safe:transition-all motion-safe:duration-200 lg:max-w-7xl"
    :dir="locale === 'en' ? 'ltr' : 'rtl'"
  >
    <div
      class="group-[&.scrolled]/landing:dark:bg-muted-950/95 group-[&.scrolled]/landing:border-muted-200 group-[&.scrolled]/landing:dark:border-muted-700 group-[&.scrolled]/landing:motion-safe:shadow-muted-300/30 group-[&.scrolled]/landing:motion-safe:dark:shadow-muted-800/20 flex items-center justify-between rounded-2xl border p-4 group-[&:not(.scrolled)]/landing:border-transparent group-[&.scrolled]/landing:bg-white/95 motion-safe:transition-all motion-safe:duration-200 group-[&.scrolled]/landing:motion-safe:shadow-xl"
    >
      <div class="flex w-1/2 items-center gap-2 md:w-1/5">
        <NuxtLink
          :to="localPath('/')"
          class="ms-2 inline-flex"
          aria-label="Go to Tairo homepage"
        >
          <!--          <TairoLogoText-->
          <!--            class="text-primary-500 group-[&.scrolled]/landing:h-6 group-[&:not(.scrolled)]/landing:h-7 motion-safe:transition-all motion-safe:duration-200"-->
          <!--          />-->
          <template>
            <span class="text-muted-800 dark:text-white hidden md:flex items-center">DASHBOARD</span>
<!--            <img-->
<!--              :src="'/img/accountract.png'"-->
<!--              alt="GPT Logo"-->
<!--              class="md:h-8 md:w-8 md:mb-1 sm:h-11 sm:w-12 h-11 w-12"-->
<!--            &lt;!&ndash; Added classes to control visibility &ndash;&gt;-->
<!--            />-->
          </template>
<!--          <template v-else>-->
<!--            <img-->
<!--              :src="'/img/accountract.png'"-->
<!--              alt="GPT Logo"-->
<!--              class="md:h-8 md:w-8 md:mb-1 sm:h-11 sm:w-12 h-11 w-12"-->
<!--            &lt;!&ndash; Added classes to control visibility &ndash;&gt;-->
<!--            />-->
<!--            <span class="text-muted-800 dark:text-white hidden md:flex items-center">ccountract</span>-->
<!--          </template>-->

        </NuxtLink>
      </div>
      <div
        class="ltablet:static ltablet:w-auto ltablet:flex ltablet:flex-row dark:bg-muted-950 ltablet:!bg-transparent ltablet:mx-0 fixed inset-x-0 top-20 mx-auto w-[calc(100%_-_2rem)] items-center justify-center bg-white lg:static lg:mx-0 lg:flex lg:w-auto lg:flex-row lg:!bg-transparent"
        :class="[
          isMobileOpen
            ? 'shadow-muted-300/30 dark:shadow-muted-900/20 group-[&.scrolled]/landing:ltablet:mt-0 group-[&:not(.scrolled)]/landing:ltablet:mt-0 flex flex-col space-y-4 rounded-xl p-6 shadow-xl group-[&.scrolled]/landing:mt-2 group-[&:not(.scrolled)]/landing:mt-4 motion-safe:transition-all motion-safe:duration-200 group-[&.scrolled]/landing:lg:mt-0 group-[&:not(.scrolled)]/landing:lg:mt-0'
            : 'hidden',
        ]"
      >
        <NuxtLink
          :to="localPath('/')"
          class="inline-flex items-center justify-center px-6"
        >
          {{ t("Shop") }}
        </NuxtLink>
        <NuxtLink
          class="inline-flex items-center justify-center px-6"
          :to="config.public.GPT_SERVER_URL"
        >
          {{ t("Chat") }}
        </NuxtLink>
        <!--        <div class="px-6">-->
        <!--          <button-->
        <!--            type="button"-->
        <!--            class="group-[&.scrolled]/landing:bg-muted-100 group-[&.scrolled]/landing:dark:bg-muted-900 group-[&.scrolled]/landing:border-muted-100 group-[&.scrolled]/landing:dark:border-muted-800 group-[&.scrolled]/landing:text-muted-400 group-[&.scrolled]/landing:dark:text-muted-500 group-[&.scrolled]/landing:hover:text-primary-500 group-[&.scrolled]/landing:dark:hover:text-primary-500 group-[&:not(.scrolled)]/landing:text-muted-800 group-[&:not(.scrolled)]/landing:dark:text-muted-200 group flex items-center gap-2 rounded-xl py-1 pe-1 ps-3 group-[&.scrolled]/landing:border"-->
        <!--            aria-label="Open search"-->
        <!--            @click="isSearchOpen = true"-->
        <!--          >-->
        <!--            <Icon-->
        <!--              name="lucide:search"-->
        <!--              class="size-4 motion-safe:transition-colors motion-safe:duration-300"-->
        <!--            />-->
        <!--            <span-->
        <!--              class="group-[&.scrolled]/landing:dark:bg-muted-800 group-[&.scrolled]/landing:border-muted-200 group-[&.scrolled]/landing:dark:border-muted-700 group-[&.scrolled]/landing:group-hover:text-muted-600 group-[&.scrolled]/landing:dark:group-hover:text-muted-100 rounded-lg border px-2 py-0.5 group-[&:not(.scrolled)]/landing:border-transparent group-[&.scrolled]/landing:bg-white group-[&.scrolled]/landing:shadow motion-safe:transition-colors motion-safe:duration-300"-->
        <!--            >-->
        <!--              <kbd class="font-sans text-sm tracking-wide">-->
        <!--                {{ metaKey }} + k-->
        <!--              </kbd>-->
        <!--            </span>-->
        <!--          </button>-->
        <!--        </div>-->
      </div>
      <div class="flex gap-4">
        <!--        <button-->
        <!--          type="button"-->
        <!--          class="border-muted-200 hover:ring-muted-200 dark:hover:ring-muted-700 dark:border-muted-700 dark:bg-muted-800 dark:ring-offset-muted-900 flex size-9 items-center justify-center rounded-full border bg-white ring-1 ring-transparent transition-all duration-300 hover:ring-offset-4"-->
        <!--          @click="-->
        <!--            () => {-->
        <!--              const isOpen = useState('switcher-open', () => false)-->
        <!--              isOpen.value = true-->
        <!--            }-->
        <!--          "-->
        <!--        >-->
        <!--          <Icon-->
        <!--            name="ph:drop-half-bottom-duotone"-->
        <!--            class="text-muted-400 size-5"-->
        <!--          />-->
        <!--        </button>-->
        <div class="flex items-center gap-2">
          <template v-for="tool of app.tairo?.sidebar?.toolbar?.landing">
            <component
              :is="resolveComponentOrNative(tool.component)"
              v-if="tool.component"
              :key="tool.component"
              v-bind="tool.props"
            />
          </template>
        </div>
                <BaseThemeToggle aria-label="Toggle darkmode"/>
        <BaseButton
          rounded="lg"
          color="primary"
          :to="localPath('/signup')"
          class="ltablet:!flex !hidden lg:!flex"
        >
          {{ t('Signup') }}
        </BaseButton>
        <BaseButton
          rounded="lg"
          color="primary"
          :to="localPath('/login')"
          class="ltablet:!flex !hidden lg:!flex"
        >
          {{ t('Login') }}
        </BaseButton>
        <button
          type="button"
          class="ltablet:hidden flex items-center justify-center lg:hidden"
          :aria-label="isMobileOpen ? 'Close menu' : 'Open menu'"
          @click="isMobileOpen = !isMobileOpen"
        >
          <div class="space-y-1.5">
            <span
              class="bg-primary-600 block h-0.5 motion-safe:transition-all motion-safe:duration-300"
              :class="isMobileOpen ? 'w-2' : 'w-6'"
            />
            <span
              class="bg-primary-600 block h-0.5 motion-safe:transition-all motion-safe:duration-300"
              :class="isMobileOpen ? 'w-6' : 'w-6'"
            />
            <span
              class="bg-primary-600 block h-0.5 motion-safe:transition-all motion-safe:duration-300"
              :class="isMobileOpen ? 'w-4' : 'w-6'"
            />
          </div>
        </button>
      </div>
    </div>
  </div>
</template>
