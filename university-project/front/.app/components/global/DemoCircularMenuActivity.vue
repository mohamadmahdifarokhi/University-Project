<script setup lang="ts">
const { open } = usePanels()
</script>

<template>
  <button
    type="button"
    class="bg-primary-700 flex size-9 items-center justify-center rounded-full transition-all duration-300"
    @click="open('activity')"
  >
<!--    <Icon name="ph:circles-four-duotone" class="size-5 text-white" />-->
    <img class="grayscale-100  dark:invert  w-6 h-5" src="/img/icons/shop.png" alt="flag icon">

  </button>
</template>
