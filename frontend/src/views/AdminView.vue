<script setup lang="ts">
import {BookOpen, BriefcaseBusiness, Languages, User, Wrench} from '@lucide/vue'
</script>

<template>
  <main class="max-w-2xl mx-auto px-2 py-6 flex flex-col gap-6">
    <h1 class="text-2xl font-bold">Administration</h1>
    <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
      <a
          class="card bg-base-200 border border-base-300 hover:border-primary hover:bg-base-300 transition-colors"
      >
        <div class="card-body">
          <div class="flex items-center gap-2">
            <User class="text-primary"/>
            <span class="font-semibold">Profil</span>
          </div>
        </div>
      </a>
      <a
          class="card bg-base-200 border border-base-300 hover:border-primary hover:bg-base-300 transition-colors"
      >
        <div class="card-body">
          <div class="flex items-center gap-2">
            <Wrench class="text-primary"/>
            <span class="font-semibold">Compétences</span>
          </div>
        </div>
      </a>
      <a
          class="card bg-base-200 border border-base-300 hover:border-primary hover:bg-base-300 transition-colors"
      >
        <div class="card-body">
          <div class="flex items-center gap-2">
            <BriefcaseBusiness class="text-primary"/>
            <span class="font-semibold">Expériences</span>
          </div>
        </div>
      </a>
      <a
          class="card bg-base-200 border border-base-300 hover:border-primary hover:bg-base-300 transition-colors"
      >
        <div class="card-body">
          <div class="flex items-center gap-2">
            <BookOpen class="text-primary"/>
            <span class="font-semibold">Formation</span>
          </div>
        </div>
      </a>
      <a
          class="card bg-base-200 border border-base-300 hover:border-primary hover:bg-base-300 transition-colors"
      >
        <div class="card-body">
          <div class="flex items-center gap-2">
            <Languages class="text-primary"/>
            <span class="font-semibold">Langues</span>
          </div>
        </div>
      </a>
    </div>
  </main>
</template>
