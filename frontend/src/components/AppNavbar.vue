<script setup lang="ts">
import { ref, watch } from 'vue'
import { Moon, Sun } from '@lucide/vue'

type Theme = 'light' | 'dark'

function getInitialTheme(): Theme {
  const stored = localStorage.getItem('theme') as Theme | null
  if (stored === 'light' || stored === 'dark') return stored
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const theme = ref<Theme>(getInitialTheme())

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

watch(
  theme,
  (value) => {
    document.documentElement.setAttribute('data-theme', value)
    localStorage.setItem('theme', value)
  },
  { immediate: true },
)
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm sticky top-0 z-50">
    <div class="flex-1"></div>
    <div class="flex-none px-2">
      <div
        class="tooltip tooltip-left"
        :data-tip="`Passer en mode ${theme === 'light' ? 'dark' : 'light'}`"
      >
        <Sun v-if="theme === 'light'" class="cursor-pointer" @click="toggleTheme" />
        <Moon v-else class="cursor-pointer" @click="toggleTheme" />
      </div>
    </div>
  </div>
</template>
