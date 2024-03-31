import { useAuthStore } from "@/stores/auth";

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  if (authStore.isAuthenticated) {
    if (from.path.startsWith('/en/')) {
      // Redirect to '/en/profile/orders'
      return navigateTo('/en/profile/orders');
    } else {
      // Redirect to '/profile/orders'
      return navigateTo('/profile/orders');
    }
  } else {
    if (from.path.startsWith('/en/')) {
      // Redirect to '/en/login'
      return navigateTo('/en/login');
    } else {
      // Redirect to '/login'
      return navigateTo('/login');
    }
  }
});
