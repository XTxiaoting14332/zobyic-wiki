import DefaultTheme from 'vitepress/theme'
import './fonts.css'
import 'viewerjs/dist/viewer.css'
import './custom.css'
import Viewer from 'viewerjs'
import { h, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'
import ThemeSwitch from './ThemeSwitch.vue'
import { snap, snapOnResize } from './snap'

export default {
  extends: DefaultTheme,
  // 主题切换：宽屏放在顶栏，窄屏放在展开的菜单里（custom.css 按宽度显示其中一个）
  Layout: () =>
    h(DefaultTheme.Layout, null, {
      'nav-bar-content-after': () => h('div', { class: 'theme-bar' }, h(ThemeSwitch)),
      'nav-screen-content-after': () => h('div', { class: 'theme-screen' }, h(ThemeSwitch))
    }),
  setup() {
    const route = useRoute()
    let viewerInstance: Viewer | null = null

    const initViewer = () => {
      if (typeof window === 'undefined') return
      if (viewerInstance) {
        viewerInstance.destroy()
        viewerInstance = null
      }
      const el = document.querySelector('.vp-doc')
      if (!el) return

      viewerInstance = new Viewer(el as HTMLElement, {
        button: true,       // 右上角关闭按钮
        navbar: false,      // 关闭底部缩略图，保持纯净视窗
        title: false,       // 关闭图片标题
        toolbar: {
          zoomIn: 1,
          zoomOut: 1,
          oneToOne: 1,
          reset: 1,
        },
        zoomRatio: 0.15,    // 滚轮缩放步长
        minZoomRatio: 0.1,  // 最小缩放比例
        maxZoomRatio: 6.0,  // 最大缩放至 600%，方便看清工业蓝图微小构件
        movable: true,      // 放大后支持鼠标拖拽平移
        zoomable: true,     // 支持滚轮与手势无级缩放
        rotatable: false,   // 禁用旋转
        scalable: false,    // 禁用镜像翻转
        transition: false,  // 关闭补间动画，打开和缩放都直接切换
        filter(image: HTMLImageElement) {
          return !image.classList.contains('no-zoom') && !image.closest('a')
        }
      })
    }

    onMounted(() => {
      initViewer()
      // 字体加载完成后表格列宽会变，所以等字体就绪再对齐
      document.fonts.ready.then(snap)
      snapOnResize()
    })

    watch(
      () => route.path,
      () =>
        nextTick(() => {
          initViewer()
          document.fonts.ready.then(snap)
        })
    )
  }
}


