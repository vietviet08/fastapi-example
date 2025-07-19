export interface Student {
  id: number
  student_id: string
  first_name: string
  last_name: string
  email: string
  phone?: string
  date_of_birth?: string
  address?: string
  is_active: boolean
  created_at: string
  updated_at?: string
}

export interface StudentCreate {
  student_id: string
  first_name: string
  last_name: string
  email: string
  phone?: string
  date_of_birth?: string
  address?: string
}

export interface StudentUpdate {
  first_name?: string
  last_name?: string
  email?: string
  phone?: string
  date_of_birth?: string
  address?: string
  is_active?: boolean
}

export interface StudentListResponse {
  students: Student[]
  total: number
  page: number
  size: number
  pages: number
}

export interface ApiError {
  detail: string
}
