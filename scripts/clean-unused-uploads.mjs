// 扫描 docs/ 下所有文档与配置文件，自动清理 docs/public/uploads/ 中未被引用的图片
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const docsDir = path.join(root, 'docs')
const uploadsDir = path.join(docsDir, 'public/uploads')

if (!fs.existsSync(uploadsDir)) {
  process.exit(0)
}

const uploadFiles = fs.readdirSync(uploadsDir).filter(name => {
  if (name.startsWith('.')) return false
  const fullPath = path.join(uploadsDir, name)
  return fs.statSync(fullPath).isFile()
})

if (uploadFiles.length === 0) {
  console.log('[clean-unused-uploads] uploads/ 目录为空，无需清理')
  process.exit(0)
}

// 递归收集 docs/ 下需要扫描引用的文本文件（跳过构建产物与 vendor 第三方库）
const SKIP_DIRS = new Set(['dist', 'cache', 'uploads', 'vendor', 'node_modules', '.git'])
const TEXT_EXTS = new Set(['.md', '.mjs', '.js', '.ts', '.vue', '.json', '.yml', '.yaml', '.html', '.css'])

function collectSourceFiles(dir, result = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      collectSourceFiles(full, result)
    } else if (entry.isFile() && TEXT_EXTS.has(path.extname(entry.name).toLowerCase())) {
      result.push(full)
    }
  }
  return result
}

const sourceFiles = collectSourceFiles(docsDir)
const combinedContent = sourceFiles.map(f => fs.readFileSync(f, 'utf-8')).join('\n')

let removedCount = 0
let removedBytes = 0
const keptFiles = []

for (const name of uploadFiles) {
  // 同时兼容直接文件名与 URL 编码后的文件名
  const encodedName = encodeURIComponent(name)
  const isReferenced = combinedContent.includes(name) || (encodedName !== name && combinedContent.includes(encodedName))
  if (isReferenced) {
    keptFiles.push(name)
  } else {
    const filePath = path.join(uploadsDir, name)
    const size = fs.statSync(filePath).size
    fs.unlinkSync(filePath)
    removedCount++
    removedBytes += size
  }
}

const freedMB = (removedBytes / 1024 / 1024).toFixed(2)
if (removedCount > 0) {
  console.log(`[clean-unused-uploads] 已清理 ${removedCount} 张未引用图片（释放 ${freedMB} MB），保留 ${keptFiles.length} 张已引用图片`)
} else {
  console.log(`[clean-unused-uploads] 检测完毕，全部 ${keptFiles.length} 张图片均被引用，无冗余图片`)
}
