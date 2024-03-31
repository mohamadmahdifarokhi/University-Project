import { useAuthStore } from "@/stores/auth";

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
          console.log(authStore.isAdmin,"qweqwew")

  if (!authStore.isAdmin) {
    if (from.path.startsWith('/en/')) {
      // Redirect to '/en/login'
      return navigateTo('/en/');
    } else {
      // Redirect to '/login'
      return navigateTo('/');
    }
  }
});
