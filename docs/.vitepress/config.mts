import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

// 分区列表与后台「分区管理」共用同一份数据（docs/public/admin/sections.json）
// 团队成员在后台增删分区后，站点侧边栏/导航会在下次部署时自动更新
const sectionsFile = path.resolve(process.cwd(), 'docs/public/admin/sections.json')
const sections = fs.existsSync(sectionsFile)
  ? JSON.parse(fs.readFileSync(sectionsFile, 'utf-8')).sections || []
  : []

// 像素字体里没有的字符（emoji、✦ 等）会由系统字体显示，宽度带小数，把同一行后面的文字推到半像素上发虚。
// 渲染时把这些字符包进 <span class="fb">，按字数给整数宽度（样式见 theme/custom.css）。
// ignore-header 让右侧「本页目录」不显示这些字符（VitePress 生成目录时会跳过带这个类的元素）。
// 字体覆盖的范围从 theme/fonts.css 的 unicode-range 读取。
const fontRanges = [...fs.readFileSync(path.resolve(process.cwd(), 'docs/.vitepress/theme/fonts.css'), 'utf-8')
  .matchAll(/U\+([0-9A-F]+)(?:-([0-9A-F]+))?/g)]
  .map(m => [parseInt(m[1], 16), parseInt(m[2] ?? m[1], 16)])
const inFont = (ch: string) => [...ch].every(c => {
  const cp = c.codePointAt(0)!
  return fontRanges.some(([a, b]) => cp >= a && cp <= b)
})
const graphemes = new Intl.Segmenter('zh', { granularity: 'grapheme' })
const escapeHtml = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

// 返回转义后的 HTML；没有需要处理的字符时返回 null
function wrapFallback(text: string): string | null {
  let out = '', run: string[] = [], changed = false
  const flush = () => {
    if (!run.length) return
    out += `<span class="fb ignore-header" style="--n:${run.length}">${escapeHtml(run.join(''))}</span>`
    run = []
    changed = true
  }
  for (const { segment } of graphemes.segment(text)) {
    if (/^\s+$/.test(segment) || inFont(segment)) {
      flush()
      out += escapeHtml(segment)
    } else {
      run.push(segment)
    }
  }
  flush()
  return changed ? out : null
}

function fallbackGlyphPlugin(md: any) {
  // 放在最后执行：标题锚点（slug）已经按原文生成，不受影响
  md.core.ruler.push('fallback_glyph', (state: any) => {
    for (const block of state.tokens) {
      if (block.type !== 'inline' || !block.children) continue
      for (const t of block.children) {
        if (t.type !== 'text' && t.type !== 'code_inline') continue
        const html = wrapFallback(t.content)
        if (html === null) continue
        t.content = t.type === 'code_inline' ? `<code>${html}</code>` : html
        t.type = 'html_inline'
      }
    }
  })
}

