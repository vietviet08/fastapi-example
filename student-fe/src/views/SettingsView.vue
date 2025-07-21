<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex justify-between items-center mb-2">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('settings.title') }}</h1>
    </div>
    
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-10 w-10 border-2 border-indigo-500 border-t-transparent"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
      <p class="text-red-500 text-lg">{{ error }}</p>
      <button 
        @click="loadSettings"
        class="mt-3 bg-red-100 text-red-600 hover:bg-red-200 px-4 py-2 rounded-md font-medium transition-colors"
      >
        {{ $t('common.tryAgain') }}
      </button>
    </div>
    
    <div v-else class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Settings navigation sidebar -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <nav class="flex flex-col">
            <button 
              v-for="(section, index) in settingSections" 
              :key="index"
              @click="activeSection = section.id"
              class="px-4 py-3 text-left flex items-center space-x-3 hover:bg-slate-50 transition-colors"
              :class="activeSection === section.id ? 'bg-slate-50 border-l-4 border-indigo-500 font-medium text-indigo-600' : 'text-slate-700'"
            >
              <span class="text-lg" v-html="section.icon"></span>
              <span>{{ $t(section.title) }}</span>
            </button>
          </nav>
        </div>
      </div>
      
      <!-- Settings content area -->
      <div class="lg:col-span-3 space-y-6">
        <!-- Appearance Settings -->
        <div v-if="activeSection === 'appearance'" class="bg-white rounded-lg shadow">
          <div class="border-b border-gray-200 px-6 py-4">
            <h2 class="text-xl font-medium text-gray-900">{{ $t('settings.appearance.title') }}</h2>
            <p class="text-sm text-gray-500">{{ $t('settings.appearance.subtitle') }}</p>
          </div>
          
          <div class="p-6 space-y-6">
            <!-- Language Setting -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">{{ $t('settings.appearance.language') }}</label>
              <div class="flex flex-wrap gap-3">
                <button 
                  v-for="lang in languages" 
                  :key="lang.code"
                  @click="setLanguage(lang.code)"
                  class="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors border"
                  :class="currentLanguage === lang.code ? 'bg-indigo-50 border-indigo-300 text-indigo-700' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'"
                >
                  <span class="text-lg">{{ lang.flag }}</span>
                  <span>{{ lang.name }}</span>
                </button>
              </div>
            </div>
            
            <!-- Theme Setting -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">{{ $t('settings.appearance.theme') }}</label>
              <div class="flex flex-wrap gap-3">
                <button 
                  v-for="theme in themes" 
                  :key="theme.id"
                  @click="setTheme(theme.id)"
                  class="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors border"
                  :class="currentTheme === theme.id ? 'bg-indigo-50 border-indigo-300 text-indigo-700' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'"
                >
                  <span class="w-4 h-4 rounded" :class="theme.colorClass"></span>
                  <span>{{ $t(theme.name) }}</span>
                </button>
              </div>
            </div>
            
            <!-- Date Format Setting -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">{{ $t('settings.appearance.dateFormat') }}</label>
              <select
                v-model="settings.dateFormat"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option v-for="format in dateFormats" :key="format.id" :value="format.id">
                  {{ format.label }} ({{ format.example }})
                </option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- Notification Settings -->
        <div v-if="activeSection === 'notifications'" class="bg-white rounded-lg shadow">
          <div class="border-b border-gray-200 px-6 py-4">
            <h2 class="text-xl font-medium text-gray-900">{{ $t('settings.notifications.title') }}</h2>
            <p class="text-sm text-gray-500">{{ $t('settings.notifications.subtitle') }}</p>
          </div>
          
          <div class="p-6 space-y-6">
            <div v-for="(notification, i) in notificationSettings" :key="i" class="flex items-center justify-between py-3">
              <div>
                <h3 class="text-sm font-medium text-gray-700">{{ $t(notification.title) }}</h3>
                <p class="text-xs text-gray-500">{{ $t(notification.description) }}</p>
              </div>
              <div class="ml-4">
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="settings.notifications[notification.id]" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                </label>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Security Settings -->
        <div v-if="activeSection === 'security'" class="bg-white rounded-lg shadow">
          <div class="border-b border-gray-200 px-6 py-4">
            <h2 class="text-xl font-medium text-gray-900">{{ $t('settings.security.title') }}</h2>
            <p class="text-sm text-gray-500">{{ $t('settings.security.subtitle') }}</p>
          </div>
          
          <div class="p-6 space-y-6">
            <!-- Two-Factor Authentication -->
            <div class="space-y-2">
              <div class="flex justify-between">
                <div>
                  <h3 class="text-sm font-medium text-gray-700">{{ $t('settings.security.twoFactor.title') }}</h3>
                  <p class="text-xs text-gray-500">{{ $t('settings.security.twoFactor.description') }}</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="settings.twoFactorEnabled" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                </label>
              </div>
              
              <div v-if="settings.twoFactorEnabled" class="mt-4 p-4 bg-gray-50 rounded-md">
                <div class="text-center space-y-4">
                  <p class="text-sm text-gray-700">{{ $t('settings.security.twoFactor.setupInstructions') }}</p>
                  <div class="inline-block p-2 bg-white rounded border border-gray-200">
                    <!-- Placeholder for QR code -->
                    <div class="w-48 h-48 bg-gray-100 flex items-center justify-center">
                      <span class="text-gray-400">{{ $t('settings.security.twoFactor.qrCode') }}</span>
                    </div>
                  </div>
                  <div class="max-w-xs mx-auto">
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('settings.security.twoFactor.verifyCode') }}</label>
                    <input
                      type="text"
                      v-model="verificationCode"
                      class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      :placeholder="$t('settings.security.twoFactor.enterCode')"
                    />
                  </div>
                  <button 
                    class="mt-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md text-sm font-medium transition-colors"
                    @click="verifyTwoFactor"
                  >
                    {{ $t('settings.security.twoFactor.verify') }}
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Session Management -->
            <div class="space-y-2 pt-4 border-t border-gray-200">
              <h3 class="text-sm font-medium text-gray-700">{{ $t('settings.security.sessions.title') }}</h3>
              <p class="text-xs text-gray-500 mb-4">{{ $t('settings.security.sessions.description') }}</p>
              
              <div class="space-y-4">
                <div v-for="(session, i) in sessions" :key="i" class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div class="flex items-center space-x-3">
                    <div class="p-2 bg-white rounded-full">
                      <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path v-if="session.deviceType === 'desktop'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        <path v-else-if="session.deviceType === 'mobile'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-sm font-medium">{{ session.device }} - {{ session.browser }}</p>
                      <p class="text-xs text-gray-500">{{ session.location }} · {{ session.lastActive }}</p>
                    </div>
                  </div>
                  <button 
                    v-if="!session.current"
                    @click="logoutSession(session.id)"
                    class="text-xs text-red-600 hover:text-red-800 font-medium"
                  >
                    {{ $t('settings.security.sessions.terminate') }}
                  </button>
                  <span v-else class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">{{ $t('settings.security.sessions.current') }}</span>
                </div>
              </div>
              
              <button 
                @click="logoutAllSessions"
                class="mt-4 px-4 py-2 border border-gray-300 bg-white hover:bg-gray-50 rounded-md text-sm font-medium transition-colors"
              >
                {{ $t('settings.security.sessions.logoutAll') }}
              </button>
            </div>
            
            <!-- Password Requirements -->
            <div class="space-y-2 pt-4 border-t border-gray-200">
              <h3 class="text-sm font-medium text-gray-700">{{ $t('settings.security.passwordPolicy.title') }}</h3>
              <p class="text-xs text-gray-500">{{ $t('settings.security.passwordPolicy.description') }}</p>
              
              <div class="space-y-2 mt-2">
                <div v-for="(policy, i) in passwordPolicies" :key="i" class="flex items-center space-x-2">
                  <div class="w-4 h-4 rounded-full flex items-center justify-center" :class="policy.enabled ? 'bg-green-100' : 'bg-gray-100'">
                    <svg v-if="policy.enabled" class="w-3 h-3 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <span class="text-sm" :class="policy.enabled ? 'text-gray-800' : 'text-gray-500'">{{ $t(policy.description) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- System Settings (Admin only) -->
        <div v-if="activeSection === 'system' && isAdmin" class="bg-white rounded-lg shadow">
          <div class="border-b border-gray-200 px-6 py-4">
            <h2 class="text-xl font-medium text-gray-900">{{ $t('settings.system.title') }}</h2>
            <p class="text-sm text-gray-500">{{ $t('settings.system.subtitle') }}</p>
          </div>
          
          <div class="p-6 space-y-6">
            <!-- System Maintenance Mode -->
            <div class="flex justify-between items-start pb-4 border-b border-gray-200">
              <div>
                <h3 class="text-sm font-medium text-gray-700">{{ $t('settings.system.maintenanceMode.title') }}</h3>
                <p class="text-xs text-gray-500">{{ $t('settings.system.maintenanceMode.description') }}</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.maintenanceMode" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-red-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-red-600"></div>
              </label>
            </div>
            
            <!-- Auto Backup Settings -->
            <div class="space-y-2 pb-4 border-b border-gray-200">
              <h3 class="text-sm font-medium text-gray-700">{{ $t('settings.system.autoBackup.title') }}</h3>
              <p class="text-xs text-gray-500">{{ $t('settings.system.autoBackup.description') }}</p>
              <div class="mt-2">
                <select
                  v-model="settings.backupFrequency"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                >
                  <option value="daily">{{ $t('settings.system.autoBackup.daily') }}</option>
                  <option value="weekly">{{ $t('settings.system.autoBackup.weekly') }}</option>
                  <option value="monthly">{{ $t('settings.system.autoBackup.monthly') }}</option>
                  <option value="disabled">{{ $t('settings.system.autoBackup.disabled') }}</option>
                </select>
              </div>
            </div>
            
            <!-- Email Configuration -->
            <div class="space-y-4">
              <h3 class="text-sm font-medium text-gray-700">{{ $t('settings.system.emailConfig.title') }}</h3>
              <p class="text-xs text-gray-500">{{ $t('settings.system.emailConfig.description') }}</p>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">{{ $t('settings.system.emailConfig.smtpServer') }}</label>
                  <input
                    v-model="settings.emailConfig.smtpServer"
                    type="text"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">{{ $t('settings.system.emailConfig.port') }}</label>
                  <input
                    v-model="settings.emailConfig.port"
                    type="number"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">{{ $t('settings.system.emailConfig.username') }}</label>
                  <input
                    v-model="settings.emailConfig.username"
                    type="text"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">{{ $t('settings.system.emailConfig.password') }}</label>
                  <input
                    v-model="settings.emailConfig.password"
                    type="password"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
                <div class="md:col-span-2">
                  <label class="block text-xs font-medium text-gray-700 mb-1">{{ $t('settings.system.emailConfig.fromEmail') }}</label>
                  <input
                    v-model="settings.emailConfig.fromEmail"
                    type="email"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>
              
              <button 
                @click="testEmailConfig"
                class="mt-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md text-sm font-medium transition-colors"
              >
                {{ $t('settings.system.emailConfig.testConnection') }}
              </button>
            </div>
          </div>
        </div>
        
        <!-- Save Changes Button -->
        <div class="flex justify-end">
          <button 
            @click="saveSettings"
            :disabled="isSaving"
            class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md font-medium transition-colors disabled:bg-indigo-400 disabled:cursor-not-allowed"
          >
            <span v-if="isSaving" class="flex items-center">
              <span class="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              {{ $t('common.saving') }}
            </span>
            <span v-else>{{ $t('common.save') }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/composables/useAuth'
import { availableLanguages } from '@/i18n'

const toast = useToast()
const { t, locale } = useI18n()
const { user: authUser, checkAuth } = useAuth()

// State
const loading = ref(false)
const error = ref('')
const isSaving = ref(false)
const activeSection = ref('appearance')
const verificationCode = ref('')

// Determine if user is admin
const isAdmin = computed(() => authUser.value?.is_admin || false)

// Settings object
const settings = ref({
  language: locale.value,
  theme: 'light',
  dateFormat: 'YYYY-MM-DD',
  notifications: {
    email: true,
    system: true,
    studentUpdates: true,
    security: true
  },
  twoFactorEnabled: false,
  maintenanceMode: false,
  backupFrequency: 'weekly',
  emailConfig: {
    smtpServer: 'smtp.example.com',
    port: 587,
    username: 'user@example.com',
    password: '********',
    fromEmail: 'noreply@example.com'
  }
})

// Define settings sections
const settingSections = [
  { 
    id: 'appearance', 
    title: 'settings.appearance.title', 
    icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" /></svg>' 
  },
  { 
    id: 'notifications', 
    title: 'settings.notifications.title', 
    icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>' 
  },
  { 
    id: 'security', 
    title: 'settings.security.title', 
    icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>' 
  },
  { 
    id: 'system', 
    title: 'settings.system.title', 
    icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>' 
  }
]

// Languages, themes, and date formats options
const languages = availableLanguages
const currentLanguage = computed(() => locale.value)

const themes = [
  { id: 'light', name: 'settings.appearance.themes.light', colorClass: 'bg-white border border-gray-300' },
  { id: 'dark', name: 'settings.appearance.themes.dark', colorClass: 'bg-gray-900' },
  { id: 'system', name: 'settings.appearance.themes.system', colorClass: 'bg-gradient-to-r from-white to-gray-800' }
]
const currentTheme = computed(() => settings.value.theme)

const dateFormats = [
  { id: 'YYYY-MM-DD', label: 'ISO (YYYY-MM-DD)', example: '2023-11-15' },
  { id: 'MM/DD/YYYY', label: 'US (MM/DD/YYYY)', example: '11/15/2023' },
  { id: 'DD/MM/YYYY', label: 'EU (DD/MM/YYYY)', example: '15/11/2023' },
  { id: 'DD.MM.YYYY', label: 'DE (DD.MM.YYYY)', example: '15.11.2023' }
]

// Notification settings
const notificationSettings = [
  { id: 'email' as keyof typeof settings.value.notifications, title: 'settings.notifications.emailNotifications.title', description: 'settings.notifications.emailNotifications.description' },
  { id: 'system' as keyof typeof settings.value.notifications, title: 'settings.notifications.systemNotifications.title', description: 'settings.notifications.systemNotifications.description' },
  { id: 'studentUpdates' as keyof typeof settings.value.notifications, title: 'settings.notifications.studentUpdates.title', description: 'settings.notifications.studentUpdates.description' },
  { id: 'security' as keyof typeof settings.value.notifications, title: 'settings.notifications.securityAlerts.title', description: 'settings.notifications.securityAlerts.description' }
]

// Sample active sessions data
const sessions = [
  { id: 1, device: 'MacBook Pro', browser: 'Chrome 106', deviceType: 'desktop', location: 'Hanoi, Vietnam', lastActive: '2023-11-15 10:30:45', current: true },
  { id: 2, device: 'iPhone 13', browser: 'Safari 16', deviceType: 'mobile', location: 'Hanoi, Vietnam', lastActive: '2023-11-14 18:22:31', current: false },
  { id: 3, device: 'Windows PC', browser: 'Firefox 105', deviceType: 'desktop', location: 'Ho Chi Minh City, Vietnam', lastActive: '2023-11-10 09:15:08', current: false }
]

// Password policy requirements
const passwordPolicies = [
  { description: 'settings.security.passwordPolicy.minLength', enabled: true },
  { description: 'settings.security.passwordPolicy.upperCase', enabled: true },
  { description: 'settings.security.passwordPolicy.lowerCase', enabled: true },
  { description: 'settings.security.passwordPolicy.numbers', enabled: true },
  { description: 'settings.security.passwordPolicy.special', enabled: false }
]

// Methods
const loadSettings = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Here you would call your API to get user settings
    // For now, we're using the default values defined above
    setTimeout(() => {
      // Simulate loading settings from an API
      loading.value = false
    }, 500)
  } catch (err) {
    console.error('Error loading settings:', err)
    error.value = t('settings.loadError')
    loading.value = false
  }
}

