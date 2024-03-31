import {useAuthStore} from "@/stores/auth";


export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  if (authStore.isAuthenticated) {
    if (from.path.startsWith('/en/')) {
      // Redirect to '/en/'
      return navigateTo('/en/');
    } else {
      // Redirect to '/'
      return navigateTo('/');
    }
  }
})
