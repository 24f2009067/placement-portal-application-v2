<script setup>
import { toasts } from '@/toast';
</script>

<template>
  <div
    class="toast-container position-fixed bottom-0 end-0 p-3"
  >
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="toast show"
    >

      <div class="toast-header border-2">
          <img src="/recruitx/recruitex-default-monochrome.svg" class="rounded me-2 w-25" alt="RecruitX logo">
          <strong class="ms-auto">{{ ((Date.now() - toast.id) / 1000).toFixed(0) }} sec ago</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">
          <p class="fw-bolder fs-5 mb-1">{{ toast.title }}</p>
          <p class="text-muted">{{ toast.message }}</p>
      </div>

    </div>
  </div>
</template>