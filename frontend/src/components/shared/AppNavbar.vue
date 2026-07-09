<template>
  <nav
    class="navbar navbar-expand-lg navbar-dark sticky-top py-3 bg-body shadow"
    style="border-bottom: 0.3rem solid rgba(19, 19, 19, 0.9)"
  >
    <div class="container-fluid">
      <!-- Logo -->
      <RouterLink class="navbar-brand d-flex align-items-center" to="/">
        <img src="/recruitx/recruitex-default-monochrome.svg" alt="RecruitX" width="120" />
      </RouterLink>

      <!-- Mobile Toggle -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar Content -->
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <!-- Left Links -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink
              class="nav-link"
              :class="{
                active:
                  route.name === `${role}Dashboard` ||
                  route.name === 'admin'
              }"
              :to="`/${role}`"
            >
              <i class="bi bi-kanban"></i>
              Dashboard
            </RouterLink>
          </li>

          <template v-if="role === 'student'">
            <li class="nav-item">
              <RouterLink
                class="nav-link"
                :class="{ active: route.name === 'history' }"
                :to="{ name: 'history' }"
              >
                <i class="bi bi-clock-history"></i>
                History
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink
                class="nav-link"
                :class="{ active: route.name === 'notifications' }"
                :to="{ name: 'notifications' }"
              >
                <i class="bi bi-bell"></i>
                Notifications
              </RouterLink>
            </li>
          </template>
        </ul>

        <!-- Right Section -->
        <div class="d-flex align-items-center gap-3">
          <!-- Search -->
          <form role="search" @submit.prevent="emit('search', searchTerm)">
            <div class="input-group">
              <input
                class="form-control"
                type="search"
                v-model="searchTerm"
                placeholder="Search"
              />
              <span class="input-group-text">
                <i class="bi bi-search"></i>
              </span>
            </div>
          </form>

          <!-- User Dropdown -->
          <div class="dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
            >
              <i class="bi bi-person-circle me-1"></i>
              {{ email || "User" }}
            </a>

            <ul class="dropdown-menu dropdown-menu-end">
              <li v-if="role !== 'admin'">
                <a class="dropdown-item" href="#" @click.prevent="toProfile">
                  Profile
                </a>
              </li>

              <li><hr class="dropdown-divider" /></li>

              <li>
                <a
                  class="dropdown-item text-danger"
                  href="#"
                  @click.prevent="logOut"
                >
                  Logout
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const emit = defineEmits(['search'])

const role = computed(() => localStorage.getItem('role'))
const email = computed(() => localStorage.getItem('email'))

if (!role.value || !email.value) {
  router.replace('/')
}

const searchTerm = ref('')

function logOut() {
  localStorage.clear()
  router.replace('/')
}

function toProfile() {
  if (role.value && role.value !== 'admin') {
    router.push(`/${role.value}/profile`)
  }
}
</script>

<style scoped></style>