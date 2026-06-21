<template>
  <div class="my-4 container">
    <div class="spinner-grow position-fixed top-50 start-50" role="status" v-if="loading">
      <span class="visually-hidden">Loading...</span>
    </div>

    <dashboard-stats :dashboard="dashboard" v-if="!loading" />
    <ApplicationSection
      :dashboard="dashboard"
      v-if="!loading"
      @getApplication="handleGetApplication"
    />
    <StudentSection
      :dashboard="dashboard"
      v-if="!loading"
      @blacklistStudent="handleBlacklistStudent"
    />
    <CompanySection
      :dashboard="dashboard"
      v-if="!loading"
      @approveCompany="handleApproveCompany"
      @blacklistCompany="handleBlacklistCompany"
    />
    <DriveSection
      :dashboard="dashboard"
      v-if="!loading"
      @closeDrive="handleCloseDrive"
      @approveDrive="handleApproveDrive"
      @blacklistDrive="handleBlacklistDrive"
      @getDrive="handleGetDrive"
    />

    <ApplicationCard
      :application="application"
      v-if="Object.keys(application).length !== 0"
      @closeApplication="handleCloseApplication"
    />

    <DriveCard
      :drive="drive"
      v-if="Object.keys(drive).length !== 0"
      @closeDrive="handleCloseDriveCard"
    />
  </div>
</template>

<script setup>
import {
  loadDashboard,
  sendApproveCompany,
  sendApproveDrive,
  sendBlacklistCompany,
  sendBlacklistDrive,
  sendBlacklistStudent,
  sendCloseDrive,
  sendGetApplications,
  sendGetDrive,
} from '@/api/admin'
import { onMounted, reactive, ref, watch } from 'vue'
import { showToast } from '@/toast.js'

import DashboardStats from './DashboardStats.vue'
import ApplicationSection from './ApplicationSection.vue'
import StudentSection from './StudentSection.vue'
import CompanySection from './CompanySection.vue'
import DriveSection from './DriveSection.vue'

import ApplicationCard from './ApplicationCard.vue'
import DriveCard from './DriveCard.vue'

// search
const props = defineProps(["searchTerm"])

watch(
  () => props.searchTerm,
  (newSearchTerm) => {reload(newSearchTerm)}
)

let dashboard = reactive({
  approvedCompanies: [],
  removedCompanies: [],
  pendingCompanies: [],

  approvedStudents: [],
  removedStudents: [],

  applications: [],

  approvedDrives: [],
  pendingDrives: [],
  closedDrives: [],
  removedDrives: [],
})

let application = ref({})
let drive = ref({})
let loading = ref(true)

onMounted(() => {
  reload(props.searchTerm || "")
})

// reload data
async function reload(s) {
  let data = await loadDashboard(s)
  for (const k in dashboard) {
    dashboard[k] = data[k]
  }
  loading.value = false
}

// company
async function handleApproveCompany(user_id) {
  const data = await sendApproveCompany(user_id)
  if (data && data.status == 'success') {
    showToast(data.message)
    reload(props.searchTerm || "")
  }
}

async function handleBlacklistCompany(user_id) {
  const data = await sendBlacklistCompany(user_id)
  if (data && data.status == 'success') {
    showToast(data.message)
    reload(props.searchTerm || "")
  }
}

// student
async function handleBlacklistStudent(user_id) {
  const data = await sendBlacklistStudent(user_id)
  if (data && data.status == 'success') {
    showToast(data.message)
    reload(props.searchTerm || "")
  }
}

// Drive
async function handleBlacklistDrive(drive_id) {
  const data = await sendBlacklistDrive(drive_id)
  if (data && data.status == 'success') {
    showToast(data.message)
    reload(props.searchTerm || "")
  }
}

async function handleCloseDrive(drive_id) {
  const data = await sendCloseDrive(drive_id)
  if (data && data.status == 'success') {
    showToast(data.message)
    reload(props.searchTerm || "")
  }
}

async function handleApproveDrive(drive_id) {
  const data = await sendApproveDrive(drive_id)
  if (data && data.status == 'success') {
    showToast(data.message)
    reload(props.searchTerm || "")
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

async function handleGetDrive(drive_id) {
  const data = await sendGetDrive(drive_id)
  if (data && data.status == 'success') {
    drive.value = data
  }
}

function handleCloseDriveCard() {
  drive.value = {}
}
</script>
