<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <h1>Create Drive</h1>
        <p class="fw-bold text-muted">{{ company.name }} • {{ company.email }}</p>

        <form @submit.prevent="handleCreateDrive">
          <div class="card shadow mb-4">
            <div class="card-body">
              <h5 class="card-title mb-4">Job Details</h5>
              <div class="mb-3">
                <label for="position" class="form-label"
                  >Job Position<span class="text-danger"> *</span></label
                >
                <input
                  type="text"
                  id="position"
                  class="form-control"
                  required
                  v-model="drive.job_title"
                />
              </div>
              <div class="mb-3">
                <label for="description" class="form-label"
                  >Job Description<span class="text-danger"> *</span></label
                >
                <textarea
                  id="description"
                  rows="3"
                  class="form-control"
                  required
                  v-model="drive.description"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="salary" class="form-label"
                  >Salary<span class="text-danger"> *</span></label
                >
                <input
                  type="number"
                  id="salary"
                  class="form-control"
                  required
                  v-model="drive.salary"
                  min="0"
                />
              </div>
            </div>
          </div>

          <div class="card shadow mb-4">
            <div class="card-body">
              <h5 class="card-title mb-4">Eligibility</h5>
              <div class="row g-3">
                <div class="col-md-6">
                  <label for="cgpa" class="form-label"
                    >CGPA<span class="text-danger"> *</span></label
                  >
                  <input
                    id="cgpa"
                    type="number"
                    step="0.01"
                    class="form-control"
                    required
                    v-model="drive.eligibility_cgpa"
                    min="0"
                  />
                </div>

                <div class="col-md-6">
                  <label for="graduation_year" class="form-label">
                    Graduation Year<span class="text-danger"> *</span>
                  </label>
                  <input
                    id="graduation_year"
                    type="number"
                    class="form-control"
                    required
                    min="1"
                    v-model="drive.eligibility_graduation_year"
                  />
                </div>
              </div>

              <div class="my-3">
                <label for="backlog_count" class="form-label">
                  Number of Backlogs <span class="text-danger">*</span>
                </label>
                <input
                  id="backlog_count"
                  type="number"
                  class="form-control"
                  min="0"
                  required
                  v-model="drive.eligibility_backlog_count"
                />
              </div>

              <div class="mb-3">
                <label for="deadline" class="form-label"
                  >Deadline<span class="text-danger"> *</span></label
                >
                <input
                  type="date"
                  id="deadline"
                  class="form-control"
                  required
                  v-model="drive.deadline"
                  :min="new Date().toLocaleDateString('en-CA')"
                />
              </div>
            </div>
          </div>

          <div class="card shadow mb-4">
            <div class="card-body">
              <h5 class="card-title mb-3">Required Skills</h5>

              <textarea
                id="skills"
                rows="4"
                class="form-control"
                placeholder="Java, Python, SQL, Vue.js..."
                v-model="drive.required_skills"
              ></textarea>
            </div>
          </div>

          <div class="d-flex justify-content-end gap-3">
            <button class="btn btn-light" @click.prevent="goBack">Go Back</button>
            <button type="submit" class="btn btn-success">Create Drive</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDrive, getCompanyProfile } from '@/api/company'
import { showToast } from '@/toast'
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const company = ref({})
const drive = reactive({
  job_title: '',
  description: '',
  salary: '',
  eligibility_cgpa: '',
  eligibility_graduation_year: '',
  eligibility_backlog_count: '',
  required_skills: '',
  deadline: '',
})
const router = useRouter()

onMounted(async () => {
  const data = await getCompanyProfile()
  company.value = data
})

async function handleCreateDrive() {
  const data = await createDrive(drive)
  if (data && data.status == 'success') {
    showToast(data.message)
    router.back()
  }
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.card {
  border: 0.2rem solid rgba(19, 19, 19, 0.5);
}
</style>
