<template>
  <div class="bg-white px-6 py-4 flex items-center justify-between border-t border-slate-200 rounded-b-lg">
    <div class="flex-1 flex justify-between sm:hidden">
      <!-- Mobile pagination -->
      <button
        @click="$emit('prev')"
        :disabled="!hasPrev"
        :class="[
          'relative inline-flex items-center px-4 py-2 border rounded-lg text-sm font-medium transition-colors',
          hasPrev
            ? 'text-slate-700 bg-white border-slate-300 hover:bg-slate-50 hover:border-slate-400'
            : 'text-slate-400 bg-slate-50 border-slate-200 cursor-not-allowed'
        ]"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        {{ $t('pagination.previous') }}
      </button>
      <button
        @click="$emit('next')"
        :disabled="!hasNext"
        :class="[
          'relative inline-flex items-center px-4 py-2 border rounded-lg text-sm font-medium transition-colors',
          hasNext
            ? 'text-slate-700 bg-white border-slate-300 hover:bg-slate-50 hover:border-slate-400'
            : 'text-slate-400 bg-slate-50 border-slate-200 cursor-not-allowed'
        ]"
      >
        {{ $t('pagination.next') }}
        <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
    
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
      <!-- Results info -->
      <div class="flex items-center space-x-2">
        <div class="px-3 py-1 bg-slate-100 rounded-lg">
          <p class="text-sm font-medium text-slate-700">
            {{ $t('pagination.showing', { from: startItem, to: endItem, total: total }) }}
          </p>
        </div>
        <div class="text-sm text-slate-500">
          {{ $t('pagination.page', { current: currentPage, total: totalPages }) }}
        </div>
      </div>
      
      <!-- Desktop pagination -->
      <div class="flex items-center space-x-1">
        <nav class="relative z-0 inline-flex items-center space-x-1" aria-label="Pagination">
          <!-- Previous button -->
          <button
            @click="$emit('prev')"
            :disabled="!hasPrev"
            :class="[
              'relative inline-flex items-center px-3 py-2 rounded-lg border text-sm font-medium transition-all duration-200',
              hasPrev
                ? 'text-slate-700 bg-white border-slate-300 hover:bg-slate-50 hover:border-slate-400 hover:shadow-sm'
                : 'text-slate-400 bg-slate-50 border-slate-200 cursor-not-allowed'
            ]"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            <span class="hidden sm:inline">{{ $t('pagination.previous') }}</span>
          </button>
          
          <!-- Page numbers -->
          <template v-for="pageNum in visiblePages" :key="pageNum">
            <button
              v-if="typeof pageNum === 'number'"
              @click="$emit('goto', pageNum)"
              :class="[
                'relative inline-flex items-center px-4 py-2 rounded-lg border text-sm font-medium transition-all duration-200',
                pageNum === currentPage
                  ? 'z-10 bg-indigo-600 border-indigo-600 text-white shadow-lg transform scale-110'
                  : 'bg-white border-slate-300 text-slate-700 hover:bg-slate-50 hover:border-slate-400 hover:shadow-sm'
              ]"
            >
              {{ pageNum }}
            </button>
            <span
              v-else
              class="relative inline-flex items-center px-3 py-2 text-sm font-medium text-slate-500"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z"/>
              </svg>
            </span>
          </template>
          
          <!-- Next button -->
          <button
            @click="$emit('next')"
            :disabled="!hasNext"
            :class="[
              'relative inline-flex items-center px-3 py-2 rounded-lg border text-sm font-medium transition-all duration-200',
              hasNext
                ? 'text-slate-700 bg-white border-slate-300 hover:bg-slate-50 hover:border-slate-400 hover:shadow-sm'
                : 'text-slate-400 bg-slate-50 border-slate-200 cursor-not-allowed'
            ]"
          >
            <span class="hidden sm:inline">{{ $t('pagination.next') }}</span>
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  currentPage: number
  totalPages: number
  total: number
  pageSize: number
}

const props = defineProps<Props>()

defineEmits<{
  prev: []
  next: []
  goto: [page: number]
}>()

const hasPrev = computed(() => props.currentPage > 1)
const hasNext = computed(() => props.currentPage < props.totalPages)

const startItem = computed(() => {
  return Math.min(((props.currentPage - 1) * props.pageSize) + 1, props.total)
})

const endItem = computed(() => {
  return Math.min(props.currentPage * props.pageSize, props.total)
})

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const maxVisible = 7
  const current = props.currentPage
  const total = props.totalPages

  if (total <= maxVisible) {
    // Show all pages if total is small
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // Always show first page
    pages.push(1)
    
    if (current <= 4) {
      // Near beginning
      for (let i = 2; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      // Near end
      pages.push('...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      // In middle
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    }
  }

  return pages
})
</script>
