import { createRouter, createWebHistory } from 'vue-router'

import AuthView from '@/views/AuthView.vue'
import AdminView from '@/views/AdminView.vue'
import StudentView from '@/views/StudentView.vue'
import CompanyView from '@/views/CompanyView.vue'

import StudentDashboard from '@/components/student/StudentDashboard.vue'
import StudentProfile from '@/components/student/StudentProfile.vue'

import CompanyDashboard from '@/components/company/CompanyDashboard.vue'
import CompanyProfile from '@/components/company/CompanyProfile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'auth',
      component: AuthView,
      meta: {
        title: 'Login/Register - RecruitX',
      },
    },

    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
    },

    {
      path: '/student',
      name: 'student',
      component: StudentView,
      children: [
        {
          path: '',
          name: 'studentDashboard',
          component: StudentDashboard,
          meta: {
            title: 'Student Dashboard - RecruitX',
          },
        },

        {
          path: 'profile',
          name: 'studentProfile',
          component: StudentProfile,
          meta: {
            title: 'Student Profile - RecruitX',
          },
        },
      ],
    },

    {
      path: '/company',
      name: 'company',
      component: CompanyView,
      children: [
        {
          path: '',
          name: 'companyDashboard',
          component: CompanyDashboard,
          meta: {
            title: 'Company Dashboard - RecruitX',
          },
        },

        {
          path: 'profile',
          name: 'companyProfile',
          component: CompanyProfile,
          meta: {
            title: 'Company Profile - RecruitX',
          },
        },
      ],
    },
  ],
})

// set page title
router.beforeEach((to, from) => {
  document.title = to.meta.title || 'RecruitX'
})

// auth on page route (all roles)
router.beforeEach((to, from) => {
  let access_token = localStorage.getItem('access_token')
  let role = localStorage.getItem('role')

  if ((access_token === null || role === null) && to.path !== '/') {
    return { name: 'auth' }
  }

  if (!to.path.startsWith(`/${role}`) && to.path !== '/') {
    return { name: 'auth' }
  }
})

// student profile check
router.beforeEach((to, from) => {
  let profile_complete = localStorage.getItem('profile_complete')
  if (profile_complete === null && to.path !== '/') {
    return { name: 'auth' }
  }

  if (
    profile_complete === 'false' &&
    to.name !== 'studentProfile' &&
    to.path.startsWith('/student')
  ) {
    return { name: 'studentProfile' }
  }
})

// Company profile check
router.beforeEach((to, from) => {
  let profile_complete = localStorage.getItem('profile_complete')
  if (profile_complete === null && to.path !== '/') {
    return { name: 'auth' }
  }

  if (
    profile_complete === 'false' &&
    to.name !== 'companyProfile' &&
    to.path.startsWith('/company')
  ) {
    return { name: 'companyProfile' }
  }
})

export default router
