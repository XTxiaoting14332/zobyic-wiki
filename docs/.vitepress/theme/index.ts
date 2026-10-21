import DefaultTheme from 'vitepress/theme'
import './custom.css'
import 'viewerjs/dist/viewer.css'
import Viewer from 'viewerjs'
import { onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'

export default {
  extends: DefaultTheme,
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
        transition: true,   // 开启平滑补间动画
        filter(image: HTMLImageElement) {
          return !image.classList.contains('no-zoom') && !image.closest('a')
        }
      })
    }

    onMounted(() => {
      initViewer()
    })

    watch(
      () => route.path,
      () => nextTick(() => initViewer())
    )
  }
}


