<script setup lang="ts">
import type { Metadata } from '@/types/resume'
import { Laptop, MapPin } from '@lucide/vue'
import IconGithub from '@/components/icons/IconGithub.vue'
import IconMail from '@/components/icons/IconMail.vue'
import IconLinkedin from '@/components/icons/IconLinkedin.vue'

defineProps<{
  metadata: Metadata
}>()
</script>

<template>
  <div class="flex flex-col gap-4">
    <!-- ******************************************************************* -->
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-extrabold text-base-content">
        {{ metadata.contact.full_name }}
      </h1>
      <div v-if="metadata.contact.available" class="flex items-center gap-2">
        <div class="status status-success status-lg"></div>
        <div
          class="badge badge-sm badge-success badge-outline hidden sm:inline font-semibold uppercase tracking-wider"
        >
          Disponible
        </div>
      </div>
    </div>
    <!-- ******************************************************************* -->
    <div class="flex items-center gap-3 text-xl font-semibold text-base-content/80">
      <Laptop class="size-4 text-secondary" />
      <div>
        {{ metadata.contact.job_title }}
      </div>
    </div>
    <!-- ******************************************************************* -->
    <div class="flex items-center gap-3 text-base font-normal text-base-content/60">
      <MapPin class="size-4 text-secondary" />
      <div>{{ metadata.contact.location }} · {{ metadata.contact.remote }}</div>
    </div>
    <!-- ******************************************************************* -->
    <div class="flex gap-6">
      <a :href="`mailto:${metadata.contact.email}`" class="btn btn-circle btn-soft">
        <IconMail class="text-secondary" />
      </a>
      <a
        :href="`https://github.com/${metadata.contact.github_username}`"
        target="_blank"
        class="btn btn-circle btn-soft"
      >
        <IconGithub class="text-secondary" />
      </a>
      <a
        :href="`https://www.linkedin.com/in/${metadata.contact.linkedin_username}`"
        target="_blank"
        class="btn btn-circle btn-soft"
      >
        <IconLinkedin class="text-secondary" />
      </a>
    </div>
    <!-- ******************************************************************* -->
  </div>
</template>
