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
            summary: "{{fields.label}} → {{fields.folder}}"
            hint: "改完保存后：站点侧边栏与后台分区列表要等部署完成并刷新页面才生效。删除分区不会删除已写好的页面文件。"
            fields:
              - { label: "显示名称", name: "label", widget: "string" }
              - { label: "英文标识", name: "name", widget: "string", hint: "唯一标识，如 wiki / tutorials" }
              - { label: "内容目录", name: "folder", widget: "string", hint: "相对仓库根目录，如 docs/wiki" }

${sectionCollections}
`

fs.writeFileSync(outFile, yaml)
console.log(`[gen-admin-config] 已生成 config.yml（${sections.length} 个分区）`)
