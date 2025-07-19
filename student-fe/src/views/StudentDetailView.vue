<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
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
            Quay lại danh sách
          </router-link>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">Chi tiết sinh viên</h1>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">Đang tải thông tin sinh viên...</span>
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="rounded-md bg-red-50 p-4"
      >
        <div class="flex">
          <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
          </svg>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Không thể tải thông tin</h3>
            <div class="mt-2 text-sm text-red-700">{{ error }}</div>
          </div>
        </div>
      </div>

      <!-- Student Details -->
      <div v-else-if="currentStudent" class="space-y-6">
        <!-- Main Info Card -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <!-- Header with avatar and status -->
          <div class="px-6 py-8 bg-gradient-to-r from-blue-600 to-purple-600">
            <div class="flex items-center space-x-6">
              <div class="w-20 h-20 bg-white bg-opacity-20 rounded-full flex items-center justify-center text-white font-bold text-2xl">
                {{ getInitials(currentStudent.first_name, currentStudent.last_name) }}
              </div>
              <div class="text-white">
                <h2 class="text-2xl font-bold">
                  {{ currentStudent.last_name }} {{ currentStudent.first_name }}
                </h2>
                <p class="text-blue-100 text-lg">{{ currentStudent.student_id }}</p>
                <span
                  :class="currentStudent.is_active 
                    ? 'bg-green-500 text-white' 
                    : 'bg-red-500 text-white'"
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium mt-2"
                >
                  {{ currentStudent.is_active ? 'Hoạt động' : 'Tạm ngưng' }}
                </span>
              </div>
            </div>
            
            <!-- Action buttons -->
            <div class="mt-6 flex space-x-3">
              <router-link
                :to="`/students/${currentStudent.id}/edit`"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                Chỉnh sửa
              </router-link>
              
              <button
                @click="confirmDelete"
                class="inline-flex items-center px-4 py-2 border border-white text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                Xóa sinh viên
              </button>
            </div>
          </div>
          
          <!-- Details -->
          <div class="px-6 py-6">
            <dl class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Email -->
              <div>
                <dt class="text-sm font-medium text-gray-500 flex items-center">
                  <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  Email
                </dt>
                <dd class="mt-1 text-sm text-gray-900">
                  <a :href="`mailto:${currentStudent.email}`" class="text-blue-600 hover:text-blue-800">
                    {{ currentStudent.email }}
                  </a>
                </dd>
              </div>

              <!-- Phone -->
              <div v-if="currentStudent.phone">
                <dt class="text-sm font-medium text-gray-500 flex items-center">
                  <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                  Số điện thoại
                </dt>
                <dd class="mt-1 text-sm text-gray-900">
                  <a :href="`tel:${currentStudent.phone}`" class="text-blue-600 hover:text-blue-800">
                    {{ currentStudent.phone }}
                  </a>
                </dd>
              </div>

              <!-- Date of Birth -->
              <div v-if="currentStudent.date_of_birth">
                <dt class="text-sm font-medium text-gray-500 flex items-center">
                  <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  Ngày sinh
                </dt>
                <dd class="mt-1 text-sm text-gray-900">{{ formatDate(currentStudent.date_of_birth) }}</dd>
              </div>

              <!-- Created At -->
              <div>
                <dt class="text-sm font-medium text-gray-500 flex items-center">
                  <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  Ngày tạo
                </dt>
                <dd class="mt-1 text-sm text-gray-900">{{ formatDate(currentStudent.created_at, true) }}</dd>
              </div>

              <!-- Updated At -->
              <div v-if="currentStudent.updated_at">
                <dt class="text-sm font-medium text-gray-500 flex items-center">
                  <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                  Ngày cập nhật
                </dt>
                <dd class="mt-1 text-sm text-gray-900">{{ formatDate(currentStudent.updated_at, true) }}</dd>
              </div>
            </dl>

            <!-- Address -->
            <div v-if="currentStudent.address" class="mt-6 pt-6 border-t border-gray-200">
              <dt class="text-sm font-medium text-gray-500 flex items-center mb-2">
                <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                Địa chỉ
              </dt>
              <dd class="text-sm text-gray-900">{{ currentStudent.address }}</dd>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <Modal
      v-model="showDeleteModal"
      title="Xác nhận xóa"
      size="sm"
    >
      <div class="text-center">
        <svg class="mx-auto mb-4 w-14 h-14 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
        </svg>
        <h3 class="mb-2 text-lg font-semibold text-gray-900">Bạn có chắc chắn?</h3>
        <p class="text-gray-500 mb-4">
          Bạn có muốn xóa sinh viên <strong>{{ currentStudent?.last_name }} {{ currentStudent?.first_name }}</strong> không?
        </p>
        <p class="text-sm text-gray-400 mb-6">Hành động này sẽ vô hiệu hóa tài khoản sinh viên.</p>
      </div>

      <template #footer>
        <div class="flex space-x-3 justify-center">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200"
          >
            Hủy
          </button>
          <button
            @click="handleDelete"
            :disabled="loading"
            class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg border border-red-600 hover:bg-red-700 focus:ring-4 focus:outline-none focus:ring-red-300 disabled:opacity-50"
          >
            {{ loading ? 'Đang xóa...' : 'Xóa' }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { format, parseISO } from 'date-fns'
import { vi } from 'date-fns/locale'
import { useStudents } from '../composables/useStudents'
import Modal from '../components/Modal.vue'

const route = useRoute()
const router = useRouter()

const { loading, error, currentStudent, fetchStudent, deleteStudent } = useStudents()
const showDeleteModal = ref(false)

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

const confirmDelete = () => {
  showDeleteModal.value = true
}

const handleDelete = async () => {
  if (!currentStudent.value) return
  
  try {
    await deleteStudent(currentStudent.value.id)
    router.push('/')
  } catch (err) {
    showDeleteModal.value = false
  }
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
