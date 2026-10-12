# AGENTS.md

## 沟通风格（用户明确要求，务必遵守）
- 使用中性、专业、直接的表述；不要轻松、热情、亲切的语气。
- 任务结束时不要反问、不要征求下一步（如“要不要…？”“需要我…吗？”），除非用户明确要求给出选项。
- 不使用 emoji。

## 项目结构
- VitePress 站点：`docs/`（首页 + `docs/wiki/`、`docs/tutorials/` 等内容分区）
- Decap CMS 后台：`docs/public/admin/`（index.html + 自托管 decap-cms.js + sections.json）
- 代理网关：`proxy/`（Cloudflare Worker，源文件 `proxy/src/index.js`）
- 部署：Vercel（`vercel.json`，站点 https://wiki.zobyic.top，网关 https://wiki-gateway.zobyic.top）

## 构建与验证
- 构建站点：`npm run docs:build`（会先运行 `scripts/gen-admin-config.mjs` 由 `sections.json` 生成 `docs/public/admin/config.yml` 与 `vendor/manifest.json`）
- 本地预览：`npm run docs:dev` / `npm run docs:preview`
- 网关测试：`node proxy/test.mjs`

## 部署（Cloudflare Workers）
- 站点 Worker：`zobyic-wiki`，绑定自定义域名 `wiki.zobyic.top`
  - 配置在仓库根目录 `wrangler.toml`（assets 目录 `docs/.vitepress/dist`）
  - 部署：`npm run docs:build && npx wrangler deploy`（需 `CLOUDFLARE_API_TOKEN`）
  - 缓存头由 `docs/public/_headers` 提供（CF 静态资源会读取该文件；Vercel 的 `vercel.json` 已不再生效）
  - 若要「推送即自动部署」，需在 CF 控制台为该 Worker 配置 Workers Builds（Build 命令 `npm run docs:build`，Deploy 命令 `npx wrangler deploy`）
- 网关 Worker：`zobyic-wiki-gateway`，配置在 `proxy/wrangler.toml`，部署：`cd proxy && npx wrangler deploy`

## 关键机制
- 内容分区数据源：`docs/public/admin/sections.json`（后台「分区管理」集合可编辑，构建时生成 config.yml 与站点导航/侧边栏）
- 不要用 `window.CMS_CONFIG` 注入配置：该路径会跳过 Decap 的配置归一化，集合会缺 `type` 字段而崩溃。
- 网关代提交时会把 commit 作者改写为 Vercel 账号关联身份（`COMMIT_AUTHOR_NAME/EMAIL`），否则 Vercel 部署会因提交作者校验失败。
