import { ref } from 'vue'

// 和官网一致的三档主题。初始主题由 config.mts 里 head 的内联脚本在渲染前设置，
// 这里只负责切换和保存。站点关闭了 VitePress 自带的明暗开关（appearance: false）。
export type Pref = 'light' | 'dark' | 'system'

const KEY = 'zobyic_theme'

// 顶栏和移动端菜单里各有一个切换按钮，共用这一份状态
export const pref = ref<Pref>('system')

let mq: MediaQueryList | null = null

function apply() {
  const dark = pref.value === 'dark' || (pref.value === 'system' && !!mq?.matches)
  document.documentElement.classList.toggle('dark', dark)
}

export function initTheme() {
  if (mq) return
  mq = matchMedia('(prefers-color-scheme: dark)')
  mq.addEventListener('change', apply)
  try {
    const v = localStorage.getItem(KEY)
    if (v === 'light' || v === 'dark' || v === 'system') pref.value = v
  } catch {
    // 隐私模式下 localStorage 可能不可用
  }
}

export function setTheme(p: Pref) {
  pref.value = p
  try {
    localStorage.setItem(KEY, p)
  } catch {
    // 同上
  }
  apply()
}
