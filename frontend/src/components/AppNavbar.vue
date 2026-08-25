<script setup lang="ts">
import {useRoute, useRouter} from 'vue-router'
import {useTheme} from '@/composables/useTheme'
import api from '@/services/api'
import {Moon, Sun} from '@lucide/vue'

const route = useRoute()
const router = useRouter()
const {theme, toggleTheme} = useTheme()

async function logout() {
  await api.post('/auth/logout')
  router.push('/login')
}
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm sticky top-0 z-50">
    <div class="flex flex-1 gap-2">
      <a
          v-if="route.name === 'admin'"
          href="/"
          class="btn btn-primary text-xs font-semibold uppercase tracking-wider"
      >
        CV
      </a>
      <button
          v-if="route.name === 'admin'"
          @click="logout"
          class="btn btn-error text-xs font-semibold uppercase tracking-wider"
      >
        Logout
      </button>
    </div>
    <div class="flex-none px-2">
      <div
          class="tooltip tooltip-left"
          :data-tip="`Passer en mode ${theme === 'light' ? 'dark' : 'light'}`"
      >
        <Sun v-if="theme === 'light'" class="cursor-pointer" @click="toggleTheme"/>
        <Moon v-else class="cursor-pointer" @click="toggleTheme"/>
      </div>
    </div>
  </div>
</template>
