<template>
  <AppNavbar @search="handleSearch" />
  <router-view :searchTerm="searchTerm"></router-view>
</template>

<script setup>
import AppNavbar from '@/components/shared/AppNavbar.vue'
import { ref } from 'vue';

const searchTerm = ref("")
function handleSearch(s){
  searchTerm.value = s
}
</script>
