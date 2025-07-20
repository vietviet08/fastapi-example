export interface LoginRequest {
  email: string
  password: string
}

export interface UserResponse {
  id: number
  email: string
  is_active: boolean
  is_admin: boolean
  created_at: string
  updated_at?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: UserResponse
}

export interface APIError {
  detail: string
}
