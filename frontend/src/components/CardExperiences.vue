<script setup lang="ts">
import type { Experience } from '@/types/resume'
import CardExperienceProject from '@/components/CardExperienceProject.vue'
import { BriefcaseBusiness, Calendar, Circle } from '@lucide/vue'

defineProps<{
  experiences: Experience[]
}>()
</script>

<template>
  <h2 class="card-title uppercase opacity-50">Expériences</h2>

  <ul class="timeline timeline-vertical timeline-compact">
    <li
      v-for="(experience, index) in experiences"
      :key="index"
      class="mb-4 last:mb-0 break-inside-avoid-page"
    >
      <hr />
      <!-- ************************************************************************************* -->
      <div class="timeline-start text-left flex flex-col gap-1 pl-2">
        <div class="text-lg font-semibold">
          {{ experience.company }}
        </div>
        <div class="flex items-center gap-2 font-semibold">
          <BriefcaseBusiness :size="14" :stroke-width="1" />
          {{ experience.role }}
        </div>
        <div class="flex items-center gap-2 text-xs text-base-content/50">
          <Calendar :size="14" :stroke-width="1" />
          {{ experience.period }}
        </div>
      </div>
      <!-- ************************************************************************************* -->
      <div class="timeline-middle">
        <Circle :size="16" class="text-secondary" />
      </div>
      <!-- ************************************************************************************* -->
      <div class="timeline-end w-full flex flex-col gap-2">
        <template v-for="(project, index) in experience.projects" :key="index">
          <div class="card bg-base-100 shadow">
            <div class="card-body p-2 md:p-4">
              <CardExperienceProject :project="project" />
            </div>
          </div>
        </template>
      </div>
      <!-- ************************************************************************************* -->
      <hr />
    </li>
  </ul>
</template>
