import axios from 'axios'

const apiUrl = `${import.meta.env.VITE_BACKEND_SERVER_URL}`
let refreshPromise = null

export default defineNuxtPlugin(() => {
  // Nuxt can re-run a client plugin during hot reload; do not stack interceptors.
  if (axios.__energyAuthInterceptorInstalled) return
  axios.__energyAuthInterceptorInstalled = true

  axios.interceptors.response.use(
    response => response,
    async (error) => {
      const request = error.config
      const isRefreshRequest = String(request?.url || '').includes('/users/refresh')

      if (error.response?.status !== 401 || !request || request._authRetry || isRefreshRequest) {
        return Promise.reject(error)
      }

      const refreshToken = useCookie('refresh_token').value
      if (!refreshToken) return Promise.reject(error)

      if (!refreshPromise) {
        refreshPromise = axios.post(`${apiUrl}/users/refresh`, {}, {
          headers: { Authorization: `Bearer ${refreshToken}` },
        }).then((response) => {
          const token = response.data?.access_token
          if (!token) throw new Error('Refresh response did not include an access token')
          setCookie('access_token', token)
          if (import.meta.client) localStorage.setItem('access_token', token)
          return token
        }).finally(() => {
          refreshPromise = null
        })
      }

      try {
        const accessToken = await refreshPromise
        request._authRetry = true
        request.headers = request.headers || {}
        request.headers.Authorization = `Bearer ${accessToken}`
        return axios(request)
      } catch {
        return Promise.reject(error)
      }
    },
  )
})
