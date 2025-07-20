<template>
  <div class="relative">
    <button
      @click="isOpen = !isOpen"
      class="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-md transition-colors"
    >
      <span class="text-lg">{{ currentFlag }}</span>
      <span class="hidden sm:block">{{ getCurrentLanguageName() }}</span>
      <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': isOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <div 
      v-if="isOpen"
      class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50"
      @click.stop
    >
      <div class="py-1">
        <button
          v-for="language in availableLanguages"
          :key="language.code"
          @click="selectLanguage(language.code as 'en' | 'vi' | 'ja')"
          class="flex items-center w-full px-4 py-2 text-sm text-slate-700 hover:bg-slate-100 transition-colors"
          :class="{
            'bg-indigo-50 text-indigo-700': currentLanguage === language.code
          }"
        >
          <span class="text-lg mr-3">{{ language.flag }}</span>
          <span>{{ language.name }}</span>
          <svg
            v-if="currentLanguage === language.code"
            class="w-4 h-4 ml-auto text-indigo-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Overlay to close dropdown -->
    <div
      v-if="isOpen"
      class="fixed inset-0 z-40"
      @click="isOpen = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useLanguage } from '@/composables/useLanguage'

const { currentLanguage, availableLanguages, setLanguage, getCurrentLanguageName } = useLanguage()

const isOpen = ref(false)

const currentFlag = computed(() => {
  const current = availableLanguages.find(lang => lang.code === currentLanguage.value)
  return current?.flag || '🇺🇸'
})

const selectLanguage = (code: 'en' | 'vi' | 'ja') => {
  setLanguage(code)
  isOpen.value = false
}

// Close dropdown on escape key
const handleEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
})
</script>
