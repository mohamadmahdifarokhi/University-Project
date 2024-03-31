<script setup lang="ts">
const {locale, locales} = useI18n()
const {t} = useI18n({useScope: "local"})

</script>


<template>
  <div class="dark:bg-muted-900 bg-white py-24" :dir="locale === 'en' ? 'ltr' : 'rtl'">
    <div class="mx-auto w-full max-w-7xl px-4">
      <div class="mb-10 max-w-2xl">
        <!--        <BaseText-->
        <!--          class="text-primary-500 mb-2 text-[0.65rem] uppercase tracking-wider"-->
        <!--        >-->
        <!--          We back you up-->
        <!--        </BaseText>-->
        <BaseHeading
          as="h2"
          size="4xl"
          weight="light"
          lead="tight"
          class="text-muted-800 mx-auto mb-4 dark:text-white"
        >
          {{ t("Developers") }}
        </BaseHeading>
        <BaseParagraph
          size="lg"
          class="text-muted-500 dark:text-muted-100 mx-auto mb-4"
        >
          {{ t("Introduction.paragraph") }}


        </BaseParagraph>
      </div>
      <div class="ptablet:grid-cols-2 grid gap-6 sm:grid-cols-3">
        <LandingLayersBox
          :title="t('MtiFarokhi.title')"
          src="/img/mtifarokhi.jpg"
          to="https://instagram.com/mtifrokhi/"
          color="indigo"
        >
          <!--      <img-->
          <!--                  class=" size-10 h-7 w-8"-->
          <!--                  src="/img/accountract.png"-->
          <!--                  alt=""-->
          <!--                >-->
          {{ t("MtiFarokhi.description") }}

        </LandingLayersBox>
        <LandingLayersBox
          title="Mehdi Mirzaie"
          icon="fa6-brands:github"
          to="https://cssninja.io/faq/github-access"
          color="purple"
        >
          We built Github automation that allows you to access to our private
          repositories, for the products you've purchased from us.
        </LandingLayersBox>
        <LandingLayersBox
          title="Reza Karimi"
          icon="fa6-brands:discord"
          to="https://go.cssninja.io/discord"
        >
          We have a thrilling Discord community where you can discuss your work
          and get help from our community of customers and developers.
        </LandingLayersBox>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
</script>
