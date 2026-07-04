<template>
  <div class="container flex-grow-1 d-flex align-items-center">
    <div class="row justify-content-center w-100 g-4 align-items-start">
      <div class="col-12 col-lg-6 my-5 text-center">
        <img
          src="/recruitx/recruitex-default-monochrome.svg"
          alt="recruitex logo"
          srcset=""
          class="img-fluid"
        />
      </div>

      <!-- Register -->
      <div class="col-12 col-md-7">
        <div class="card p-4" style="border-right: 2px solid rgba(255, 255, 255, 0.2)">
          <div class="card-body">
            <h2 class="mb-4 text-center">Register</h2>
            <form @submit.prevent="handleRegister">
              <div class="btn-group w-100 text-nowrap">
                <input
                  type="radio"
                  class="btn-check"
                  id="student-radio"
                  name="role-radio"
                  value="student"
                  v-model="registerForm.role"
                  required
                />
                <label class="btn btn-outline-secondary w-50" for="student-radio">Student</label>

                <input
                  type="radio"
                  class="btn-check"
                  id="company-radio"
                  name="role-radio"
                  value="company"
                  v-model="registerForm.role"
                  required
                />
                <label class="btn btn-outline-secondary w-50" for="company-radio">Company</label>
              </div>

              <div class="my-4">
                <label class="form-label" for="registerEmail">Email</label>
                <input
                  class="form-control"
                  type="email"
                  name="registerEmail"
                  id="registerEmail"
                  v-model="registerForm.email"
                  required
                />
              </div>

              <div class="mb-4">
                <label class="form-label" for="registerPassword">Password</label>
                <input
                  class="form-control"
                  type="password"
                  name="registerPassword"
                  id="registerPassword"
                  v-model="registerForm.password"
                  required
                />
              </div>
              <p
                :class="{
                  'text-danger': regStatus === 'error',
                  'text-success': regStatus !== 'error',
                  'text-center': true,
                }"
                v-if="regMsg"
              >
                {{ regMsg }}
              </p>
              <button type="submit" class="my-3 btn btn-dark w-100">Register</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Login -->
      <div class="col-12 col-md-5">
        <div class="card p-4">
          <div class="card-body">
            <h2 class="mb-4 text-center">Login</h2>
            <form @submit.prevent="handleLogin">
              <div class="my-4">
                <label class="form-label" for="loginEmail">Email</label>
                <input
                  class="form-control"
                  type="email"
                  name="loginEmail"
                  id="loginEmail"
                  v-model="loginForm.email"
                  required
                />
              </div>
              <div class="my-4">
                <label class="form-label" for="loginPassword">Password</label>
                <input
                  class="form-control"
                  type="password"
                  name="loginPassword"
                  id="loginPassword"
                  v-model="loginForm.password"
                  required
                />
              </div>
              <p
                :class="{
                  'text-danger': loginStatus === 'error',
                  'text-success': loginStatus !== 'error',
                  'text-center': true,
                }"
                v-if="loginMsg"
              >
                {{ loginMsg }}
              </p>
              <button type="submit" class="btn btn-dark w-100 my-3">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { register, login } from '@/api/auth'
import { useRouter } from 'vue-router'
import { showToast } from '@/toast';

let router = useRouter();

// Register
const registerForm = reactive({
  role: 'student',
  email: '',
  password: '',
})

const loginForm = reactive({
  email: '',
  password: '',
})

let regMsg = ref('')
let regStatus = ref('')

async function handleRegister() {
  let { email, password, role } = registerForm
  if (password.length < 4) {
    regMsg.value = 'Password is too short'
    regStatus.value = 'error'
    return
  }

  let res = await register(email, password, role)
  regMsg.value = res.message
  regStatus.value = res.status
}

// login

let loginMsg = ref('')
let loginStatus = ref('')

async function handleLogin() {
  let { email, password } = loginForm
  if (password.length < 4) {
    loginMsg.value = 'Password is too short'
    loginStatus.value = 'error'
    return
  }

  let res = await login(email, password)
  loginMsg.value = res.message
  loginStatus.value = res.status

  if (res.status == "success"){
    localStorage.setItem("id", res.id)
    localStorage.setItem("role", res.role)
    localStorage.setItem("access_token", res.access_token)
    localStorage.setItem("email", email)
    localStorage.setItem("profile_complete", res.profile_complete)

    showToast("", `Login Successful!`)
    router.push(`/${res.role}`);
  }

}
</script>

<style scoped>
.card{
  border: none;
}
</style>
