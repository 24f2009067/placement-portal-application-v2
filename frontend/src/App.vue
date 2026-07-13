<template>
  <div class="d-flex flex-column min-vh-100">
    <router-view />
    <toast-container />
  </div>
</template>

<style>
.card{
  border: 0.2rem solid rgba(255, 255, 255, 0.1);
}

.btn{
  transition: 0.2s;
}

.btn:hover{
  transform: scale(1.05);
}
</style>

<script setup>
import ToastContainer from './components/shared/ToastContainer.vue';
</script>
