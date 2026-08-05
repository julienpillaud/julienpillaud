<script setup lang="ts">
import { computed } from 'vue'
import type { Metadata } from '@/types/resume'

const props = defineProps<{
  metadata: Metadata
}>()

const visibleLanguages = computed(() =>
  props.metadata.languages.filter((language) => !language.optional),
)
</script>

<template>
  <h2 class="card-title uppercase opacity-50">Langues</h2>

  <p v-for="(language, index) in visibleLanguages" :key="index" class="text-sm font-medium mb-2">
    {{ language.name }} : {{ language.level }}
  </p>
</template>
