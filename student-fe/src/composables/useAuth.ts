import { ref, computed } from 'vue'
import { authAPI } from '@/api/auth'
import type { LoginRequest, LoginResponse, UserResponse } from '@/types/auth'

// Global auth state
const token = ref<string | null>(localStorage.getItem('authToken'))
const user = ref<UserResponse | null>(null)
const loading = ref(false)

export function useAuth() {
  // Computed properties
  const isAuthenticated = computed(() => !!token.value)
  const userEmail = computed(() => user.value?.email || '')

  // Login function
  const login = async (credentials: LoginRequest): Promise<boolean> => {
    try {
      loading.value = true
      const response = await authAPI.login(credentials)
      
      token.value = response.access_token
      user.value = response.user
      
      // Save to localStorage
      localStorage.setItem('authToken', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  // Logout function
  const logout = async () => {
    try {
      loading.value = true
      
      // Clear local state
      token.value = null
      user.value = null
      
      // Clear localStorage
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      loading.value = false
    }
  }

  // Check auth status
  const checkAuth = async () => {
    const savedToken = localStorage.getItem('authToken')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      try {
        // Verify token by calling /auth/me
        const response = await authAPI.getCurrentUser()
        
        token.value = savedToken
        user.value = response
        
      } catch (error) {
        // Token is invalid, clear auth
        console.error('Token verification failed:', error)
        logout()
      }
    }
  }

  // Get auth headers for API calls
  const getAuthHeaders = () => {
    if (!token.value) return {}
    return {
      Authorization: `Bearer ${token.value}`
    }
  }

  return {
    // State
    isAuthenticated,
    user: computed(() => user.value),
    userEmail,
    loading: computed(() => loading.value),
    
    // Actions
    login,
    logout,
    checkAuth,
    getAuthHeaders
  }
}
