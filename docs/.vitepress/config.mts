import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

// 自动从内容目录生成侧边栏：团队成员在后台新建的页面会自动出现
function scanDir(dir, section) {
  if (!fs.existsSync(dir)) return []
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.md') && f !== 'index.md')
    .map(f => {
      const slug = f.replace(/\.md$/, '')
      const content = fs.readFileSync(path.join(dir, f), 'utf-8')
      const title = content.match(/^title:\s*(.+)$/m)?.[1]?.trim() || slug
      return { text: title, link: `/${section}/${slug}` }
    })
    .sort((a, b) => a.text.localeCompare(b.text, 'zh'))
}

const wikiItems = scanDir(path.resolve(process.cwd(), 'docs/wiki'), 'wiki')
const tutorialItems = scanDir(path.resolve(process.cwd(), 'docs/tutorials'), 'tutorials')

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
      { text: '教程', link: '/tutorials/' },
      { text: '编辑', link: '/admin/', target: '_self' }
    ],

    sidebar: {
      '/wiki/': [
        {
          text: 'Wiki',
          items: [
            { text: 'Wiki 首页', link: '/wiki/' },
            ...wikiItems
          ]
        }
      ],
      '/tutorials/': [
        {
          text: '教程',
          items: [
            { text: '教程首页', link: '/tutorials/' },
            ...tutorialItems
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'qq', link: 'https://qm.qq.com/q/1mn4FppPPO' }
    ]
  }
})
