<script setup lang="ts">
import type { Metadata } from '@/types/resume'

defineProps<{
  metadata: Metadata
}>()
</script>

<template>
  <h2 class="card-title uppercase opacity-50">Formation</h2>

  <p v-for="(education, index) in metadata.education" :key="index" class="text-sm font-medium mb-2">
    {{ education.year }} : {{ education.name }} - {{ education.school }}
  </p>
</template>
