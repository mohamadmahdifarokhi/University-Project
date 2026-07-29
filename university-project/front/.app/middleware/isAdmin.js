import { useAuthStore } from "@/stores/auth";

export default defineNuxtRouteMiddleware(async () => {
  const authStore = useAuthStore();
  await authStore.checkAccessToken();
  if (!authStore.isAdmin) {
    return navigateTo('/dashboard');
  }
});
