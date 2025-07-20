import axios from 'axios'
import type { LoginRequest, LoginResponse, UserResponse } from '@/types/auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// Create axios instance for auth
const authClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include auth token
authClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Add response interceptor for error handling
authClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  // Login
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await authClient.post('/auth/login', credentials)
    return response.data
  },

  // Get current user info
  async getCurrentUser(): Promise<UserResponse> {
    const response = await authClient.get('/auth/me')
    return response.data
  }
}

// Export configured axios instance for other API calls
export const apiClient = authClient
