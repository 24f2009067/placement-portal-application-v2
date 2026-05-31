<template>
  <AppNavbar />
  <div class="container my-4">
    <h1>Hello Student</h1>
  </div>
</template>

<script setup>
import AppNavbar from '@/components/shared/AppNavbar.vue'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

let router = useRouter()

onMounted(() => {
  let access_token = localStorage.getItem('access_token')
  let role = localStorage.getItem('role')

  if (access_token === null || role !== 'student') {
    router.push('/')
  }
})
</script>
