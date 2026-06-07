<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="mb-4">
          <h2 class="mb-1">Company Profile</h2>
          <p class="text-muted mb-0">{{ profile.email }}</p>
        </div>

        <form @submit.prevent="handleProfileSubmit">
          <div class="card shadow-sm mb-4">
            <div class="card-body">
              <h5 class="card-title mb-4">Company Information</h5>

              <div class="mb-3">
                <label for="namr" class="form-label">Name<span class="text-danger">*</span></label>
                <input id="name" type="text" class="form-control required" v-model="profile.name" />
              </div>

              <div class="mb-3">
                <label for="industry" class="form-label"
                  >Industry<span class="text-danger">*</span></label
                >
                <input id="industry" type="text" class="form-control required" v-model="profile.industry" />
              </div>

              <div class="mb-3">
                <label for="location" class="form-label"
                  >Location<span class="text-danger">*</span></label
                >
                <textarea id="location" class="form-control" rows="3" required v-model="profile.location" ></textarea>
              </div>

              <div class="mb-3">
                <label for="website" class="form-label">Website</label>
                <input type="url" id="website" class="form-control" v-model="profile.website" />
              </div>
            </div>

            <div class="d-flex justify-content-end">
              <button type="submit" class="btn btn-success px-4">Save Profile</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getCompanyProfile, setProfile } from '@/api/company'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { reactive } from 'vue'

const router = useRouter();

const profile = reactive({
  email: '',
  name: '',
  industry: '',
  location: '',
  website: '',
})

onMounted(async () => {
  const data = await getCompanyProfile()

  if (data.status == 'error') {
    console.log(data.message)
    console.log(data.err)
    return
  }

  profile.email = data.email
  profile.name = data.name
  profile.industry = data.industry
  profile.location = data.location
  profile.website = data.website
})

async function handleProfileSubmit() {
  const res = await setProfile(profile)
  if (res.status === 'success') {
    localStorage.setItem('profile_complete', true)
    router.push({ name: 'companyDashboard' })
  }
}
</script>
