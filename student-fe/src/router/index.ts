import { createRouter, createWebHistory } from 'vue-router'
import StudentsView from '@/views/StudentsView.vue'
import StudentDetailView from '@/views/StudentDetailView.vue'
import CreateStudentView from '@/views/CreateStudentView.vue'
import EditStudentView from '@/views/EditStudentView.vue'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { title: 'Login', requiresAuth: false }
    },
    {
      path: '/',
      redirect: '/students'
    },
    {
      path: '/students',
      name: 'students',
      component: StudentsView,
      meta: { title: 'Danh sách sinh viên', requiresAuth: true }
    },
    {
      path: '/students/create',
      name: 'create-student',
      component: CreateStudentView,
      meta: { title: 'Thêm sinh viên mới', requiresAuth: true }
    },
    {
      path: '/students/:id',
      name: 'student-detail',
      component: StudentDetailView,
      meta: { title: 'Chi tiết sinh viên', requiresAuth: true }
    },
    {
      path: '/students/:id/edit',
      name: 'edit-student',
      component: EditStudentView,
      meta: { title: 'Chỉnh sửa sinh viên', requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/students'
    }
  ]
})

// Auth guard
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('authToken')
  const requiresAuth = to.meta.requiresAuth !== false

  // Update document title
  document.title = to.meta.title as string || 'Student Management'

  if (requiresAuth && !token) {
    // Redirect to login if authentication required but not logged in
    next('/login')
  } else if (to.path === '/login' && token) {
    // Redirect to students if already logged in and trying to access login
    next('/students')
  } else {
    next()
  }
})

export default router
