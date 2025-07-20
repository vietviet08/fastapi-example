<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white border-b border-slate-200 px-6 py-4 rounded-lg shadow-sm">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div class="mb-4 lg:mb-0">
          <h1 class="text-2xl font-bold text-slate-900 flex items-center">
            <div class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
            </div>
            {{ $t('students.title') }}
          </h1>
          <p class="text-slate-600 mt-1">{{ $t('students.subtitle') }}</p>
        </div>
        
        <!-- Stats -->
        <div class="flex items-center space-x-6 text-sm text-slate-600">
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>{{ totalStudents }} {{ $t('students.totalStudents') }}</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span>{{ activeStudents }} {{ $t('students.activeStudents') }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Actions -->
    <div class="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <!-- Search Bar -->
        <div class="flex-1 max-w-md">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              @input="handleSearchInput"
              type="text"
              :placeholder="$t('students.searchPlaceholder')"
              class="block w-full pl-10 pr-3 py-3 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
            />
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center space-x-3">
          <!-- Filter Dropdown -->
          <div class="relative">
            <button
              @click="showFilters = !showFilters"
              class="inline-flex items-center px-4 py-3 border border-slate-300 rounded-lg shadow-sm text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.414A1 1 0 013 6.707V4z" />
              </svg>
              <span>{{ $t('students.filter') }}</span>
              <svg class="w-4 h-4 ml-2 transition-transform" :class="{ 'rotate-180': showFilters }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          <!-- Refresh Button -->
          <button
            @click="refreshStudents"
            :disabled="loading"
            class="inline-flex items-center px-4 py-3 border border-slate-300 rounded-lg shadow-sm text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ $t('students.refresh') }}
          </button>

          <!-- Add Student Button -->
          <router-link
            to="/students/create"
            class="inline-flex items-center px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-lg shadow-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transform transition-all duration-200 hover:scale-105"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            {{ $t('students.addStudent') }}
          </router-link>
        </div>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <div class="flex items-center space-x-3">
        <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="text-sm font-medium text-red-800">Error occurred</h3>
          <p class="text-sm text-red-700 mt-1">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg shadow-sm border border-slate-200 p-12">
      <div class="flex flex-col items-center justify-center space-y-4">
        <div class="animate-spin rounded-full h-12 w-12 border-2 border-indigo-500 border-t-transparent"></div>
        <p class="text-slate-600 font-medium">Loading students...</p>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!hasStudents && !loading" class="bg-white rounded-lg shadow-sm border border-slate-200 p-12">
      <div class="text-center">
        <div class="w-24 h-24 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-12 h-12 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-slate-900 mb-2">No students found</h3>
        <p class="text-slate-600 mb-6 max-w-md mx-auto">
          {{ searchQuery ? 'No students match your search criteria. Try adjusting your search terms.' : 'Get started by adding your first student to the system.' }}
        </p>
        <router-link
          to="/students/create"
          class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-lg shadow-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transform transition-all duration-200 hover:scale-105"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          {{ searchQuery ? 'Add New Student' : 'Add First Student' }}
        </router-link>
      </div>
    </div>

    <!-- Students Grid -->
    <div v-else-if="hasStudents" class="space-y-6">
      <!-- Students Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
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
      <div v-if="pagination.pages > 1" class="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
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
      :title="$t('students.modal.confirmDeletion')"
      size="md"
    >
      <div class="space-y-6">
        <!-- Warning Icon & Header -->
        <div class="flex items-center justify-center">
          <div class="relative">
            <div class="w-20 h-20 bg-gradient-to-br from-red-100 to-red-200 rounded-full flex items-center justify-center">
              <div class="absolute inset-0 bg-red-500/10 rounded-full animate-pulse"></div>
              <svg class="w-10 h-10 text-red-600 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="text-center space-y-4">
          <div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">{{ $t('students.modal.areYouSure') }}</h3>
            <p class="text-slate-600 leading-relaxed">
              {{ $t('students.modal.deleteWarning', { studentName: `${studentToDelete?.first_name} ${studentToDelete?.last_name}` }) }}
            </p>
          </div>

          <!-- Student Info Card -->
          <div v-if="studentToDelete" class="bg-slate-50 border border-slate-200 rounded-lg p-4 mx-auto max-w-sm">
            <div class="flex items-center space-x-3">
              <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                {{ studentToDelete.first_name?.charAt(0) }}{{ studentToDelete.last_name?.charAt(0) }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-slate-900 truncate">
                  {{ studentToDelete.first_name }} {{ studentToDelete.last_name }}
                </p>
                <p class="text-sm text-slate-600 truncate">{{ studentToDelete.student_id }}</p>
                <p class="text-sm text-slate-500 truncate">{{ studentToDelete.email }}</p>
              </div>
            </div>
          </div>

          <!-- Warning Text -->
          <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-sm text-red-800 font-medium mb-2">{{ $t('students.modal.dangerZone') }}</p>
            <p class="text-sm text-red-700">{{ $t('students.modal.deleteConfirmText') }}</p>
          </div>

          <!-- Confirmation Input -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-slate-700 text-left">
              {{ $t('students.modal.typeToConfirm') }}
            </label>
            <input
              v-model="deleteConfirmText"
              type="text"
              :placeholder="$t('students.modal.deletePlaceholder')"
              class="w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
              @keyup.enter="deleteConfirmText === 'DELETE' && handleDeleteStudent()"
            />
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col-reverse sm:flex-row sm:justify-end space-y-3 space-y-reverse sm:space-y-0 sm:space-x-3 pt-4 border-t border-slate-200">
          <button
            @click="cancelDelete"
            class="w-full sm:w-auto px-6 py-3 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200"
          >
            {{ $t('common.cancel') }}
          </button>
          <button
            @click="handleDeleteStudent"
            :disabled="deleteConfirmText !== 'DELETE' || isDeleting"
            class="w-full sm:w-auto px-6 py-3 text-sm font-medium text-white bg-gradient-to-r from-red-600 to-red-700 border border-transparent rounded-lg hover:from-red-700 hover:to-red-800 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
          >
            <div v-if="isDeleting" class="flex items-center justify-center space-x-2">
              <div class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
              <span>{{ $t('common.loading') }}...</span>
            </div>
            <div v-else class="flex items-center justify-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span>{{ $t('students.deleteStudent') }}</span>
            </div>
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useToast } from 'vue-toastification'
import { useStudents } from '../composables/useStudents'
import StudentCard from '../components/StudentCard.vue'
import Pagination from '../components/Pagination.vue'
import Modal from '../components/Modal.vue'
import type { Student } from '../types/student'

const router = useRouter()
const { t } = useI18n()
const toast = useToast()

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

// Additional state
const showDeleteModal = ref(false)
const studentToDelete = ref<Student | null>(null)
const showFilters = ref(false)

// Computed properties
const totalStudents = computed(() => pagination.total)
const activeStudents = computed(() => students.value.filter(s => s.is_active).length)
// Modal states
const deleteConfirmText = ref('')
const isDeleting = ref(false)

// Methods
const handleSearchInput = async (event: Event) => {
  const target = event.target as HTMLInputElement
  searchQuery.value = target.value
  await searchStudents(target.value)
}

const refreshStudents = async () => {
  await fetchStudents(pagination.page, pagination.size, searchQuery.value)
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
  deleteConfirmText.value = ''
}

const cancelDelete = () => {
  showDeleteModal.value = false
  studentToDelete.value = null
  deleteConfirmText.value = ''
  isDeleting.value = false
}

const handleDeleteStudent = async () => {
  if (!studentToDelete.value || deleteConfirmText.value !== 'DELETE') return
  
  isDeleting.value = true
  
  try {
    await deleteStudent(studentToDelete.value.id)
    toast.success(t('students.messages.deleteSuccess'))
    showDeleteModal.value = false
    studentToDelete.value = null
    deleteConfirmText.value = ''
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || t('students.messages.deleteError')
    toast.error(errorMessage)
  } finally {
    isDeleting.value = false
  }
}

// Initialize
onMounted(() => {
  fetchStudents()
})
</script>

<style scoped>
/* Custom animations and styles */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.6s ease-out forwards;
}
</style>
