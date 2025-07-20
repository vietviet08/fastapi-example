<template>
  <div
    class="group bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 border border-slate-200 hover:border-slate-300 overflow-hidden">
    <!-- Header với avatar và status -->
    <div class="p-6 pb-4">
      <div class="flex items-start justify-between mb-4">
        <div class="flex items-center space-x-3">
          <div class="relative">
            <div
              class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-lg shadow-md">
              {{ getInitials(student.first_name, student.last_name) }}
            </div>
            <div class="absolute -bottom-1 -right-1 w-5 h-5 rounded-full border-2 border-white shadow-sm"
              :class="student.is_active ? 'bg-green-500' : 'bg-red-500'">
            </div>
          </div>
          <div>
            <h3 class="font-semibold text-lg text-slate-900 group-hover:text-indigo-600 transition-colors">
              {{ student.last_name }} {{ student.first_name }}
            </h3>
            <p class="text-sm font-medium text-indigo-600 bg-indigo-50 px-2 py-1 rounded-md inline-block">
              {{ student.student_id }}
            </p>
          </div>
        </div>

        <!-- Status Badge -->
        <span :class="student.is_active
          ? 'bg-green-100 text-green-800 border-green-200'
          : 'bg-red-100 text-red-800 border-red-200'"
          class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border">
          <div class="w-2 h-2 rounded-full mr-2" :class="student.is_active ? 'bg-green-500' : 'bg-red-500'">
          </div>
          {{ student.is_active ? $t('students.status.active') : $t('students.status.inactive') }}
        </span>
      </div>

      <!-- Thông tin liên hệ -->
      <div class="space-y-3 text-sm text-slate-600">
        <div class="flex items-center text-sm text-slate-600 hover:text-slate-800 transition-colors">
          <div
            class="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center mr-3 group-hover:bg-slate-200 transition-colors">
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <span class="truncate font-medium">{{ student.email }}</span>
        </div>

        <div v-if="student.phone"
          class="flex items-center text-sm text-slate-600 hover:text-slate-800 transition-colors">
          <div
            class="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center mr-3 group-hover:bg-slate-200 transition-colors">
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
          </div>
          <span class="font-medium">{{ student.phone }}</span>
        </div>

        <div v-if="student.date_of_birth"
          class="flex items-center text-sm text-slate-600 hover:text-slate-800 transition-colors">
          <div
            class="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center mr-3 group-hover:bg-slate-200 transition-colors">
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <span class="font-medium">{{ formatDate(student.date_of_birth) }}</span>
        </div>

        <div v-if="student.address"
          class="flex items-center text-sm text-slate-600 hover:text-slate-800 transition-colors">
          <div
            class="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center mr-3 group-hover:bg-slate-200 transition-colors">
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 11a2 2 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <span class="font-medium">{{ student.address }}</span>
        </div>

      </div>
    </div>



    <!-- Actions -->
    <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
      <div class="text-xs text-slate-500 font-medium">
        {{ formatDate(student.created_at, true) }}
      </div>

      <div class="flex space-x-1">
        <button @click="$emit('view', student)"
          class="inline-flex items-center px-3 py-2 text-sm font-medium text-indigo-600 bg-indigo-50 rounded-lg hover:bg-indigo-100 hover:text-indigo-700 transition-all duration-200 transform hover:scale-105"
          :title="$t('common.view')">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          <span class="ml-1.5">{{ $t('common.view') }}</span>
        </button>

        <button @click="$emit('edit', student)"
          class="inline-flex items-center px-3 py-2 text-sm font-medium text-amber-600 bg-amber-50 rounded-lg hover:bg-amber-100 hover:text-amber-700 transition-all duration-200 transform hover:scale-105"
          :title="$t('common.edit')">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          <span class="ml-1.5">{{ $t('common.edit') }}</span>
        </button>

        <button @click="$emit('delete', student)"
          class="inline-flex items-center px-3 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 hover:text-red-700 transition-all duration-200 transform hover:scale-105"
          :title="$t('common.delete')">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          <span class="ml-1.5">{{ $t('common.delete') }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { format, parseISO } from 'date-fns'
import { vi } from 'date-fns/locale'
import type { Student } from '../types/student'

interface Props {
  student: Student
}

defineProps<Props>()

defineEmits<{
  view: [student: Student]
  edit: [student: Student]
  delete: [student: Student]
}>()

const getInitials = (firstName: string, lastName: string): string => {
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase()
}

const formatDate = (dateString: string, includeTime = false): string => {
  try {
    const date = parseISO(dateString)
    if (includeTime) {
      return format(date, 'dd/MM/yyyy HH:mm', { locale: vi })
    }
    return format(date, 'dd/MM/yyyy', { locale: vi })
  } catch (error) {
    return dateString
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
