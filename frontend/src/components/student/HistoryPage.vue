<template>
  <div class="container my-4">
    <div class="spinner-grow position-fixed top-50 start-50" role="status" v-if="loading">
      <span class="visually-hidden">Loading...</span>
    </div>

    <div class="row" v-if="!loading">
      <div class="col-12">
        <h1>History</h1>
        <p class="text-center fw-bold text-muted" v-if="applications.length == 0">
          Nothing to Show
        </p>

        <div
          class="card p-3 my-4"
          v-for="application in applications"
          :key="application.application_id"
        >
          <h3 class="card-title">{{ application.company_name }} • {{ application.job_title }}</h3>
          <ul class="list-group list-group-horizontal-sm border-0 my-2 mx-auto">
            <template
              v-for="(s, index) in application.application_history"
              :key="s.application_history_id"
            >
              <li
                :class="[
                  'fw-bold',
                  'list-group-item',
                  index < application.application_history.length - 1
                    ? 'text-secondary'
                    : 'border-warning',
                ]"
              >
                {{ s.status }}
              </li>

              <li
                v-if="index < application.application_history.length - 1"
                class="list-group-item px-2 d-flex justify-content-center"
              >
                <i class="bi bi-arrow-right text-secondary fw-bold"></i>
              </li>
            </template>
          </ul>

          <div v-if="application.interviews.length !== 0" class="my-3">
            <h4>Interview</h4>
            <div v-for="interview in application.interviews" :key="interview.interview_id">
              <div class="my-3 p-3">
                <p class="fw-bold">
                  Mode: <span class="fw-normal">{{ interview.type }}</span>
                </p>
                <p class="fw-bold">
                  Location: <span class="fw-normal">{{ interview.location }}</span>
                </p>
                <p class="fw-bold">
                  Scheduled at:
                  <span class="fw-normal">{{
                    new Date(interview.scheduled_at).toLocaleString()
                  }}</span>
                </p>
                <p class="fw-bold">
                  Location: <span class="fw-normal">{{ interview.location }}</span>
                </p>
                <p class="fw-bold">
                  Feedback: <span class="fw-normal">{{ interview.feedback }}</span>
                </p>
              </div>
            </div>
          </div>

          <div v-if="application.placements.length !== 0" class="my-3">
            <h4>Placement</h4>
            <div v-for="placement in application.placements" :key="placement.placement_id">
              <div class="my-3 p-3">
                <p class="fw-bold">
                  Position: <span class="fw-normal">{{ placement.position }}</span>
                </p>
                <p class="fw-bold">
                  Salary: <span class="fw-normal">{{ Number(placement.salary) }}</span>
                </p>
                <p class="fw-bold">
                  Joining Date:
                  <span class="fw-normal">{{
                    new Date(placement.joining_date).toLocaleString()
                  }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getHistory } from '@/api/student'
import { onMounted, ref } from 'vue'

let loading = ref(true)
const applications = ref(null)

onMounted(async () => {
  const data = await getHistory()
  if (data && data.status === 'success') {
    applications.value = data.applications
    loading.value = false

    console.log(data)
  }
})
</script>
