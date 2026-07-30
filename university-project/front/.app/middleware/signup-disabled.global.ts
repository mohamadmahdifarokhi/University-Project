export default defineNuxtRouteMiddleware((to) => {
  if (to.path === '/signup') {
    return navigateTo('/login', { replace: true })
  }
})
