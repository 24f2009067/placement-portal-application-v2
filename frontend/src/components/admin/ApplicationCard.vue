<template>
  <div
    class="position-fixed top-0 start-0 h-100 w-100"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(5px)"
  >
    <div class="container h-100">
      <div class="row h-100 justify-content-center align-items-center">
        <div class="col-12 col-md-10 col-lg-6">
          <div class="card shadow">
            <div class="card-body">
              <h3 class="card-title mb-4">
                Student Application
                <span class="text-secondary">#{{ application.application_id }}</span>
              </h3>
              <div class="my-4">
                <p class="text-muted fw-bold mb-2 fs-4">Student</p>
                <h4>{{ application.student_name }}</h4>
                <p class="fw-bold text-secondary my-2">
                  {{ application.course }} • {{ application.dept }}
                </p>
                <p class="fw-bold text-secondary my-2">
                  <span class="text-dark-emphasis">skills:</span> {{ application.skills }}
                </p>
              </div>

              <div class="my-4">
                <p class="text-muted fw-bold mb-2 fs-4">Company</p>
                <h4>{{ application.company_name }}</h4>
                <p class="fw-bold text-secondary">{{ application.job_title }}</p>
              </div>

              <div class="my-4">
                <p class="text-muted fw-bold mb-2 fs-4">Application</p>
                <h4>{{ application.application_status }}</h4>
                <p class="fw-bold text-secondary"><span class="text-dark-emphasis">Applied on</span> {{ application.created_on.split('.')[0] }}</p>
              </div>

              <div class="my-4 d-flex justify-content-center gap-3">
                <button class="btn btn-info" @click="getResume" v-if="application.resume">View Resume</button>
                <button class="btn btn-secondary" @click="$emit('closeApplication')">
                  go back
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const API_URL = import.meta.env.VITE_API_URL
const props = defineProps(['application'])

function getResume() {
  window.open(`${API_URL}/api/students/resume/${props.application.student_id}`)
}
</script>
