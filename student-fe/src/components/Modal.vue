<template>
  <Teleport to="body">
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click="handleBackdropClick"
    >
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-opacity-75 backdrop-blur-xl transition-opacity"></div>

      <!-- Modal content -->
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div
          ref="modalRef"
          :class="[
            'relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 w-full',
            sizeClasses
          ]"
        >
          <!-- Header -->
          <div v-if="title || $slots.header" class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:text-left flex-1">
                <slot name="header">
                  <h3 class="text-lg font-medium leading-6 text-gray-900">
                    {{ title }}
                  </h3>
                </slot>
              </div>
              
              <!-- Close button -->
              <button
                v-if="closable"
                @click="close"
                class="ml-4 text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md p-1"
              >
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Body -->
          <div class="bg-white px-4 pb-4 sm:p-6">
            <slot></slot>
          </div>
          
          <!-- Footer -->
          <div v-if="$slots.footer" class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

interface Props {
  modelValue: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  closable?: boolean
  closeOnBackdrop?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  closable: true,
  closeOnBackdrop: true
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  close: []
}>()

const modalRef = ref<HTMLElement>()

const sizeClasses = {
  sm: 'sm:max-w-sm',
  md: 'sm:max-w-lg',
  lg: 'sm:max-w-2xl',
  xl: 'sm:max-w-4xl'
}[props.size]

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleBackdropClick = (event: MouseEvent) => {
  if (props.closeOnBackdrop && modalRef.value && !modalRef.value.contains(event.target as Node)) {
    close()
  }
}

// Focus management
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    nextTick(() => {
      // Focus first focusable element
      const focusable = modalRef.value?.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])') as HTMLElement
      focusable?.focus()
    })
  }
})

// Handle escape key
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && props.modelValue && props.closable) {
    close()
  }
}

// Add/remove event listeners
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    document.addEventListener('keydown', handleKeydown)
    document.body.style.overflow = 'hidden'
  } else {
    document.removeEventListener('keydown', handleKeydown)
    document.body.style.overflow = ''
  }
})
</script>
