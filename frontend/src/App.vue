<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import AppNavbar from '@/components/AppNavbar.vue'
import { useTheme } from '@/composables/useTheme'

const route = useRoute()
useTheme()
</script>

<template>
  <AppNavbar v-if="route.meta.showNavbar" />
  <RouterView />
</template>
