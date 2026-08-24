import { ref, watch } from 'vue'

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

export function useTheme() {
  return {
    theme,
    toggleTheme,
  }
}
