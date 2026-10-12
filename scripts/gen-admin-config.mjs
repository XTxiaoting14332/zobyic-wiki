// 由 sections.json 生成 Decap CMS 的 config.yml（构建时运行）
// 团队成员在后台「分区管理」里增删分区 → 提交 sections.json → 重新构建时本脚本生成新 config.yml
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sectionsFile = path.join(root, 'docs/public/admin/sections.json')
const outFile = path.join(root, 'docs/public/admin/config.yml')

const sections = JSON.parse(fs.readFileSync(sectionsFile, 'utf-8')).sections || []

const sectionCollections = sections
  .filter(s => s.name && s.folder)
  .map(s => `  - name: "${s.name}"
    label: "${s.label || s.name}"
    label_singular: "页面"
    folder: "${s.folder}"
    create: true
    delete: true
    slug: "{{slug}}"
    fields:
      - { label: "标题", name: "title", widget: "string" }
      - { label: "简介", name: "description", widget: "string", required: false }
      - { label: "正文", name: "body", widget: "markdown" }`)
  .join('\n')

const yaml = `# ⚠️ 本文件由 scripts/gen-admin-config.mjs 从 sections.json 自动生成，请勿手动修改
# 要增删分区，请在后台「分区管理」里编辑，或直接改 docs/public/admin/sections.json
backend:
  name: github
  repo: XTxiaoting14332/zobyic-wiki
  branch: main
  base_url: https://wiki-gateway.zobyic.top
  auth_endpoint: auth
  api_root: https://wiki-gateway.zobyic.top
  site_domain: wiki.zobyic.top

media_folder: "docs/public/uploads"
public_folder: "/uploads"

# 后台界面语言（Decap 内置 zh_Hans 语言包）
locale: zh_Hans

logo_url: /logo.png

collections:
  - name: "settings"
    label: "分区管理"
    files:
      - name: "sections"
        label: "内容分区"
        file: "docs/public/admin/sections.json"
        fields:
          - label: "分区列表"
            name: "sections"
            widget: "list"
            summary: "{{fields.label}} (标识: {{fields.name}} ➜ 路径: {{fields.folder}})"
            hint: "保存后：站点侧边栏与后台分区列表将在 Vercel 自动部署完成（约1-2分钟）后刷新页面生效。删除分区不会删除已有页面文件。"
            fields:
              - { label: "显示名称", name: "label", widget: "string", hint: "用于导航栏和侧边栏展示，如：Wiki、教程、服务器规范" }
              - { label: "英文标识", name: "name", widget: "string", hint: "唯一标识，建议小写英文无空格，如：wiki、tutorials、rules" }
              - { label: "内容目录", name: "folder", widget: "string", hint: "相对仓库根目录的文件夹路径，如：docs/wiki、docs/tutorials" }

${sectionCollections}
`

fs.writeFileSync(outFile, yaml)
console.log(`[gen-admin-config] 已生成 config.yml（${sections.length} 个分区）`)

// 生成编辑器资源清单：供后台在加载编辑器时显示「已加载 / 总大小」进度
const adminDir = path.join(root, 'docs/public/admin')
const editorAssetPaths = [
  'vendor/vditor/dist/index.min.js',
  'vendor/vditor/dist/index.css',
  'vendor/vditor/dist/js/lute/lute.min.js',
  'vendor/vditor/dist/js/i18n/zh_CN.js',
  'vendor/vditor/dist/js/icons/material.js',
  'vendor/vditor/dist/css/content-theme/dark.css',
  'vendor/vditor/dist/css/content-theme/light.css',
]
const editorAssets = editorAssetPaths
  .map(rel => {
    const abs = path.join(adminDir, rel)
    return fs.existsSync(abs) ? { url: `/admin/${rel}`, size: fs.statSync(abs).size } : null
  })
  .filter(Boolean)
const manifestFile = path.join(adminDir, 'vendor/manifest.json')
fs.writeFileSync(manifestFile, JSON.stringify({ editorAssets }, null, 2) + '\n')
const totalMB = (editorAssets.reduce((sum, f) => sum + f.size, 0) / 1024 / 1024).toFixed(2)
console.log(`[gen-admin-config] 已生成 vendor/manifest.json（${editorAssets.length} 个文件，共 ${totalMB} MB）`)
