import {useAuthStore} from "@/stores/auth";


export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  if (authStore.isAuthenticated) {
    if (from.path.startsWith('/en/')) {
      // Redirect to '/en/'
      return navigateTo('/en/dashboard');
    } else {
      // Redirect to '/'
      return navigateTo('/dashboard');
    }
  }
})
