import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: API_URL + '/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const adminToken = localStorage.getItem('admin_token')
  const studentToken = localStorage.getItem('access_token')
  
  let token = null
  if (
    config.url.startsWith('/admin') ||
    config.url.startsWith('/results') ||
    config.url.startsWith('/students') ||
    config.url.startsWith('/questions')
  ) {
    token = adminToken
  } else {
    token = studentToken
  }

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
