<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Thông tin cá nhân -->
    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Thông tin cá nhân</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Mã sinh viên -->
        <div>
          <label for="student_id" class="block text-sm font-medium text-gray-700 mb-2">
            Mã sinh viên <span class="text-red-500">*</span>
          </label>
          <input
            id="student_id"
            v-model="formData.student_id"
            type="text"
            required
            :disabled="isEdit"
            :class="[
              'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
              isEdit ? 'bg-gray-50 text-gray-500 cursor-not-allowed' : 'border-gray-300'
            ]"
            placeholder="Nhập mã sinh viên"
          />
        </div>

        <!-- Họ -->
        <div>
          <label for="first_name" class="block text-sm font-medium text-gray-700 mb-2">
            Họ <span class="text-red-500">*</span>
          </label>
          <input
            id="first_name"
            v-model="formData.first_name"
            type="text"
            required
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Nhập họ"
          />
        </div>

        <!-- Tên -->
        <div>
          <label for="last_name" class="block text-sm font-medium text-gray-700 mb-2">
            Tên <span class="text-red-500">*</span>
          </label>
          <input
            id="last_name"
            v-model="formData.last_name"
            type="text"
            required
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Nhập tên"
          />
        </div>

        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            Email <span class="text-red-500">*</span>
          </label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            required
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Nhập email"
          />
        </div>

        <!-- Số điện thoại -->
        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
            Số điện thoại
          </label>
          <input
            id="phone"
            v-model="formData.phone"
            type="tel"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Nhập số điện thoại"
          />
        </div>

        <!-- Ngày sinh -->
        <div>
          <label for="date_of_birth" class="block text-sm font-medium text-gray-700 mb-2">
            Ngày sinh
          </label>
          <input
            id="date_of_birth"
            v-model="formData.date_of_birth"
            type="date"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
      </div>

      <!-- Địa chỉ -->
      <div class="mt-6">
        <label for="address" class="block text-sm font-medium text-gray-700 mb-2">
          Địa chỉ
        </label>
        <textarea
          id="address"
          v-model="formData.address"
          rows="3"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Nhập địa chỉ"
        ></textarea>
      </div>

      <!-- Trạng thái (chỉ hiện khi edit) -->
      <div v-if="isEdit" class="mt-6">
        <label class="flex items-center">
          <input
            v-model="formData.is_active"
            type="checkbox"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
          <span class="ml-2 text-sm text-gray-700">Trạng thái hoạt động</span>
        </label>
      </div>
    </div>

    <!-- Form Actions -->
    <div class="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200">
      <button
        type="button"
        @click="$emit('cancel')"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
      >
        Hủy
      </button>
      
      <button
        type="submit"
        :disabled="loading"
        class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {{ loading ? 'Đang xử lý...' : (isEdit ? 'Cập nhật' : 'Tạo mới') }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { Student, StudentCreate, StudentUpdate } from '../types/student'

interface Props {
  initialData?: Student | null
  loading?: boolean
  isEdit?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  initialData: null,
  loading: false,
  isEdit: false
})

const emit = defineEmits<{
  submit: [data: StudentCreate | StudentUpdate]
  cancel: []
}>()

const formData = reactive({
  student_id: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: '',
  address: '',
  is_active: true
})

// Watch for initial data changes
watch(() => props.initialData, (student) => {
  if (student) {
    formData.student_id = student.student_id
    formData.first_name = student.first_name
    formData.last_name = student.last_name
    formData.email = student.email
    formData.phone = student.phone || ''
    formData.date_of_birth = student.date_of_birth ? student.date_of_birth.split('T')[0] : ''
    formData.address = student.address || ''
    formData.is_active = student.is_active
  }
}, { immediate: true })

const handleSubmit = () => {
  const submitData = {
    ...formData,
    phone: formData.phone || undefined,
    date_of_birth: formData.date_of_birth || undefined,
    address: formData.address || undefined
  }

  if (props.isEdit) {
    // For edit, exclude student_id
    const { student_id, ...updateData } = submitData
    emit('submit', updateData)
  } else {
    emit('submit', submitData as StudentCreate)
  }
}
</script>
