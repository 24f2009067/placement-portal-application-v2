<template>
  <div class="my-4 container">
    <div class="spinner-grow position-fixed top-50 start-50" role="status" v-if="loading">
      <span class="visually-hidden">Loading...</span>
    </div>

    <CompanySection v-if="!loading" :dashboard="dashboard" />

    <ApplicationSection
      v-if="!loading"
      :dashboard="dashboard"
      @getApplication="handleGetApplication"
    />

    <ApplicationCard
      :application="application"
      v-if="Object.keys(application).length !== 0"
      @closeApplication="handleCloseApplication"
    />
  </div>
</template>

<script setup>
import { getNotifications, loadDashboard } from '@/api/student'
import { onMounted, reactive, ref, watch } from 'vue'
import CompanySection from './CompanySection.vue'
import ApplicationSection from './ApplicationSection.vue'
import ApplicationCard from '../admin/ApplicationCard.vue'
import { sendGetApplications } from '@/api/admin.js'
import { showToast } from '@/toast.js'

const dashboard = reactive({
  companies: [],
  applications: [],
})
let loading = ref(true)
let application = ref({})

// search
const props = defineProps(['searchTerm'])

watch(
  () => props.searchTerm,
  (newSearchTerm) => {
    reload(newSearchTerm)
  },
)

onMounted(() => {
  reload(props.searchTerm || '')
})

// reload data
async function reload(s) {
  let data = await loadDashboard(s)
  for (const k in data) {
    dashboard[k] = data[k]
  }
  if (data){
    loading.value = false
  }

  const res = await getNotifications()
  const notifications = res.notifications
  const count = notifications.length
  console.log(count)
  if (count !== 0){
    showToast('Student Dashboard', `You have new notifications! (${count})`)
  }
}

// cards
async function handleGetApplication(application_id) {
  const data = await sendGetApplications(application_id)
  if (data && data.status == 'success') {
    application.value = data
  }
}

function handleCloseApplication() {
  application.value = {}
}
</script>
