<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Navigation Bar -->
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Brand -->
          <div class="flex items-center">
            <router-link to="/" class="flex items-center space-x-3 hover:opacity-80 transition-opacity">
              <div class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div class="hidden sm:block">
                <h1 class="text-xl font-bold text-slate-900">{{ $t('nav.brand') }}</h1>
                <p class="text-xs text-slate-500 -mt-1">{{ $t('nav.tagline') }}</p>
              </div>
            </router-link>
          </div>

          <!-- Navigation Menu -->
          <div class="flex items-center space-x-4">
            <!-- Language Selector -->
            <LanguageSelector />
            
            <template v-if="isAuthenticated">
              <div class="hidden md:flex items-center space-x-1">
                <router-link 
                  to="/students" 
                  class="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
                  :class="{ 'text-indigo-600 bg-indigo-50 hover:bg-indigo-100 hover:text-indigo-700': $route.path === '/students' }"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  {{ $t('nav.students') }}
                </router-link>
                
                <router-link 
                  to="/analytics" 
                  class="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
                  :class="{ 'text-indigo-600 bg-indigo-50 hover:bg-indigo-100 hover:text-indigo-700': $route.path === '/analytics' }"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  {{ $t('nav.reports') }}
                </router-link>
              </div>

              <!-- User Menu -->
              <div class="relative">
                <button 
                  @click="toggleUserMenu"
                  class="flex items-center space-x-3 p-2 rounded-lg hover:bg-slate-100 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <div class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                    {{ userInitials }}
                  </div>
                  <div class="hidden sm:block text-left">
                    <p class="text-sm font-medium text-slate-900">{{ userName }}</p>
                    <p class="text-xs text-slate-500">Administrator</p>
                  </div>
                  <svg class="w-4 h-4 text-slate-400 transition-transform" :class="{ 'rotate-180': showUserMenu }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                <!-- User Dropdown Menu -->
                <transition
                  enter-active-class="transition ease-out duration-200"
                  enter-from-class="opacity-0 scale-95"
                  enter-to-class="opacity-100 scale-100"
                  leave-active-class="transition ease-in duration-75"
                  leave-from-class="opacity-100 scale-100"
                  leave-to-class="opacity-0 scale-95"
                >
                  <div v-if="showUserMenu" class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-slate-200 py-2 z-50">
                    <div class="px-4 py-2 border-b border-slate-100">
                      <p class="text-sm font-medium text-slate-900">{{ userEmail }}</p>
                      <p class="text-xs text-slate-500">{{ $t('auth.login.signedInAs') }}</p>
                    </div>
                    
                    <div class="py-1">
                      <router-link to="/profile" class="flex items-center space-x-3 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100 cursor-pointer transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        {{ $t('nav.profile') }}
                      </router-link>
                      <router-link to="/settings" class="flex items-center space-x-3 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100 cursor-pointer transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {{ $t('nav.settings') }}
                      </router-link>
                      <a href="#" class="flex items-center space-x-3 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100 cursor-pointer transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {{ $t('nav.help') }}
                      </a>
                    </div>
                    
                    <div class="border-t border-slate-100 py-1">
                      <button @click="logout" class="flex items-center space-x-3 px-4 py-2 text-sm text-red-700 hover:bg-red-50 cursor-pointer transition-colors w-full text-left">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        {{ $t('nav.logout') }}
                      </button>
                    </div>
                  </div>
                </transition>
              </div>
            </template>
            
            <!-- Login Link for unauthenticated users -->
            <template v-else>
              <router-link to="/login" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                <span>{{ $t('nav.login') }}</span>
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>

    <!-- Loading Overlay -->
    <transition
      enter-active-class="transition-opacity ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 flex flex-col items-center space-y-4 shadow-xl">
          <div class="animate-spin rounded-full h-8 w-8 border-2 border-indigo-500 border-t-transparent"></div>
          <p class="text-slate-600 font-medium">{{ $t('common.loading') }}</p>
        </div>
      </div>
    </transition>

    <!-- Click outside handler for user menu -->
    <div v-if="showUserMenu" @click="showUserMenu = false" class="fixed inset-0 z-40"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import LanguageSelector from './LanguageSelector.vue'

const router = useRouter()
const { isAuthenticated, userEmail, loading, logout: performLogout, checkAuth } = useAuth()

// User menu state
const showUserMenu = ref(false)

// Computed properties
const userInitials = computed(() => {
  if (!userEmail.value) return 'U'
  const emailParts = userEmail.value.split('@')[0]
  return emailParts.charAt(0).toUpperCase()
})

const userName = computed(() => {
  if (!userEmail.value) return 'User'
  return userEmail.value.split('@')[0]
})

// Methods
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const logout = async () => {
  showUserMenu.value = false
  await performLogout()
  router.push('/login')
}

// Close user menu when clicking outside
const handleClickOutside = (event: Event) => {
  const target = event.target as Element
  if (!target.closest('.relative')) {
    showUserMenu.value = false
  }
}

// Check authentication status on mount
onMounted(() => {
  checkAuth()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Custom styles for specific animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
</style>
