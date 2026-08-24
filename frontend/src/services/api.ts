import axios, { type AxiosInstance } from 'axios'

function logRequest(
  config: { method?: string; url?: string },
  status: number | string,
  symbol: '→' | '✓' | '✗',
) {
  console.log(`${symbol} ${config.method?.toUpperCase()} ${config.url} → ${status}`)
}

const api: AxiosInstance = axios.create({
  baseURL: '/api',
  withCredentials: true,
})

let refreshPromise: Promise<void> | null = null

api.interceptors.response.use(
  (response) => {
    logRequest(response.config, response.status, '✓')
    return response
  },
  async (error) => {
    const original = error.config

    if (original.url === '/auth/refresh') {
      return Promise.reject(error)
    }

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true

      if (!refreshPromise) {
        refreshPromise = api
          .post('/auth/refresh')
          .then(() => undefined)
          .finally(() => {
            refreshPromise = null
          })
      }

      try {
        await refreshPromise
        return api(original)
      } catch {
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  },
)

export default api
