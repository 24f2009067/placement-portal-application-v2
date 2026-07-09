<template>
  <div class="container my-4">
    <div class="spinner-grow position-fixed top-50 start-50" role="status" v-if="loading">
      <span class="visually-hidden">Loading...</span>
    </div>

    <div class="row" v-if="!loading">
      <div class="col-12">
        <h1>Notifications</h1>
        <p class="text-center fw-bold text-muted" v-if="notifications.length == 0">No new Notifications</p>
        <div class="card my-3 p-3" v-for="n in notifications" :key="n.notification_id">
          <div class="d-flex justify-content-between flex-wrap">
            <h3 class="card-title">{{ n.title }}</h3>
            <p class="text-muted fw-bold">{{ new Date(n.created_on).toLocaleString() }}</p>
          </div>
          <div class="d-flex justify-content-between align-items-center flex-wrap">
            <p>{{ n.message }}</p>
            <button class="btn btn-info text-nowrap" @click="handleMarkRead(n.notification_id)">Mark as Read</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getNotifications, markRead } from '@/api/student'
import { showToast } from '@/toast'
import { onMounted, ref } from 'vue'

let loading = ref(true)
const notifications = ref(null)

onMounted(() => {
  reload()
})

async function reload(){
  const data = await getNotifications()
  if (data && data.status === 'success') {
    notifications.value = data.notifications
    loading.value = false
  }
}

async function handleMarkRead(notification_id){
  const data = await markRead(notification_id)
  if (data && data.status === 'success') {
    showToast('Student Dashboard', data.message)
  }
  reload()
}
</script>
