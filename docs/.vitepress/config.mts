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

function scanDir(dir, route) {
  if (!fs.existsSync(dir)) return []
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.md') && f !== 'index.md')
    .map(f => {
      const slug = f.replace(/\.md$/, '')
      const content = fs.readFileSync(path.join(dir, f), 'utf-8')
      const title = content.match(/^title:\s*(.+)$/m)?.[1]?.trim() || slug
      return { text: title, link: `${route}${slug}` }
    })
    .sort((a, b) => a.text.localeCompare(b.text, 'zh'))
}

const sectionList = sections
  .filter(s => s.name && s.folder)
  .map(s => ({
    label: s.label || s.name,
    route: routeOf(s.folder),
    items: scanDir(path.resolve(process.cwd(), s.folder), routeOf(s.folder)),
  }))

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Zobyic Realms Wiki",
  description: "Zobyic Realms官方Wiki",
  head: [
    ['link', { rel: 'icon', href: '/zbLOGO.png' }]
  ],
  themeConfig: {
    siteTitle: 'Zobyic Realms Wiki',
    logo: '/zbLOGO.png',
    nav: [
      { text: '主页', link: '/' },
      ...sectionList.map(s => ({ text: s.label, link: s.route })),
      { text: '编辑', link: '/admin/', target: '_self' }
    ],

    sidebar: Object.fromEntries(
      sectionList.map(s => [
        s.route,
        [{ text: s.label, items: [{ text: '首页', link: s.route }, ...s.items] }]
      ])
    ),

    socialLinks: [
      { icon: 'qq', link: 'https://qm.qq.com/q/1mn4FppPPO' }
    ]
  }
})