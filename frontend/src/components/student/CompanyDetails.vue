<template>
  <div class="container">
    <div class="spinner-grow position-fixed top-50 start-50" role="status" v-if="loading">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div class="row my-3" v-if="!loading">
      <div class="col-12">
        <div class="mt-3 mb-4">
          <h1>{{ company.company_name }} - <span class="text-muted">{{ company.company_email }}</span></h1>
        </div>
        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title">Drives</h3>

            <div class="mt-4">
              <h4 class="text-muted">Approved Drives</h4>
              <div class="table-responsive" v-if="company.drives && company.drives.length !== 0">
                <table class="table text-center">
                  <thead>
                    <tr>
                      <th>Drive ID</th>
                      <th>Job Position</th>
                      <th>Deadline</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                    <tr v-for="drive in company.drives" :key="drive.drive_id">
                      <td>{{ drive.drive_id }}</td>
                      <td>{{ drive.job_title }}</td>
                      <td>{{ drive.deadline }}</td>
                      <td>
                        <div class="d-flex justify-content-center align-content-center">
                          <button
                            class="btn btn-dark mx-1"
                            @click="handleGetDrive(drive.drive_id)"
                          >
                            view
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p
                class="text-center fw-bold text-secondary my-3"
                v-if="company.drives && company.drives.length === 0"
              >
                No approved drive
              </p>
            </div>
          </div>
        </div>

        <div class="my-3 d-flex justify-content-end">
          <button class="btn btn-light" @click="router.back()">Go Back</button>
        </div>
      </div>
    </div>
  </div>

  <DriveCard :drive="drive" v-if="drive" @closeDrive="drive=null" @apply="handleApply"></DriveCard>
</template>

<script setup>
import { applyDrive, getCompany, getDrive } from '@/api/student'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DriveCard from './DriveCard.vue'
import { showToast } from '@/toast.js'

const route = useRoute()
const router = useRouter()
const user_id = route.params.id

const company = ref({})
const drive = ref(null)
let loading = ref(true)

onMounted(async () => {
  const data = await getCompany(user_id)
  if (data && data.status === 'success') {
    company.value = data
    loading.value = false
  }
})

async function handleGetDrive(drive_id){
  const data = await getDrive(drive_id)
  if (data && data.status === 'success') {
    drive.value = data
  }
}

async function handleApply(drive_id) {
  const data = await applyDrive(drive_id)
  console.log(data)
  if (data && data.status === 'success') {
    showToast('Student Dashboard', data.message)
  }

  drive.value = null
}
</script>
