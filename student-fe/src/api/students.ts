import { apiClient } from '@/api/auth'
import type { Student, StudentCreate, StudentUpdate, StudentListResponse } from '@/types/student'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

// Remove old axios setup since we'll use apiClient from auth
// const api = axios.create({...})

export const studentApi = {
  // Lấy danh sách sinh viên
  getStudents: async (params?: {
    page?: number
    size?: number
    search?: string
  }): Promise<StudentListResponse> => {
    const response = await apiClient.get('/students/', { params })
    return response.data
  },

  // Lấy thông tin sinh viên theo ID
  getStudent: async (id: number): Promise<Student> => {
    const response = await apiClient.get(`/students/${id}`)
    return response.data
  },

  // Tạo sinh viên mới
  createStudent: async (student: StudentCreate): Promise<Student> => {
    const response = await apiClient.post('/students/', student)
    return response.data
  },

  // Cập nhật sinh viên
  updateStudent: async (id: number, student: StudentUpdate): Promise<Student> => {
    const response = await apiClient.put(`/students/${id}`, student)
    return response.data
  },

  // Xóa sinh viên
  deleteStudent: async (id: number, hardDelete = false): Promise<void> => {
    await apiClient.delete(`/students/${id}`, {
      params: { hard_delete: hardDelete }
    })
  }
}

export default apiClient
