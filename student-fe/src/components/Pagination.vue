<template>
  <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
    <div class="flex-1 flex justify-between sm:hidden">
      <!-- Mobile pagination -->
      <button
        @click="$emit('prev')"
        :disabled="!hasPrev"
        :class="[
          'relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md',
          hasPrev
            ? 'text-gray-700 bg-white hover:bg-gray-50'
            : 'text-gray-400 bg-gray-100 cursor-not-allowed'
        ]"
      >
        Trước
      </button>
      <button
        @click="$emit('next')"
        :disabled="!hasNext"
        :class="[
          'ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md',
          hasNext
            ? 'text-gray-700 bg-white hover:bg-gray-50'
            : 'text-gray-400 bg-gray-100 cursor-not-allowed'
        ]"
      >
        Sau
      </button>
    </div>
    
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
      <!-- Results info -->
      <div>
        <p class="text-sm text-gray-700">
          Hiển thị
          <span class="font-medium">{{ startItem }}</span>
          đến
          <span class="font-medium">{{ endItem }}</span>
          trong tổng số
          <span class="font-medium">{{ total }}</span>
          kết quả
        </p>
      </div>
      
      <!-- Desktop pagination -->
      <div>
        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
          <!-- Previous button -->
          <button
            @click="$emit('prev')"
            :disabled="!hasPrev"
            :class="[
              'relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 text-sm font-medium',
              hasPrev
                ? 'text-gray-500 bg-white hover:bg-gray-50'
                : 'text-gray-300 bg-gray-100 cursor-not-allowed'
            ]"
          >
            <span class="sr-only">Trang trước</span>
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </button>
          
          <!-- Page numbers -->
          <template v-for="pageNum in visiblePages" :key="pageNum">
            <button
              v-if="typeof pageNum === 'number'"
              @click="$emit('goto', pageNum)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                pageNum === currentPage
                  ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                  : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
              ]"
            >
              {{ pageNum }}
            </button>
            <span
              v-else
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
            >
              ...
            </span>
          </template>
          
          <!-- Next button -->
          <button
            @click="$emit('next')"
            :disabled="!hasNext"
            :class="[
              'relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 text-sm font-medium',
              hasNext
                ? 'text-gray-500 bg-white hover:bg-gray-50'
                : 'text-gray-300 bg-gray-100 cursor-not-allowed'
            ]"
          >
            <span class="sr-only">Trang sau</span>
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
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
