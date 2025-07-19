import axios from 'axios'
import type { Student, StudentCreate, StudentUpdate, StudentListResponse } from '@/types/student'

const API_BASE_URL = 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data)
    
    if (error.response?.data?.detail) {
      // Handle validation errors
      if (Array.isArray(error.response.data.detail)) {
        const messages = error.response.data.detail.map((err: any) => 
          `${err.loc?.join(' → ') || 'Field'}: ${err.msg}`
        ).join(', ')
        throw new Error(messages)
      } else if (typeof error.response.data.detail === 'string') {
        throw new Error(error.response.data.detail)
      } else {
        throw new Error('Validation error')
      }
    } else if (error.message) {
      throw new Error(error.message)
    } else {
      throw new Error('Đã xảy ra lỗi không xác định')
    }
  }
)

export const studentApi = {
  // Lấy danh sách sinh viên
  getStudents: async (params?: {
    page?: number
    size?: number
    search?: string
  }): Promise<StudentListResponse> => {
    const response = await api.get('/students/', { params })
    return response.data
  },

  // Lấy thông tin sinh viên theo ID
  getStudent: async (id: number): Promise<Student> => {
    const response = await api.get(`/students/${id}`)
    return response.data
  },

  // Tạo sinh viên mới
  createStudent: async (student: StudentCreate): Promise<Student> => {
    const response = await api.post('/students/', student)
    return response.data
  },

  // Cập nhật sinh viên
  updateStudent: async (id: number, student: StudentUpdate): Promise<Student> => {
    const response = await api.put(`/students/${id}`, student)
    return response.data
  },

  // Xóa sinh viên
  deleteStudent: async (id: number, hardDelete = false): Promise<void> => {
    await api.delete(`/students/${id}`, {
      params: { hard_delete: hardDelete }
    })
  }
}

export default api
