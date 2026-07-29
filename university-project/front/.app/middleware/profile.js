import { useAuthStore } from "@/stores/auth";

export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();
  await authStore.checkAccessToken();
  const english = to.path.startsWith('/en/');
  if (!authStore.isAuthenticated) return navigateTo(english ? '/en/login' : '/login');
  return navigateTo(english ? '/en/profile/orders' : '/profile/orders', { replace: true });
});
