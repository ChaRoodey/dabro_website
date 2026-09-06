import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const api = axios.create({
    baseURL: config.public.apiBase,
    timeout: 10_000,
    paramsSerializer: { indexes: null },
    withCredentials: true,
  })

  return {
    provide: { api },
  }
})
