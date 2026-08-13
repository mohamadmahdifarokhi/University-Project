import { useAuthStore } from "@/stores/auth";
import {useAppStore} from "~/stores/app";

export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();
  await authStore.checkAccessToken();
  if (!authStore.isAuthenticated) {
    const login = to.path.startsWith('/en/') ? '/en/login' : '/login';
    return navigateTo(`${login}?callBackUrl=${encodeURIComponent(to.fullPath)}`);
  }
});
