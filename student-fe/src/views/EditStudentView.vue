<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center space-x-4 mb-4">
          <router-link
            :to="`/students/${route.params.id}`"
            class="inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700"
          >
            <svg class="mr-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            Quay lại chi tiết
          </router-link>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">Chỉnh sửa sinh viên</h1>
        <p v-if="currentStudent" class="mt-2 text-gray-600">
          Cập nhật thông tin cho {{ currentStudent.last_name }} {{ currentStudent.first_name }}
        </p>
      </div>

      <!-- Loading initial data -->
      <div v-if="loadingStudent" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">Đang tải thông tin sinh viên...</span>
      </div>

      <!-- Error loading student -->
      <div
        v-else-if="error && !currentStudent"
        class="mb-6 rounded-md bg-red-50 p-4"
      >
        <div class="flex">
          <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
          </svg>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Không thể tải thông tin sinh viên</h3>
            <div class="mt-2 text-sm text-red-700">{{ error }}</div>
          </div>
        </div>
      </div>

      <template v-else-if="currentStudent">
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
              <h3 class="text-sm font-medium text-green-800">Cập nhật thành công!</h3>
              <div class="mt-2 text-sm text-green-700">Thông tin sinh viên đã được cập nhật.</div>
            </div>
          </div>
        </div>

        <!-- Update Error Alert -->
        <div
          v-if="updateError"
          class="mb-6 rounded-md bg-red-50 p-4"
        >
          <div class="flex">
            <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Có lỗi xảy ra khi cập nhật</h3>
              <div class="mt-2 text-sm text-red-700">{{ updateError }}</div>
            </div>
          </div>
        </div>

        <!-- Form -->
        <div class="bg-white rounded-lg shadow">
          <div class="p-6">
            <StudentForm
              :initial-data="currentStudent"
              :loading="loadingUpdate"
              :is-edit="true"
              @submit="handleSubmit"
              @cancel="handleCancel"
            />
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStudents } from '../composables/useStudents'
import StudentForm from '../components/StudentForm.vue'
import type { StudentUpdate } from '../types/student'

const route = useRoute()
const router = useRouter()

const { loading, error, currentStudent, fetchStudent, updateStudent } = useStudents()
const showSuccess = ref(false)
const updateError = ref<string | null>(null)
const loadingUpdate = ref(false)

// Separate loading states
const loadingStudent = computed(() => loading.value && !currentStudent.value)

const handleSubmit = async (studentData: StudentUpdate) => {
  if (!currentStudent.value) return
  
  try {
    loadingUpdate.value = true
    updateError.value = null
    
    await updateStudent(currentStudent.value.id, studentData)
    showSuccess.value = true
    
    // Hide success message after 3 seconds
    setTimeout(() => {
      showSuccess.value = false
    }, 3000)
  } catch (err) {
    updateError.value = err instanceof Error ? err.message : 'Có lỗi xảy ra khi cập nhật'
    console.error('Failed to update student:', err)
  } finally {
    loadingUpdate.value = false
  }
}

const handleCancel = () => {
  router.push(`/students/${route.params.id}`)
}

onMounted(async () => {
  const studentId = Number(route.params.id)
  if (studentId) {
    try {
      await fetchStudent(studentId)
    } catch (err) {
      // Error is handled by composable
    }
  }
})
</script>
