<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <!-- Header -->
        <div class="mb-4">
          <h2 class="mb-1">Student Profile</h2>
          <p class="text-muted mb-0">{{ profile.email }}</p>
        </div>

        <form @submit.prevent="handleProfileSubmit">
          <!-- Personal Information -->
          <div class="card shadow-sm mb-4">
            <div class="card-body">
              <h5 class="card-title mb-4">Personal Information</h5>

              <div class="mb-3">
                <label for="name" class="form-label">Name <span class="text-danger">*</span></label>
                <input id="name" type="text" class="form-control" v-model="profile.name" required />
              </div>

              <div class="row g-3">
                <div class="col-md-6">
                  <label for="dept" class="form-label"
                    >Department<span class="text-danger">*</span></label
                  >
                  <input
                    id="dept"
                    type="text"
                    class="form-control"
                    required
                    v-model="profile.dept"
                  />
                </div>

                <div class="col-md-6">
                  <label for="course" class="form-label"
                    >Course<span class="text-danger">*</span></label
                  >
                  <input
                    id="course"
                    type="text"
                    class="form-control"
                    required
                    v-model="profile.course"
                  />
                </div>
              </div>

              <div class="row g-3 mt-1">
                <div class="col-md-6">
                  <label for="cgpa" class="form-label"
                    >CGPA<span class="text-danger">*</span></label
                  >
                  <input
                    id="cgpa"
                    type="number"
                    step="0.01"
                    class="form-control"
                    required
                    v-model="profile.cgpa"
                  />
                </div>

                <div class="col-md-6">
                  <label for="graduation_year" class="form-label">
                    Graduation Year<span class="text-danger">*</span>
                  </label>
                  <input
                    id="graduation_year"
                    type="number"
                    class="form-control"
                    required
                    min="1"
                    v-model="profile.graduation_year"
                  />
                </div>
              </div>

              <div class="mt-3">
                <label for="backlog_count" class="form-label"> Number of Backlogs <span class="text-danger">*</span> </label>
                <input
                  id="backlog_count"
                  type="number"
                  class="form-control"
                  min="0"
                  required
                  v-model="profile.backlog_count"
                />
              </div>
            </div>
          </div>

          <!-- Skills -->
          <div class="card shadow-sm mb-4">
            <div class="card-body">
              <h5 class="card-title mb-3">Skills</h5>

              <textarea
                id="skills"
                rows="4"
                class="form-control"
                placeholder="Java, Python, SQL, Vue.js..."
                v-model="profile.skills"
              ></textarea>
            </div>
          </div>

          <!-- Resume -->
          <div class="card shadow-sm mb-4">
            <div class="card-body">
              <h5 class="card-title mb-3">Resume</h5>

              <input
                type="file"
                id="resume"
                class="form-control"
                accept=".pdf"
                @change="handleFile"
              />

              <div class="d-flex justify-content-between"><span class="form-text">Upload your latest resume (PDF).</span><a class="form-text" href="#" v-if="profile.previous_resume !== ''" @click.prevent="getResume">Open previous upload</a></div>
            </div>
          </div>

          <!-- Submit -->
          <div class="d-flex justify-content-end">
            <button type="submit" class="btn btn-success px-4">Save Profile</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
const API_URL = import.meta.env.VITE_API_URL
import { getStudentProfile, setProfile } from '@/api/student'
import { showToast } from '@/toast'
import { onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const profile = reactive({
  student_id: '',
  email: '',
  name: '',
  skills: '',
  dept: '',
  course: '',
  cgpa: '',
  graduation_year: '',
  backlog_count: '',
  resume: '',
  resume_added: false,
  previous_resume: ""
})

onMounted(async () => {
  const data = await getStudentProfile()

  if (data.status == 'error') {
    console.log(data.message)
    console.log(data.err)
    return
  }
  profile.student_id = data.student_id
  profile.email = data.email
  profile.name = data.name
  profile.skills = data.skills
  profile.dept = data.dept
  profile.course = data.course
  profile.cgpa = data.cgpa
  profile.graduation_year = data.graduation_year
  profile.backlog_count = data.backlog_count
  profile.previous_resume = data.resume
})

function handleFile(e) {
  profile.resume = e.target.files[0]
  profile.resume_added = true
}

async function handleProfileSubmit() {
  const formData = new FormData()
  formData.append('name', profile.name)
  formData.append('skills', profile.skills)
  formData.append('dept', profile.dept)
  formData.append('course', profile.course)
  formData.append('cgpa', profile.cgpa)
  formData.append('graduation_year', profile.graduation_year)
  formData.append('backlog_count', profile.backlog_count)
  formData.append('resume', profile.resume)
  formData.append('resume_added', profile.resume_added)

  const res = await setProfile(formData)
  if (res.status === 'success') {
    localStorage.setItem('profile_complete', true)
    showToast("Student Dashboard", "Profile saved!");
    router.push({ name: 'studentDashboard' })
  }
}

function getResume(){
  window.open(`${API_URL}/api/students/resume/${profile.student_id}`)
}
</script>

<style scoped>
.card{
  border: none;
}
</style>