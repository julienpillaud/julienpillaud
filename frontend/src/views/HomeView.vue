<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '@/services/api'
import ResumeCard from '@/components/ResumeCard.vue'
import CardSkills from '@/components/CardSkills.vue'
import CardMetadata from '@/components/CardMetadata.vue'
import CardExperiences from '@/components/CardExperiences.vue'
import CardLanguages from '@/components/CardLanguages.vue'
import CardEducation from '@/components/CardEducation.vue'
import type { Resume } from '@/types/resume'

const resume = ref<Resume | null>(null)

onMounted(async () => {
  const response = await api.get('/resume')
  resume.value = await response.data
  document.title = resume.value?.metadata.contact.full_name ?? ''
})
</script>

<template>
  <main class="max-w-4xl mx-auto flex flex-col gap-2 md:gap-4 px-3 py-4">
    <template v-if="resume">
      <ResumeCard>
        <CardMetadata :metadata="resume.metadata" />
      </ResumeCard>
      <ResumeCard>
        <CardSkills :skills="resume.skills" />
      </ResumeCard>
      <ResumeCard>
        <CardExperiences :experiences="resume.experiences" />
      </ResumeCard>
      <ResumeCard>
        <CardEducation :metadata="resume.metadata" />
      </ResumeCard>
      <ResumeCard>
        <CardLanguages :metadata="resume.metadata" />
      </ResumeCard>
    </template>
  </main>
</template>
