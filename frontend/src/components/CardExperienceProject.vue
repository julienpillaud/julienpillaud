<script setup lang="ts">
import type { Project } from '@/types/resume'
import { ChevronRight, Minus } from '@lucide/vue'

defineProps<{
  project: Project
}>()
</script>

<template>
  <h2 class="card-title text-sm">{{ project.context }}</h2>

  <ul class="space-y-2">
    <li v-for="task in project.tasks" :key="task.label" class="flex gap-2 text-sm opacity-80">
      <span class="text-primary font-bold">
        <ChevronRight :size="16" class="text-primary" />
      </span>
      <div>
        {{ task.label }}
        <ul v-if="task.details?.length" class="mt-2 space-y-2">
          <li v-for="(detail, index) in task.details" :key="index" class="flex gap-2">
            <span> <Minus :size="16" class="text-primary" /> </span>{{ detail }}
          </li>
        </ul>
      </div>
    </li>
  </ul>
</template>
