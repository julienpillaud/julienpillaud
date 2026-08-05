<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import AppNavbar from '@/components/AppNavbar.vue'

const route = useRoute()
</script>

<template>
  <AppNavbar v-if="route.meta.showNavbar" />
  <RouterView />
</template>
