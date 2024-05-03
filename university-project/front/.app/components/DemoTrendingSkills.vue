<script setup lang="ts">
const skills = [
  {
    id: 0,
    name: 'Peak Hour Consumption',
    count: 149,
    icon: 'ri:time-fill',
  },
  {
    id: 1,
    name: 'Peak Power Consumption',
    count: 117,
    icon: 'ri:flashlight-fill',
  },
  // {
  //   id: 2,
  //   name: 'Nuxt',
  //   count: 94,
  //   icon: 'logos:nuxt-icon',
  // },
  // {
  //   id: 4,
  //   name: 'Tailwind CSS',
  //   count: 82,
  //   icon: 'logos:tailwindcss-icon',
  // },
]
</script>

<template>
  <div class="mb-2 space-y-5">
    <div
      v-for="skill in skills"
      :key="skill.id"
      class="flex items-center gap-3"
    >
      <div
        class="border-muted-200 dark:border-muted-700 flex size-10 items-center justify-center rounded-full border"
      >
        <Icon :name="skill.icon" class="size-5" />

      </div>
      <div >
        <BaseHeading
          as="h4"
          size="sm"
          weight="light"
          lead="tight"
          class="text-muted-800 dark:text-white"
        >
          <span>{{ skill.name }}</span>
        </BaseHeading>
        <BaseParagraph size="xs">
          <span class="text-muted-400">
            {{ skill.count }}
          </span>
        </BaseParagraph>
      </div>
<!--      <div class="ms-auto flex items-center">-->
<!--        <BaseButtonIcon-->
<!--          rounded="lg"-->
<!--          muted-->
<!--          class="scale-75"-->
<!--        >-->
<!--          <Icon name="lucide:arrow-right" class="size-5" />-->
<!--        </BaseButtonIcon>-->
<!--      </div>-->
    </div>
  </div>
</template>
