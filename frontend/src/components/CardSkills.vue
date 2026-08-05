<script setup lang="ts">
import type { SkillCategory } from '@/types/resume'

defineProps<{
  skills: SkillCategory[]
}>()
</script>

<template>
  <h2 class="card-title uppercase opacity-50">Compétences</h2>

  <ul class="space-y-3">
    <li v-for="(skill_group, index) in skills" :key="index">
      <p class="text-sm font-medium mb-2">{{ skill_group.name }}</p>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="skill in skill_group.skills"
          :key="skill.name"
          class="px-2 py-0 text-primary rounded border border-primary"
        >
          {{ skill.name }}
        </span>
      </div>
    </li>
  </ul>
</template>
