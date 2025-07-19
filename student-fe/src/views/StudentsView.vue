<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Quản lý sinh viên</h1>
        <p class="mt-2 text-gray-600">Danh sách tất cả sinh viên trong hệ thống</p>
      </div>

      <!-- Actions Bar -->
      <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
        <!-- Search -->
        <div class="flex-1 max-w-md">
          <SearchBar
            v-model="searchQuery"
            @search="handleSearch"
            placeholder="Tìm kiếm theo tên, mã SV, email..."
          />
        </div>
        
        <!-- Actions -->
        <div class="flex items-center space-x-3">
          <!-- Refresh button -->
          <button
            @click="refreshStudents"
            :disabled="loading"
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Làm mới
          </button>
          
          <!-- Add student button -->
          <router-link
            to="/students/create"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm sinh viên
          </router-link>
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
            <h3 class="text-sm font-medium text-red-800">Có lỗi xảy ra</h3>
            <div class="mt-2 text-sm text-red-700">{{ error }}</div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">Đang tải dữ liệu...</span>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="!hasStudents && !loading"
        class="text-center py-12"
      >
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">Không có sinh viên</h3>
        <p class="mt-1 text-sm text-gray-500">
          {{ searchQuery ? 'Không tìm thấy sinh viên nào phù hợp.' : 'Hãy bắt đầu bằng cách thêm sinh viên mới.' }}
        </p>
        <div class="mt-6">
          <router-link
            to="/students/create"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm sinh viên đầu tiên
          </router-link>
        </div>
      </div>

      <!-- Students Grid -->
      <div
        v-else-if="hasStudents"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8"
      >
        <StudentCard
          v-for="student in students"
          :key="student.id"
          :student="student"
          @view="viewStudent"
          @edit="editStudent"
          @delete="confirmDeleteStudent"
        />
      </div>

      <!-- Pagination -->
      <div v-if="hasStudents && pagination.pages > 1">
        <Pagination
          :current-page="pagination.page"
          :total-pages="pagination.pages"
          :total="pagination.total"
          :page-size="pagination.size"
          @prev="prevPage"
          @next="nextPage"
          @goto="goToPage"
        />
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
          Bạn có muốn xóa sinh viên <strong>{{ studentToDelete?.last_name }} {{ studentToDelete?.first_name }}</strong> không?
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
            @click="handleDeleteStudent"
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
import { useRouter } from 'vue-router'
import { useStudents } from '../composables/useStudents'
import StudentCard from '../components/StudentCard.vue'
import SearchBar from '../components/SearchBar.vue'
import Pagination from '../components/Pagination.vue'
import Modal from '../components/Modal.vue'
import type { Student } from '../types/student'

const router = useRouter()

const {
  loading,
  error,
  students,
  pagination,
  hasStudents,
  searchQuery,
  fetchStudents,
  searchStudents,
  deleteStudent,
  nextPage,
  prevPage,
  goToPage
} = useStudents()

// Delete modal state
const showDeleteModal = ref(false)
const studentToDelete = ref<Student | null>(null)

// Methods
const refreshStudents = async () => {
  await fetchStudents(pagination.page, pagination.size, searchQuery.value)
}

const handleSearch = async (query: string) => {
  await searchStudents(query)
}

const viewStudent = (student: Student) => {
  router.push(`/students/${student.id}`)
}

const editStudent = (student: Student) => {
  router.push(`/students/${student.id}/edit`)
}

const confirmDeleteStudent = (student: Student) => {
  studentToDelete.value = student
  showDeleteModal.value = true
}

const handleDeleteStudent = async () => {
  if (!studentToDelete.value) return
  
  try {
    await deleteStudent(studentToDelete.value.id)
    showDeleteModal.value = false
    studentToDelete.value = null
  } catch (err) {
    // Error is handled by the composable
  }
}

// Initialize
onMounted(() => {
  fetchStudents()
})
</script>
