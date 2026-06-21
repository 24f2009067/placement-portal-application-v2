<template>
  <AppNavbar @search="handleSearch" />
  <AdminDashboard :searchTerm="searchTerm"/>
</template>

<script setup>
import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import AppNavbar from '@/components/shared/AppNavbar.vue'
import { ref } from 'vue';

const searchTerm = ref("")
function handleSearch(s){
  searchTerm.value = s
}

</script>
