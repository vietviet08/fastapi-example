<template>
  <div class="relative">
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
    </div>
    <input
      v-model="searchQuery"
      @input="handleInput"
      @keyup.enter="handleSearch"
      type="text"
      :placeholder="placeholder"
      class="block w-full pl-10 pr-12 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
    />
    <div class="absolute inset-y-0 right-0 flex items-center">
      <!-- Clear button -->
      <button
        v-if="searchQuery"
        @click="clearSearch"
        type="button"
        class="p-1 mr-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-colors"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
      
      <!-- Search button -->
      <button
        @click="handleSearch"
        type="button"
        class="p-1 mr-2 text-blue-600 hover:text-blue-800 rounded-full hover:bg-blue-50 transition-colors"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  modelValue?: string
  placeholder?: string
  debounceMs?: number
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: 'Tìm kiếm sinh viên...',
  debounceMs: 300
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  search: [query: string]
  clear: []
}>()

const searchQuery = ref(props.modelValue)
let debounceTimer: number | null = null

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  searchQuery.value = newValue
})

// Watch for internal changes and emit
watch(searchQuery, (newValue) => {
  emit('update:modelValue', newValue)
})

const handleInput = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  debounceTimer = setTimeout(() => {
    emit('search', searchQuery.value)
  }, props.debounceMs)
}

const handleSearch = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  emit('search', searchQuery.value)
}

const clearSearch = () => {
  searchQuery.value = ''
  emit('clear')
  emit('search', '')
}
</script>
