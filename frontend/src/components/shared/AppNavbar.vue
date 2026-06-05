<template>
  <nav class="navbar navbar-expand-lg navbar-dark sticky-top border-bottom border-2 py-3 bg-body">
    <div class="container-fluid">
      <!-- Logo -->
      <a class="navbar-brand d-flex align-items-center" href="#">
        <img src="/recruitx/recruitex-default-monochrome.svg" alt="RecruitX" width="120" />
      </a>

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
            <a class="nav-link active" href="#">
              <i class="bi bi-speedometer2 me-1"></i>
              Dashboard
            </a>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="#">
              <i class="bi bi-briefcase me-1"></i>
              Jobs
            </a>
          </li>
        </ul>

        <!-- Right Section -->
        <div class="d-flex align-items-center gap-3">
          <!-- Search -->
          <form role="search">
            <div class="input-group">
              <input class="form-control" type="search" placeholder="Search" />
              <span class="input-group-text">
                <i class="bi bi-search"></i>
              </span>
            </div>
          </form>

          <!-- Dropdown -->
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                <i class="bi bi-person-circle me-1"></i>
                Account
              </a>

              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="toProfile"> Profile </a>
                </li>

                <li>
                  <a class="dropdown-item" href="#"> Settings </a>
                </li>

                <li><hr class="dropdown-divider" /></li>

                <li>
                  <a class="dropdown-item text-danger" @click.prevent="logOut" href="#"> Logout </a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped></style>

<script setup>
  import { useRouter } from 'vue-router';
  let router = useRouter()

  function logOut(){
    localStorage.clear()
    router.push("/");
  }

  function toProfile(){
    let role = localStorage.getItem("role");
    if (role){
      router.push(`/${role}/profile`)
    }

  }
</script>
