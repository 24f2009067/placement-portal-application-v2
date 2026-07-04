<template>
  <div class="my-4 container">
    <div class="spinner-grow position-fixed top-50 start-50" role="status" v-if="loading">
      <span class="visually-hidden">Loading...</span>
    </div>
    <DriveSection :dashboard="dashboard" @closeDrive="handleCloseDrive" @createDrive="handleCreateDrive" v-if="!loading" />
    <ApplicationSection :dashboard="dashboard" v-if="!loading" />
  </div>
</template>

<script setup>
import DriveSection from './DriveSection.vue'
import { loadDashboard, sendCloseDrive } from '@/api/company'
import { onMounted, reactive, ref, watch } from 'vue'
import ApplicationSection from './ApplicationSection.vue'
import { showToast } from '@/toast.js'
import { useRouter } from 'vue-router'

const dashboard = reactive({})
let loading = ref(true)
const router = useRouter();

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
  loading.value = false
}

async function handleCloseDrive(drive_id) {
  const data = await sendCloseDrive(drive_id)
  if (data && data.status == 'success') {
    showToast(data.message)
    reload(props.searchTerm || "")
  }
}

function handleCreateDrive(){
    router.push({"name": "createDrive"})
}
</script>
