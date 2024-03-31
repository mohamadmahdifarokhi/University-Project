const LOGIN_PATH = '/login';
const SIGNUP_PATH = '/signup';
const EN_LOGIN_PATH = '/en/login'; // Fixing the typo
const EN_SIGNUP_PATH = '/en/signup';
const LANDING_PATH = '/';
const EN_LANDING_PATH = '/en';

const protectedPaths = [LOGIN_PATH, SIGNUP_PATH, EN_LOGIN_PATH, EN_SIGNUP_PATH,LANDING_PATH,EN_LANDING_PATH];

export default defineNuxtRouteMiddleware((to, from) => {
  // Parse the from.fullPath to check if it contains callBackUrl parameter

  if (!protectedPaths.includes(from.fullPath) && protectedPaths.includes(to.fullPath)) {
    if (!from.fullPath.includes('callBackUrl')) {
      const callBackUrl = encodeURIComponent(from.fullPath);
      return navigateTo(`${to.fullPath}?callBackUrl=${callBackUrl}`);
    } else {
      return navigateTo(`${to.fullPath}?callBackUrl=${from.query.callBackUrl}`);

    }

  }

});
