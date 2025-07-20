<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center space-x-4 mb-4">
          <router-link
            to="/"
            class="inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700"
          >
            <svg class="mr-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            {{ $t('common.back') }}
          </router-link>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">{{ $t('students.createStudent') }}</h1>
        <p class="mt-2 text-gray-600">{{ $t('students.createSubtitle') }}</p>
      </div>

      <!-- Success Alert -->
      <div
        v-if="showSuccess"
        class="mb-6 rounded-md bg-green-50 p-4"
      >
        <div class="flex">
          <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-green-800">{{ $t('common.success') }}!</h3>
            <div class="mt-2 text-sm text-green-700">{{ $t('students.createSuccess') }}</div>
          </div>
        </div>
      </div>

      <!-- Error Alert -->
      <div
        v-if="error"
        class="mb-6 rounded-md bg-red-50 p-4"
      >
        <div class="flex">
          <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
          </svg>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">{{ $t('common.error') }}</h3>
            <div class="mt-2 text-sm text-red-700">{{ error }}</div>
          </div>
        </div>
      </div>

      <!-- Form -->
      <div class="bg-white rounded-lg shadow">
        <div class="p-6">
          <StudentForm
            :loading="loading"
            @submit="handleSubmit"
            @cancel="handleCancel"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStudents } from '../composables/useStudents'
import StudentForm from '../components/StudentForm.vue'
import type { StudentCreate, StudentUpdate } from '../types/student'

const router = useRouter()

const { loading, error, createStudent } = useStudents()
const showSuccess = ref(false)

const handleSubmit = async (studentData: StudentCreate | StudentUpdate) => {
  try {
    // Since this is CreateStudentView and isEdit is not passed to StudentForm,
    // we know this will always be StudentCreate with student_id included
    if ('student_id' in studentData) {
      await createStudent(studentData as StudentCreate)
    } else {
      throw new Error('Invalid data: student_id is required for creating a student')
    }
    showSuccess.value = true
    
    // Redirect after success
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (err) {
    // Error is handled by the composable
    console.error('Failed to create student:', err)
  }
}

const handleCancel = () => {
  router.push('/')
}
</script>
