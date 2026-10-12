import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

// 自动从 docs/wiki/ 目录生成侧边栏：团队成员在后台新建的页面会自动出现
const wikiDir = path.resolve(process.cwd(), 'docs/wiki')
const wikiItems = fs.existsSync(wikiDir)
  ? fs.readdirSync(wikiDir)
      .filter(f => f.endsWith('.md') && f !== 'index.md')
      .map(f => {
        const slug = f.replace(/\.md$/, '')
        const content = fs.readFileSync(path.join(wikiDir, f), 'utf-8')
        const title = content.match(/^title:\s*(.+)$/m)?.[1]?.trim() || slug
        return { text: title, link: `/wiki/${slug}` }
      })
      .sort((a, b) => a.text.localeCompare(b.text, 'zh'))
  : []

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
      { text: 'Wiki', link: '/wiki/' },
      { text: '编辑', link: '/admin/', target: '_self' }
    ],

    sidebar: [
      {
        text: 'Wiki',
        items: [
          { text: 'Wiki 首页', link: '/wiki/' },
          ...wikiItems
        ]
      }
    ],

    socialLinks: [
      { icon: 'qq', link: 'https://qm.qq.com/q/1mn4FppPPO' }
    ]
  }
})