const routeOf = folder => '/' + folder.replace(/^docs\//, '').replace(/\/$/, '') + '/'

function scanDir(dir: string, route: string, orderList: string[] = []) {
  if (!fs.existsSync(dir)) return []
  const files = fs.readdirSync(dir)
    .filter(f => f.endsWith('.md') && f !== 'index.md')
    .map(f => {
      const slug = f.replace(/\.md$/, '')
      const content = fs.readFileSync(path.join(dir, f), 'utf-8')
      const title = content.match(/^title:\s*(.+)$/m)?.[1]?.trim() || slug
      return { text: title, link: `${route}${slug}`, file: f }
    })

  if (Array.isArray(orderList) && orderList.length > 0) {
    files.sort((a, b) => {
      const idxA = orderList.indexOf(a.file)
      const idxB = orderList.indexOf(b.file)
      if (idxA !== -1 && idxB !== -1) return idxA - idxB
      if (idxA !== -1) return -1
      if (idxB !== -1) return 1
      return a.text.localeCompare(b.text, 'zh')
    })
  } else {
    files.sort((a, b) => a.text.localeCompare(b.text, 'zh'))
  }

  // 侧边栏用 v-html 显示标题，所以这里同样要处理字体里没有的字符
  return files.map(({ text, link }) => ({ text: wrapFallback(text) ?? escapeHtml(text), link }))
}

const sectionList = sections
  .filter((s: any) => s.name && s.folder)
  .map((s: any) => {
    const dir = path.resolve(process.cwd(), s.folder)
    return {
      label: s.label || s.name,
      route: routeOf(s.folder),
      // 分区首页（index.md）可能还没创建，导航/侧边栏不能引用不存在的页面
      hasIndex: fs.existsSync(path.join(dir, 'index.md')),
      items: scanDir(dir, routeOf(s.folder), s.order || []),
    }
  })

// 排版容器：::: large / small / center
// 只负责字号与对齐，不画边框（边框留给 VitePress 原生的提示/警告/折叠容器）。
// 后台新插入的字号已改为行内 HTML，这里保留容器是为了兼容此前已写入仓库的内容。
const CUSTOM_CONTAINERS = ['large', 'small', 'center']

function customContainersPlugin(md: any) {
  md.block.ruler.before('fence', 'custom_container', (state: any, startLine: number, endLine: number, silent: boolean) => {
    const start = state.bMarks[startLine] + state.tShift[startLine]
    const max = state.eMarks[startLine]
    const m = /^ {0,3}:::\s*([A-Za-z][\w-]*)\s*(.*)$/.exec(state.src.slice(start, max))
    if (!m || !CUSTOM_CONTAINERS.includes(m[1])) return false
    const name = m[1]
    const title = m[2].trim()

    let nextLine = startLine + 1
    let closed = false
    for (; nextLine < endLine; nextLine++) {
      const s = state.bMarks[nextLine] + state.tShift[nextLine]
      const e = state.eMarks[nextLine]
      if (/^:::\s*$/.test(state.src.slice(s, e))) {
        closed = true
        break
      }
    }
    if (!closed) return false
    if (silent) return true

    const open = state.push('custom_container_open', 'div', 1)
    open.attrSet('class', `custom-block-${name}`)
    open.map = [startLine, nextLine]

    // 起始行「::: large 文字」后面的文字并入正文，不再当作灰色小标题渲染
    const body = state.getLines(startLine + 1, nextLine, state.tShift[startLine], false).trim()
    const inner = title && body ? `${title}\n\n${body}` : title || body
    if (inner) {
      const html = state.push('html_block', '', 0)
      html.content = md.render(inner)
      html.map = [startLine + 1, nextLine]
    }

    state.push('custom_container_close', 'div', -1)
    state.line = nextLine + 1
    return true
  })
}

// 在页面渲染前设置主题，避免闪烁；和 theme/theme.ts 用同一个 localStorage 键。
// 后半段：像素字体只有在 1 个 CSS 像素对应整数个屏幕像素时才清晰，
// 125%、150% 这类缩放下给整页设 zoom，凑到最近的整数倍（和官网相同）。
const THEME_SCRIPT = `(function () {
  var p = 'system';
  try { p = localStorage.getItem('zobyic_theme') || 'system'; } catch (e) {}
  var dark = p === 'dark' || (p !== 'light' && matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.classList.toggle('dark', dark);
  var root = document.documentElement;
  function fit() {
    var dpr = window.devicePixelRatio || 1;
    var z = Math.max(1, Math.round(dpr)) / dpr;
    root.style.zoom = Math.abs(z - 1) < 0.01 ? '' : String(z);
    matchMedia('(resolution: ' + dpr + 'dppx)').addEventListener('change', fit, { once: true });
  }
  fit();
})();`

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Zobyic Realms Wiki",
  description: "Zobyic Realms官方Wiki",
  lang: 'zh-CN',
  vite: {
    plugins: [{
      // 线上的 Cloudflare 会把 /admin/ 指向 public/admin/index.html，但 dev 服务器会把它当成
      // VitePress 页面而显示 404，这里在开发时把它改写到后台页面
      name: 'admin-index',
      apply: 'serve',
      configureServer(server) {
        server.middlewares.use((req, _res, next) => {
          if (req.url === '/admin' || req.url?.startsWith('/admin/?') || req.url === '/admin/') {
            req.url = '/admin/index.html' + (req.url.split('?')[1] ? '?' + req.url.split('?')[1] : '')
          }
          next()
        })
      }
    }]
  },
  // 关闭 VitePress 自带的明暗开关，换成和官网一样的三档切换（theme/ThemeSwitch.vue）
  appearance: false,
  head: [
    ['link', { rel: 'icon', href: '/zbLOGO.png' }],
    ['link', { rel: 'preload', href: '/fonts/minecraft-0.woff2', as: 'font', type: 'font/woff2', crossorigin: '' }],
    ['script', {}, THEME_SCRIPT]
  ],
  markdown: {
    container: {
      tipLabel: '提示',
      infoLabel: '说明',
      warningLabel: '注意',
      dangerLabel: '警告',
      detailsLabel: '详情'
    },
    config: (md) => {
      customContainersPlugin(md)
      fallbackGlyphPlugin(md)
    }
  },
  themeConfig: {
    siteTitle: 'Zobyic Realms Wiki',
    logo: '/zbLOGO.png',
    nav: [
      { text: '主页', link: '/' },
      // 分区首页缺失时导航降级到分区第一页；完全没有页面的分区不显示入口（避免 404）
      ...sectionList.filter(s => s.hasIndex || s.items.length)
        .map(s => ({ text: s.label, link: s.hasIndex ? s.route : s.items[0].link })),
      { text: '编辑', link: '/admin/', target: '_self' }
    ],

    // 所有分区的页面列表始终显示在侧边栏（每个分区一组）
    sidebar: sectionList.filter(s => s.hasIndex || s.items.length).map(s => ({
      text: s.label,
      items: [...(s.hasIndex ? [{ text: '首页', link: s.route }] : []), ...s.items]
    })),

    outline: { label: '本页目录' },
    docFooter: { prev: '上一页', next: '下一页' },
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    notFound: {
      title: '页面不存在',
      quote: '这个页面可能已经改名或删除。',
      linkLabel: '返回首页',
      linkText: '返回首页'
    },

    socialLinks: [
      { icon: 'qq', link: 'https://qm.qq.com/q/1mn4FppPPO' }
    ]
  }
})
