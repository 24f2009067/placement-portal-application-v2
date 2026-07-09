import { createRouter, createWebHistory } from 'vue-router'

import AuthView from '@/views/AuthView.vue'
import AdminView from '@/views/AdminView.vue'
import StudentView from '@/views/StudentView.vue'
import CompanyView from '@/views/CompanyView.vue'

import StudentDashboard from '@/components/student/StudentDashboard.vue'
import StudentProfile from '@/components/student/StudentProfile.vue'

import CompanyDashboard from '@/components/company/CompanyDashboard.vue'
import CompanyProfile from '@/components/company/CompanyProfile.vue'
import { showToast } from '@/toast'
import CreateDrive from '@/components/company/CreateDrive.vue'
import UpdateDrive from '@/components/company/UpdateDrive.vue'
import DriveDetail from '@/components/company/DriveDetail.vue'
import CompanyDetails from '@/components/student/CompanyDetails.vue'
import NotificationPage from '@/components/student/NotificationPage.vue'
import HistoryPage from '@/components/student/HistoryPage.vue'

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

        {
          path: 'company/:id',
          name: 'companyDetails',
          component: CompanyDetails,
          meta: {
            title: 'Company Details - RecruitX',
          },
        },

        {
          path: 'notifications',
          name: 'notifications',
          component: NotificationPage,
          meta: {
            title: 'Student Notifications - RecruitX',
          },
        },

        {
          path: 'history',
          name: 'history',
          component: HistoryPage,
          meta: {
            title: 'Student History - RecruitX',
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

        {
          path: 'drive/create',
          name: 'createDrive',
          component: CreateDrive,
          meta: {
            title: 'Create Drive - RecruitX',
          },
        },

        {
          path: 'drive/:id/update',
          name: 'updateDrive',
          component: UpdateDrive,
          meta: {
            title: 'Update Drive - RecruitX',
          },
        },

        {
          path: 'drive/:id',
          name: 'driveDetail',
          component: DriveDetail,
          meta: {
            title: 'Drive details - RecruitX',
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
router.beforeEach(async (to, from) => {
  let access_token = localStorage.getItem('access_token')
  let role = localStorage.getItem('role')

  if ((access_token === null || role === null) && to.path !== '/') {
    return { name: 'auth' }
  }

  if (!to.path.startsWith(`/${role}`) && to.path !== '/') {
    return { name: 'auth' }
  }
  if (to.path !== '/') {
    if (access_token) {
      try {
        const access_token = localStorage.getItem('access_token')
        const payload = access_token.split('.')[1]
        const data = JSON.parse(atob(payload))

        if (data.role === 'student' || data.role === 'company') {
          if (data.profile_complete && !data.is_active) {
            showToast('Authentication', 'Contact admin for approval!')
            return { name: 'auth' }
          }
        }
      } catch (err) {
        console.log(err)
        return { name: 'auth' }
      }
    }
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
