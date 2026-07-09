<template>
  <div
    class="position-fixed top-0 start-0 h-100 w-100"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(5px); z-index: 1500"
  >
    <div class="container h-100">
      <div class="row h-100 justify-content-center align-items-center">
        <div class="col-12 col-md-10 col-lg-6">
          <div class="card shadow">
            <div class="card-body">
              <h3 class="card-title mb-4">
                Drive
                <span class="text-secondary">#{{ drive.drive_id }}</span>
              </h3>
              <div class="my-4">
                <p class="text-muted fw-bold mb-2 fs-4">Job</p>
                <h4>{{ drive.job_title }}</h4>
                <p class="fw-bold text-dark-emphasis my-2">
                  {{ drive.description }}
                </p>
                <p>
                  Salary:
                  <span class="fw-bold"> {{ 'Rs. ' + Number(drive.salary) || 'NA' }} </span>
                </p>
              </div>

              <div class="my-4">
                <p class="text-muted fw-bold mb-2 fs-4">Company</p>
                <h4>{{ drive.company_name }}</h4>
              </div>

              <div class="my-4">
                <p class="text-muted fw-bold mb-2 fs-4">
                  Eligibility - <span v-if="drive.eligible" class="text-success">Eligible</span>
                  <span class="text-danger" v-else>Not Eligible</span>
                </p>
                <h4>Deadline: {{ drive.deadline }}</h4>

                <p class="my-2">
                  Minimum CGPA: <span class="fw-bold">{{ drive.eligibility_cgpa }} </span>
                </p>

                <p class="my-2">
                  Graduation year:
                  <span class="fw-bold">{{ drive.eligibility_graduation_year }} and earlier </span>
                </p>

                <p class="my-2">
                  Maximum backlog count:
                  <span class="fw-bold">{{ drive.eligibility_backlog_count }} </span>
                </p>

                <p class="my-2">
                  Required Skills:
                  <span class="fw-bold">{{ drive.required_skills }} </span>
                </p>
              </div>

              <div class="my-4 d-flex justify-content-center gap-3">
                <button class="btn btn-success" v-if="drive.eligible" @click="$emit('apply', drive.drive_id)">Apply</button>
                <button class="btn btn-secondary" @click="$emit('closeDrive')">go back</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['drive'])
</script>