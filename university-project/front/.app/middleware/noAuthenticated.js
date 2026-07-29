import {useAuthStore} from "@/stores/auth";


export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();
  await authStore.checkAccessToken();
  if (authStore.isAuthenticated) {
    return navigateTo(to.path.startsWith('/en/') ? '/en/dashboard' : '/dashboard');
  }
})
