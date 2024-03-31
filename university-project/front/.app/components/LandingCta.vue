<script setup lang="ts">
const {t} = useI18n({useScope: "local"})
const {locale, locales} = useI18n()
const config = useRuntimeConfig()

</script>

<template>
  <div class="dark:bg-muted-900 bg-white py-24" :dir="locale === 'en' ? 'ltr' : 'rtl'">
    <div class="mx-auto w-full max-w-7xl px-4">
      <div class="mx-auto w-full max-w-6xl">
        <div
          class="bg-primary-900 dark:bg-primary-900/40 ltablet:grid ltablet:grid-cols-2 ltablet:gap-4 overflow-hidden rounded-3xl shadow-xl lg:grid lg:grid-cols-2 lg:gap-4"
        >
          <div
            class="ltablet:py-28 ltablet:pr-0 flex items-center px-6 pb-12 pt-10 sm:px-16 sm:pt-16 lg:py-28 lg:pr-0 xl:px-20"
          >
            <div class="ltablet:self-center font-sans lg:self-center">
              <h2 class="text-3xl font-medium text-white sm:text-4xl">

                <span class="block">{{ t("GPT-4-Powered Chatbot") }}</span>
                <!--                <span class="block">Explore all available components.</span>-->
              </h2>
              <p class="mt-4 text-lg leading-6 text-white">
                {{ t("ExperienceFutureAI") }}
              </p>
              <div class="mt-8 flex items-center gap-2">
                <NuxtLink :to="config.public.GPT_SERVER_URL">
                  <BaseButton

                    rounded="lg"
                    class="!h-11"
                  >
                    {{ t("Chat") }}
                  </BaseButton>
                </NuxtLink>

              </div>
            </div>
          </div>
          <!--          <div class="aspect-w-5 aspect-h-3 md:aspect-w-2 md:aspect-h-1 -mt-6">-->
          <!--            <NuxtImg-->
          <!--              class="ltablet:translate-y-20 translate-x-6 translate-y-6 rounded-md object-cover object-left-top sm:translate-x-16 lg:translate-y-20"-->
          <!--              src="/img/chatgptscreen.png"-->
          <!--              alt="Tairo demo screenshot lightmode"-->
          <!--              format="webp"-->
          <!--            loading="lazy"-->
          <!--            decoding="async"-->
          <!--            />-->
          <!--            -->
          <!--          </div>-->
          <div class="aspect-w-5 aspect-h-3 md:aspect-w-2 md:aspect-h-1 -mt-6">
            <NuxtImg
              :class="locale === 'en' ? 'ltablet:translate-y-20 translate-x-6 translate-y-6 rounded-md object-cover object-left-top sm:translate-x-16 lg:translate-y-20' :
              'ltablet:translate-y-20 -translate-x-6 translate-y-6 rounded-md object-cover object-right-top sm:-translate-x-16 lg:translate-y-20'"
              :src="locale ==='en' ? '/img/chatgptscreen.png' : '/img/chatgptscreen - rtl.png' "
              alt="Tairo demo screenshot lightmode"
              format="webp"
              loading="lazy"
              decoding="async"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
