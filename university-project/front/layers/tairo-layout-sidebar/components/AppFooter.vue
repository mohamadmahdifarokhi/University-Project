<script setup lang="ts">
const year = new Date().getFullYear()
const localPath = useLocalePath();
const {t} = useI18n({useScope: "local"})

</script>

<template>
  <footer
    class="bg-muted-100 dark:bg-muted-900 border-muted-200 dark:border-muted-700 relative border-t"
  >
<!--    <NuxtLink-->
<!--      :to="localPath(`/`)"-->
<!--      class="bg-muted-100 dark:bg-muted-900 absolute inset-x-0 -top-4 mx-auto flex h-9 w-14 items-center justify-center"-->
<!--    >-->
<!--      <img-->
<!--        class="size-7"-->
<!--        src="/img/accountract.png"-->
<!--        alt="Uuniversity Project Logo"-->
<!--        height="28"-->
<!--        width="28"-->
<!--        loading="lazy"-->
<!--        decoding="async"-->
<!--      >-->

<!--    </NuxtLink>-->
    <div
      class="ltablet:flex-row mx-auto flex max-w-7xl flex-col items-center justify-between px-6 py-8"
    >
      <NuxtLink
        to="/"
        aria-label="Go to Tairo homepage"
        class="ltablet:w-1/5 block w-full lg:w-1/5"
      >
        <!-- <TairoLogoText
          class="text-muted-300 ltablet:mx-0 mx-auto h-6 transition-all duration-200 lg:mx-0"
        /> -->

      </NuxtLink>


<!--      <div-->
<!--        class="ltablet:mt-0 ltablet:gap-6 mt-6 flex flex-wrap items-center justify-center gap-4 lg:mt-0 lg:gap-6"-->
<!--      >-->
<!--        <NuxtLink-->
<!--          to="https://t.me/accountract"-->
<!--          class="text-muted-600 hover:text-primary-500 dark:text-muted-200 dark:hover:text-primary-400 text-sm transition-colors duration-300"-->
<!--        >-->
<!--          <Icon name="ri:telegram-fill" class="size-6"/>-->
<!--        </NuxtLink>-->

<!--        <NuxtLink-->
<!--          :data-nui-tooltip="t('Soon')"-->
<!--          class="text-muted-600 hover:text-primary-500 dark:text-muted-200 dark:hover:text-primary-400 text-sm transition-colors duration-300"-->
<!--        >-->
<!--          &lt;!&ndash;          Documentation&ndash;&gt;-->
<!--          <Icon name="ri:instagram-fill" class="size-6"/>-->

<!--        </NuxtLink>-->
<!--        <NuxtLink-->
<!--          :data-nui-tooltip="t('Soon')"-->
<!--          class="text-muted-600 hover:text-primary-500 dark:text-muted-200 dark:hover:text-primary-400 text-sm transition-colors duration-300"-->
<!--        >-->
<!--          <Icon name="ri:twitter-fill" class="size-6"/>-->
<!--        </NuxtLink>-->
<!--        &lt;!&ndash;        <NuxtLink&ndash;&gt;-->
<!--        &lt;!&ndash;          to="https://cssninja.io/faq/support"&ndash;&gt;-->
<!--        &lt;!&ndash;          target="_blank"&ndash;&gt;-->
<!--        &lt;!&ndash;          rel="noopener"&ndash;&gt;-->
<!--        &lt;!&ndash;          class="text-muted-600 hover:text-primary-500 dark:text-muted-200 dark:hover:text-primary-400 text-sm transition-colors duration-300"&ndash;&gt;-->
<!--        &lt;!&ndash;        >&ndash;&gt;-->
<!--        &lt;!&ndash;          Support&ndash;&gt;-->
<!--        &lt;!&ndash;        </NuxtLink>&ndash;&gt;-->
<!--      </div>-->
      <div
        class="text-muted-500 dark:text-muted-400 ltablet:w-1/5 ltablet:mt-0 mt-6 flex w-full items-center justify-center text-sm"
      >
        <span dir="ltr">
                    © Uuniversity Project {{ year }}
        </span>
      </div>
    </div>
  </footer>
</template>
