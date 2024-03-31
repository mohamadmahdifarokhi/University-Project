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
    if (process.client) {
      loadExternalScript();
    }
  });

  const loadExternalScript = () => {
    const script = document.createElement('script');
    script.src = "https://widget-react.raychat.io/install/widget.js";
    script.async = true;
    document.head.appendChild(script);
  };

  // Setting the RAYCHAT_TOKEN and LOAD_TYPE (only if running on the client-side)
  if (process.client) {
    window.RAYCHAT_TOKEN = "9aef56fb-fc4d-495b-91fa-f448a567efeb";
    window.LOAD_TYPE = "SEO_FRIENDLY";
  }
</script>

<template>

  <TairoSidebarLayout>
    <slot />
  </TairoSidebarLayout>


</template>
