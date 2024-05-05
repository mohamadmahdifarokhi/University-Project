const LOGIN_PATH = '/login';
const SIGNUP_PATH = '/signup';
const LANDING_PATH = '/';

const protectedPaths = [LOGIN_PATH, SIGNUP_PATH,LANDING_PATH];

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
