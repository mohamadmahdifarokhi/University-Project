<script setup lang="ts">
const {open} = usePanels()

import {useAppStore} from "~/stores/app";
import {storeToRefs} from "pinia";

const app = useAppStore();
const {flag} = storeToRefs(app);
const loadTextDirection = app.loadTextDirection;
const {locale, locales} = useI18n()

const initializeData = async () => {
  await loadTextDirection();
};

initializeData();

</script>

<template>
  <button
    type="button"
    class="bg-primary-700 flex size-9 items-center justify-center rounded-full transition-all duration-300"
    @click="open('language')"
  >
    <img
      v-if="flag"
      :class="locale === 'en' ? 'h-7 w-7 rounded-full' : 'h-8 w-8 rounded-full'"
      :src="locale === 'en' ? '/img/icons/flags/united-states-of-america.svg' : '/img/icons/flags/iran.png'"
      alt="flag icon"
    >
  </button>
</template>
