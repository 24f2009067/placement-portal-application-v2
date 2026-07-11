<template>
  <div
    class="position-fixed top-0 start-0 h-100 w-100"
    style="
      background-color: rgba(0, 0, 0, 0.3);
      backdrop-filter: blur(5px);
      z-index: 1500;
      overflow-y: auto;
    "
  >
    <div class="container min-vh-100 d-flex align-items-center py-3">
      <div class="row justify-content-center align-items-stretch gy-3 gx-2 w-100">
        <!-- Placement (selected) -->
        <div
          class="col-12 col-xl-7 d-flex"
          v-if="status == 'selected' && application.application_status != 'selected'"
        >
          <div class="card shadow flex-fill">
            <div class="card-body">
              <h3 class="card-title mb-4">Placement Details</h3>

              <div class="my-3">
                <label class="form-label" for="position">Job Position</label>
                <input
                  class="form-control"
                  type="text"
                  id="position"
                  v-model="placement.position"
                />
              </div>

              <div class="my-3">
                <label class="form-label" for="salary">Salary</label>
                <input class="form-control" type="number" id="salary" v-model="placement.salary" min="0"/>
              </div>

              <div class="my-3">
                <label class="form-label" for="joining_date">Joining Date</label>
                <input
                  class="form-control"
                  type="date"
                  id="joining_date"
                  v-model="placement.joining_date"
                  :min="(new Date()).toISOString().slice(0, 10)"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Interview (shortlisted) -->
        <div
          class="col-12 col-xl-7 d-flex"
          v-if="status == 'shortlisted' && application.application_status != 'shortlisted'"
        >
          <div class="card shadow flex-fill">
            <div class="card-body">
              <h3 class="card-title mb-4">Schedule Interview</h3>

              <div class="my-3">
                <label class="form-label" for="location">Location</label>
                <input
                  class="form-control"
                  type="text"
                  id="location"
                  v-model="interview.location"
                />
              </div>

              <div class="my-3">
                <label class="form-label" for="scheduled_at">Scheduled at</label>
                <input
                  class="form-control"
                  type="datetime-local"
                  id="scheduled_at"
                  v-model="interview.scheduled_at"
                  :min="(new Date()).toISOString().slice(0, 16)"
                />
              </div>

              <div class="my-3">
                <label class="form-label me-2">Mode</label>

                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    id="offline"
                    value="offline"
                    v-model="interview.mode"
                  />
                  <label class="form-check-label" for="offline"> Offline </label>
                </div>

                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    id="online"
                    value="online"
                    v-model="interview.mode"
                  />
                  <label class="form-check-label" for="online"> Online </label>
                </div>
              </div>

              <div class="my-3">
                <label class="form-label" for="feedback">Feedback</label>
                <textarea
                  class="form-control"
                  :rows="5"
                  id="feedback"
                  v-model="interview.feedback"
                ></textarea>
              </div>
            </div>
          </div>
        </div>

        <div
          class="col-12 d-flex"
          :class="{
            'col-xl-5': status == 'shortlisted' || status == 'selected',
            'col-xl-6':
              application.application_status == 'selected' ||
              application.application_status == 'rejected' ||
              status === 'rejected' ||
              application.application_status == status,
          }"
        >
          <div class="card shadow flex-fill">
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

              <div class="my-4 d-flex justify-content-between">
                <div>
                  <p class="text-muted fw-bold mb-2 fs-4">Application</p>
                  <h4>{{ application.application_status }}</h4>
                  <p class="fw-bold text-secondary">
                    <span class="text-dark-emphasis">Applied on</span>
                    {{ application.created_on.split('.')[0] }}
                  </p>
                </div>
                <div class="d-flex flex-column justify-content-center">
                  <button
                    class="btn btn-info text-nowrap"
                    @click="getResume"
                    v-if="application.resume"
                  >
                    View Resume
                  </button>
                </div>
              </div>

              <div
                class="my-4"
                v-if="
                  application.application_status === 'applied' ||
                  application.application_status === 'shortlisted'
                "
              >
                <p class="text-muted fw-bold mb-2 fs-4">Modify Status</p>
                <select name="status" id="status" class="form-select text-dark" v-model="status">
                  <option value="shortlisted" v-if="application.application_status === 'applied'">
                    Shortlist
                  </option>

                  <option value="rejected">Reject</option>

                  <option
                    value="selected"
                    v-if="
                      application.application_status === 'applied' ||
                      application.application_status === 'shortlisted'
                    "
                  >
                    Select
                  </option>
                  <option hidden value="applied">Applied</option>
                </select>
              </div>

              <div class="my-4 d-flex justify-content-center gap-3">
                <button
                  class="btn btn-success"
                  @click="handleSubmit"
                  v-if="
                    application.application_status === 'applied' ||
                    application.application_status === 'shortlisted'
                  "
                >
                  Save
                </button>
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
import { modifyApplication } from '@/api/company'
import { showToast } from '@/toast'
import { reactive, ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL
const props = defineProps(['application'])
const emits = defineEmits(["closeApplication"])
const status = ref(props.application.application_status)

const interview = reactive({
  mode: 'offline',
  feedback: '',
  scheduled_at: '',
  location: '',
})

const placement = reactive({
  position: '',
  salary: 0.0,
  joining_date: '',
})

async function handleSubmit() {
  if (status.value === props.application.application_status) return

  if (status.value === 'selected' || status.value === 'shortlisted' || status.value === 'rejected') {
    const data = await modifyApplication(
      props.application.application_id,
      status.value,
      interview,
      placement,
    )
    if (data && data.status == 'success') {
      console.log(data)
      showToast(data.message)
      emits("closeApplication")
    }
  }
}

function getResume() {
  window.open(`${API_URL}/api/students/resume/${props.application.student_id}`)
}
</script>
