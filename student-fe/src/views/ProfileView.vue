<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('profile.title') }}</h1>
    </div>
    
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-10 w-10 border-2 border-indigo-500 border-t-transparent"></div>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
      <p class="text-red-500 text-lg">{{ error }}</p>
      <button 
        @click="loadUserData"
        class="mt-3 bg-red-100 text-red-600 hover:bg-red-200 px-4 py-2 rounded-md font-medium transition-colors"
      >
        {{ $t('common.tryAgain') }}
      </button>
    </div>
    
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <!-- Profile header with avatar -->
      <div class="px-6 py-8 bg-gradient-to-r from-indigo-600 to-purple-600">
        <div class="flex items-center space-x-6">
          <div class="w-24 h-24 bg-white bg-opacity-20 rounded-full flex items-center justify-center text-white font-bold text-3xl">
            {{ userInitials }}
          </div>
          <div class="text-white">
            <h2 class="text-2xl font-bold">
              {{ userData?.email }}
            </h2>
            <p class="text-blue-100">
              {{ userData?.is_admin ? $t('profile.adminRole') : $t('profile.userRole') }}
            </p>
          </div>
        </div>
      </div>
      
      <!-- Profile form -->
      <div class="p-6">
        <form @submit.prevent="saveChanges" class="space-y-6">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.email') }}</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
          </div>
          
          <!-- Password fields -->
          <div class="space-y-4">
            <h3 class="text-lg font-medium text-gray-900 border-b border-gray-200 pb-2">{{ $t('profile.changePassword') }}</h3>
            
            <div>
              <label for="current_password" class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.currentPassword') }}</label>
              <input
                id="current_password"
                v-model="formData.currentPassword"
                type="password"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                :placeholder="$t('profile.passwordPlaceholder')"
              />
            </div>
            
            <div>
              <label for="new_password" class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.newPassword') }}</label>
              <input
                id="new_password"
                v-model="formData.newPassword"
                type="password"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                :placeholder="$t('profile.newPasswordPlaceholder')"
                :disabled="!formData.currentPassword"
              />
            </div>
            
            <div>
              <label for="confirm_password" class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.confirmPassword') }}</label>
              <input
                id="confirm_password"
                v-model="formData.confirmPassword"
                type="password"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                :placeholder="$t('profile.confirmPasswordPlaceholder')"
                :disabled="!formData.currentPassword || !formData.newPassword"
              />
              <p v-if="passwordMismatch && formData.confirmPassword" class="mt-1 text-sm text-red-600">
                {{ $t('profile.passwordsMustMatch') }}
              </p>
            </div>
          </div>
          
          <!-- Submit buttons -->
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="resetForm"
              class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              {{ $t('common.cancel') }}
            </button>
            <button
              type="submit"
              :disabled="isSubmitting || passwordMismatch"
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400 disabled:cursor-not-allowed"
            >
              <span v-if="isSubmitting" class="flex items-center">
                <span class="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                {{ $t('common.saving') }}
              </span>
              <span v-else>{{ $t('common.save') }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useAuth } from '@/composables/useAuth'
import { useI18n } from 'vue-i18n'
import type { UserResponse, ProfileUpdateRequest, PasswordChangeRequest } from '@/types/auth'
import { authAPI } from '@/api/auth'

const toast = useToast()
const { t } = useI18n()
const { user: authUser, checkAuth } = useAuth()

// State
const loading = ref(false)
const error = ref('')
const isSubmitting = ref(false)
const userData = ref<UserResponse | null>(null)

// Form data
const formData = ref({
  email: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Computed
const userInitials = computed(() => {
  if (!userData.value?.email) return 'U'
  return userData.value.email.charAt(0).toUpperCase()
})

const passwordMismatch = computed(() => {
  if (!formData.value.newPassword || !formData.value.confirmPassword) return false
  return formData.value.newPassword !== formData.value.confirmPassword
})

// Methods
const loadUserData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Try to get user from auth store first
    if (authUser.value) {
      userData.value = authUser.value
    } else {
      // If not available in store, fetch directly from API
      userData.value = await authAPI.getCurrentUser()
    }
    
    // Update form data with user info
    if (userData.value) {
      formData.value.email = userData.value.email
    }
  } catch (err) {
    console.error('Error loading user data:', err)
    error.value = t('profile.loadError')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  // Reset form to original values
  if (userData.value) {
    formData.value.email = userData.value.email
  }
  formData.value.currentPassword = ''
  formData.value.newPassword = ''
  formData.value.confirmPassword = ''
}

const saveChanges = async () => {
  if (passwordMismatch.value) return
  
  isSubmitting.value = true
  
  try {
    // Update email if changed
    if (userData.value && userData.value.email !== formData.value.email) {
      const profileData: ProfileUpdateRequest = {
        email: formData.value.email
      }
      
      userData.value = await authAPI.updateProfile(profileData)
      toast.success(t('profile.updateSuccess'))
    }
    
    // Change password if provided
    if (formData.value.currentPassword && formData.value.newPassword) {
      const passwordData: PasswordChangeRequest = {
        current_password: formData.value.currentPassword,
        new_password: formData.value.newPassword
      }
      
      await authAPI.changePassword(passwordData)
      toast.success(t('profile.passwordChangeSuccess'))
      
      // Clear password fields
      formData.value.currentPassword = ''
      formData.value.newPassword = ''
      formData.value.confirmPassword = ''
    }
  } catch (err) {
    console.error('Error updating profile:', err)
    toast.error(t('profile.updateError'))
  } finally {
    isSubmitting.value = false
  }
}

// Lifecycle
onMounted(async () => {
  // If user data is not available, try to refresh auth state first
  if (!authUser.value) {
    await checkAuth()
  }
  loadUserData()
})
</script> 