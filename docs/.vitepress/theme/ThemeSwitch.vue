<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { initTheme, pref, setTheme, type Pref } from './theme'

const THEMES: { id: Pref; long: string; short: string }[] = [
  { id: 'light', long: '浅色', short: '浅色' },
  { id: 'dark', long: '暗色', short: '暗色' },
  { id: 'system', long: '跟随系统', short: '系统' }
]

// 顶栏放不下三个按钮时（1024–1279px）只显示一个按钮，点一下换到下一档
const current = computed(() => THEMES.findIndex((t) => t.id === pref.value))
const next = () => setTheme(THEMES[(current.value + 1) % THEMES.length].id)

onMounted(initTheme)
</script>

<template>
  <div class="ThemeSwitch" role="group" aria-label="颜色主题">
    <button
      v-for="t in THEMES"
      :key="t.id"
      type="button"
      :aria-pressed="pref === t.id"
      @click="setTheme(t.id)"
    >
      <span class="long">{{ t.long }}</span>
      <span class="short">{{ t.short }}</span>
    </button>
  </div>
  <button type="button" class="ThemeCycle" :title="`颜色主题：${THEMES[current].long}，点击切换`" @click="next">
    {{ THEMES[current].short }}
  </button>
</template>
