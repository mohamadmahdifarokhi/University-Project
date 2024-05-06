<script setup lang="ts">
  import { useAuthStore } from "~/stores/auth";
  import { useAppStore } from "~/stores/app";
  import { useI18n } from "vue-i18n";
  import { onMounted } from 'vue';

  const app = useAppStore();
  const loadTextDirection = app.loadTextDirection;
  const { locale, locales } = useI18n();
  const authStore = useAuthStore();
  const checkAccessToken = authStore.checkAccessToken;

  const initializeData = async () => {
    await loadTextDirection();
    await checkAccessToken();
    
  };

  onMounted(() => {
    initializeData();
  });
</script>

<template>

  <TairoSidebarLayout>
    <slot />
  </TairoSidebarLayout>


</template>
