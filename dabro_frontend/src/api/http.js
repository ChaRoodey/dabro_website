import axios from 'axios'

export const fastApi = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  paramsSerializer: {
    indexes: null
  },
  withCredentials: true,
})
