import { ref, computed, reactive } from 'vue'
import { studentApi } from '@/api/students'
import type { Student, StudentCreate, StudentUpdate } from '@/types/student'

export function useStudents() {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const students = ref<Student[]>([])
  const currentStudent = ref<Student | null>(null)
  
  const pagination = reactive({
    page: 1,
    size: 10,
    total: 0,
    pages: 0
  })

  const searchQuery = ref('')

  // Computed
  const hasStudents = computed(() => students.value.length > 0)
  const hasPrevPage = computed(() => pagination.page > 1)
  const hasNextPage = computed(() => pagination.page < pagination.pages)

  // Methods
  const fetchStudents = async (page = 1, size = 10, search = '') => {
    try {
      loading.value = true
      error.value = null
      
      const response = await studentApi.getStudents({
        page,
        size,
        search: search || undefined
      })
      
      students.value = response.students
      pagination.page = response.page
      pagination.size = response.size
      pagination.total = response.total
      pagination.pages = response.pages
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Lỗi không xác định'
      console.error('Error fetching students:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchStudent = async (id: number) => {
    try {
      loading.value = true
      error.value = null
      
      const student = await studentApi.getStudent(id)
      currentStudent.value = student
      return student
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Lỗi không xác định'
      console.error('Error fetching student:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createStudent = async (studentData: StudentCreate) => {
    try {
      loading.value = true
      error.value = null
      
      const newStudent = await studentApi.createStudent(studentData)
      
      // Refresh the list
      await fetchStudents(pagination.page, pagination.size, searchQuery.value)
      
      return newStudent
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Lỗi không xác định'
      console.error('Error creating student:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateStudent = async (id: number, studentData: StudentUpdate) => {
    try {
      loading.value = true
      error.value = null
      
      const updatedStudent = await studentApi.updateStudent(id, studentData)
      
      // Update the current student if it's the same one
      if (currentStudent.value?.id === id) {
        currentStudent.value = updatedStudent
      }
      
      // Update in the list
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value[index] = updatedStudent
      }
      
      return updatedStudent
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Lỗi không xác định'
      console.error('Error updating student:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteStudent = async (id: number, hardDelete = false) => {
    try {
      loading.value = true
      error.value = null
      
      await studentApi.deleteStudent(id, hardDelete)
      
      // Remove from list or refresh
      await fetchStudents(pagination.page, pagination.size, searchQuery.value)
      
      // Clear current student if it was deleted
      if (currentStudent.value?.id === id) {
        currentStudent.value = null
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Lỗi không xác định'
      console.error('Error deleting student:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const searchStudents = async (query: string) => {
    searchQuery.value = query
    pagination.page = 1
    await fetchStudents(1, pagination.size, query)
  }

  const nextPage = async () => {
    if (hasNextPage.value) {
      await fetchStudents(pagination.page + 1, pagination.size, searchQuery.value)
    }
  }

  const prevPage = async () => {
    if (hasPrevPage.value) {
      await fetchStudents(pagination.page - 1, pagination.size, searchQuery.value)
    }
  }

  const goToPage = async (page: number) => {
    if (page >= 1 && page <= pagination.pages) {
      await fetchStudents(page, pagination.size, searchQuery.value)
    }
  }

  return {
    // State
    loading,
    error,
    students,
    currentStudent,
    pagination,
    searchQuery,
    
    // Computed
    hasStudents,
    hasPrevPage,
    hasNextPage,
    
    // Methods
    fetchStudents,
    fetchStudent,
    createStudent,
    updateStudent,
    deleteStudent,
    searchStudents,
    nextPage,
    prevPage,
    goToPage
  }
}
