import { createRouter, createWebHistory } from 'vue-router'

import AuthView from '@/views/AuthView.vue'
import AdminView from '@/views/AdminView.vue'
import StudentView from '@/views/StudentView.vue'
import CompanyView from '@/views/CompanyView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "auth",
      component: AuthView
    },

    {
      path: "/admin",
      name: "admin",
      component: AdminView
    },

    {
      path: "/student",
      name: "student",
      component: StudentView
    },

    {
      path: "/company",
      name: "company",
      component: CompanyView
    },
  ],
})

export default router
