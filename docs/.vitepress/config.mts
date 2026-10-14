import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

// 分区列表与后台「分区管理」共用同一份数据（docs/public/admin/sections.json）
// 团队成员在后台增删分区后，站点侧边栏/导航会在下次部署时自动更新
const sectionsFile = path.resolve(process.cwd(), 'docs/public/admin/sections.json')
const sections = fs.existsSync(sectionsFile)
  ? JSON.parse(fs.readFileSync(sectionsFile, 'utf-8')).sections || []
  : []

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

  return files.map(({ text, link }) => ({ text, link }))
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

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Zobyic Realms Wiki",
  description: "Zobyic Realms官方Wiki",
  head: [
    ['link', { rel: 'icon', href: '/zbLOGO.png' }]
  ],
  markdown: {
    config: (md) => {
      customContainersPlugin(md)
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

    socialLinks: [
      { icon: 'qq', link: 'https://qm.qq.com/q/1mn4FppPPO' }
    ]
  }
})
