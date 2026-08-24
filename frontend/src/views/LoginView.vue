<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { TriangleAlert } from '@lucide/vue'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  loading.value = true
  error.value = ''

  try {
    const params = new URLSearchParams()
    params.append('username', email.value)
    params.append('password', password.value)

    await api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    router.push('/admin')
  } catch {
    error.value = 'Email ou mot de passe incorrect'
    password.value = ''
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex justify-center items-center min-h-screen">
    <form @submit.prevent="handleSubmit">
      <div class="card bg-base-200 w-sm shadow">
        <div class="card-body">
          <input
            id="email"
            v-model="email"
            type="text"
            class="input w-full"
            placeholder="Username"
            required
          />
          <input
            id="password"
            v-model="password"
            type="password"
            class="input w-full"
            placeholder="Password"
            required
          />
          <div v-if="error" role="alert" class="alert alert-error alert-soft">
            <TriangleAlert />
            <span>{{ error }}</span>
          </div>
          <button :disabled="loading" type="submit" class="btn btn-primary">Login</button>
        </div>
      </div>
    </form>
  </div>
</template>
