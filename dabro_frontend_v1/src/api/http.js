import axios from 'axios'

export const fastApi = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  paramsSerializer: {
    indexes: null
  },
  withCredentials: true,
})
