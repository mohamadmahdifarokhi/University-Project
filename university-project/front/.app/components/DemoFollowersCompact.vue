<script setup lang="ts">
const followers = [
  {
    'data-nui-tooltip': 'Mti Farokhi',
    'src': '/img/mtifarokhi.jpg',
  },
  {
    'data-nui-tooltip': 'Mehdi Mirzaie',
    'src': '/img/avatars/3.svg',
  },
  {
    'data-nui-tooltip': 'Reza Karimi',
    'src': '/img/avatars/8.svg',
  },
]
const {t} = useI18n({useScope: "local"})
const {locale, locales} = useI18n()

</script>

<template>
  <div :dir="locale === 'en' ? 'ltr' : 'rtl'">
    <div class="mb-4 flex items-center justify-between">
      <BaseHeading
        as="h3"
        size="sm"
        weight="semibold"
        lead="tight"
        class="text-muted-800 dark:text-white"
      >
        <span>{{ t("Developers") }}</span>
      </BaseHeading>
      <BaseAvatarGroup
        :avatars="followers"
        size="xs"
        :limit="3"
      />
    </div>
    <div>
      <BaseParagraph size="xs">
        <span class="text-muted-400">
          <NuxtLink
            to="#"
            class="text-primary-500 underline-offset-2 hover:underline"
          >
            {{ t("Mti") }}
          </NuxtLink>
          ,
          <NuxtLink
            to="#"
            class="text-primary-500 underline-offset-2 hover:underline"
          >
            {{ t("Mehdi") }}
          </NuxtLink>
            {{ t("And") }}
          <NuxtLink
            to="#"
            class="text-primary-500 underline-offset-2 hover:underline"
          >
            {{ t("Reza") }}
          </NuxtLink>
        {{ t("Participation") }}

        </span>
        <NuxtLink
          to="https://t.me/mtifarokhi"
          class="underline-offset-2 hover:underline"
        >
          <Icon name="ri:telegram-fill" class="size-6 ms-1"/>

        </NuxtLink>

      </BaseParagraph>
    </div>
  </div>
</template>
