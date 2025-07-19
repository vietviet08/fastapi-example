import { createRouter, createWebHistory } from 'vue-router'
import StudentsView from '@/views/StudentsView.vue'
import StudentDetailView from '@/views/StudentDetailView.vue'
import CreateStudentView from '@/views/CreateStudentView.vue'
import EditStudentView from '@/views/EditStudentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'students',
      component: StudentsView,
      meta: { title: 'Danh sách sinh viên' }
    },
    {
      path: '/students/create',
      name: 'create-student',
      component: CreateStudentView,
      meta: { title: 'Thêm sinh viên mới' }
    },
    {
      path: '/students/:id',
      name: 'student-detail',
      component: StudentDetailView,
      meta: { title: 'Chi tiết sinh viên' }
    },
    {
      path: '/students/:id/edit',
      name: 'edit-student',
      component: EditStudentView,
      meta: { title: 'Chỉnh sửa sinh viên' }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

// Update document title
router.beforeEach((to) => {
  document.title = to.meta.title as string || 'Student Management'
})

export default router