const saveSettings = async () => {
  isSaving.value = true
  
  try {
    // Here you would call your API to save user settings
    await new Promise(resolve => setTimeout(resolve, 800)) // Simulate API call
    toast.success(t('settings.saveSuccess'))
  } catch (err) {
    console.error('Error saving settings:', err)
    toast.error(t('settings.saveError'))
  } finally {
    isSaving.value = false
  }
}

const setLanguage = (lang: string) => {
  locale.value = lang as any
  settings.value.language = lang
}

const setTheme = (theme: string) => {
  settings.value.theme = theme
  // Here you would apply the theme to the application
}

const verifyTwoFactor = () => {
  if (verificationCode.value.length === 6) {
    // Here you would verify the code with your API
    toast.success(t('settings.security.twoFactor.success'))
    verificationCode.value = ''
  } else {
    toast.error(t('settings.security.twoFactor.error'))
  }
}

const logoutSession = (sessionId: number) => {
  // Here you would call your API to logout the specific session
  toast.success(t('settings.security.sessions.terminatedSuccess'))
}

const logoutAllSessions = () => {
  // Here you would call your API to logout all other sessions
  toast.success(t('settings.security.sessions.logoutAllSuccess'))
}

const testEmailConfig = () => {
  // Here you would call your API to test the email configuration
  toast.success(t('settings.system.emailConfig.testSuccess'))
}

// Lifecycle
onMounted(async () => {
  if (!authUser.value) {
    await checkAuth()
  }
  loadSettings()
})
</script> 