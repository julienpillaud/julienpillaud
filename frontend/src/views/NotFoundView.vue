<script setup lang="ts">
import { Undo2 } from '@lucide/vue'

document.title = 'Page introuvable'
</script>

<template>
  <div class="flex justify-center items-center min-h-screen p-3">
    <div class="card bg-base-200 shadow">
      <div class="card-body">
        <div class="flex flex-col items-center gap-4">
          <p class="text-2xl md:text-3xl font-medium tracking-tight">
            Vous ne devriez pas être là !
          </p>
          <div class="card-actions">
            <a href="/" class="btn btn-ghost">
              <Undo2 :size="28" :stroke-width="2.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
