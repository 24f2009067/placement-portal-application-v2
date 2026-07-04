<template>
  <div class="container py-4">
    <div class="row">
      <div class="col">
        <h1>Drive Details</h1>
        <p>{{ company.name }} • {{ drive.job_title }}</p>
      </div>
    </div>

    <div class="row my-4">
      <div class="col">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title">Received Applications</h3>
            <div class="table-responsive" v-if="drive.applications.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>Application ID</th>
                    <th>Student Name</th>
                    <th>Company Name</th>
                    <th>Job Position</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="application in drive.applications" :key="application.application_id">
                    <td>{{ application.application_id }}</td>
                    <td>{{ application.student_name }}</td>
                    <td>{{ application.company_name }}</td>
                    <td>{{ application.job_title }}</td>
                    <td>{{ application.application_status }}</td>
                    <td>
                      <button
                        class="btn btn-dark"
                        @click="viewApplication(application.application_id)"
                      >
                        view
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="drive.applications.length === 0"
            >
              No student applications
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col d-flex justify-content-end">
        <button class="btn btn-light" @click="router.back()">Go Back</button>
      </div>
    </div>
  </div>

  <ApplicationCard
    :application="application"
    v-if="application"
    @closeApplication="
      () => {
        application = null
        reload()
      }
    "
  ></ApplicationCard>
</template>

<script setup>
import { getCompanyProfile, getDrive } from '@/api/company'
import ApplicationCard from './ApplicationCard.vue'
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const company = ref({})
const application = ref(null)
const drive = reactive({
  job_title: '',
  description: '',
  salary: '',
  eligibility_cgpa: '',
  eligibility_graduation_year: '',
  eligibility_backlog_count: '',
  required_skills: '',
  deadline: '',
  applications: '',
})
const router = useRouter()
const route = useRoute()
const drive_id = route.params.id

onMounted(reload)

async function reload() {
  const data = await getCompanyProfile()
  company.value = data

  const drives = await getDrive(drive_id)
  if (!drives || drives.status !== 'success') {
    router.push({ name: 'auth' })
  }

  for (let key in drive) {
    drive[key] = drives[key]
  }

  drive.salary = Number(drive.salary).toFixed(2)
}

function viewApplication(application_id) {
  application.value = drive.applications.filter(
    (application) => application.application_id == application_id,
  )[0]
}
</script>
