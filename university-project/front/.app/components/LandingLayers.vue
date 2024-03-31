<script setup lang="ts">
const {locale, locales} = useI18n()
const localPath = useLocalePath();
const {t} = useI18n({useScope: "local"})

</script>
<template>
  <div class="dark:bg-muted-900 bg-white py-24" :dir="locale === 'en' ? 'ltr' : 'rtl'">
    <div class="mx-auto w-full max-w-7xl px-4">
      <div class="mb-10 max-w-2xl">
<!--        <BaseText class="text-primary-500 mb-2 text-[0.65rem] uppercase tracking-wider">-->
<!--          Tailored for Developers-->
<!--        </BaseText>-->
        <BaseHeading as="h2" size="4xl" weight="light" lead="tight" class="text-muted-800 mx-auto mb-4 dark:text-white">
          {{ t("ExploreFeatures.title") }}
        </BaseHeading>
        <BaseParagraph size="lg" class="text-muted-500 dark:text-muted-100 mx-auto mb-4">
          {{ t("ExploreFeatures.description") }}
        </BaseParagraph>
      </div>
      <div class="ptablet:grid-cols-2 grid gap-6 sm:grid-cols-3">
        <LandingLayersBox :title="t('Accounts')" icon="ph:wallet-duotone" :to="localPath('/')" color="purple">
          {{ t("LandingLayersBox.Accounts") }}
        </LandingLayersBox>
        <LandingLayersBox :title="t('GPT-4')" icon="ph:brain-duotone" :to="localPath('/')" color="purple">
          {{ t("LandingLayersBox.GPT-4") }}
        </LandingLayersBox>
        <LandingLayersBox :title="t('Fast Delivery')" icon="ph:rocket-duotone"
                          :to="localPath('/')" color="purple">
          {{ t("LandingLayersBox.FastDelivery") }}
        </LandingLayersBox>
      </div>
    </div>
  </div>
</template>
