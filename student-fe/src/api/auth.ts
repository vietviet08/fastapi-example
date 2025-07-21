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

// Create axios instance for general API calls with auth
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include auth token for apiClient
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

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
  },

  // Update user profile
  async updateProfile(data: { email?: string }): Promise<UserResponse> {
    const response = await authClient.patch('/auth/me', data)
    return response.data
  },

  // Change password
  async changePassword(data: { current_password: string, new_password: string }): Promise<void> {
    await authClient.post('/auth/change-password', data)
  }
}
