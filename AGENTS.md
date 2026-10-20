# AGENTS.md

## 沟通风格（用户明确要求，务必遵守）
- 使用中性、专业、直接的表述；不要轻松、热情、亲切的语气。
- 任务结束时不要反问、不要征求下一步（如“要不要…？”“需要我…吗？”），除非用户明确要求给出选项。
- 不使用 emoji。

## 维基编写与内容规范（普通玩家视角，坚决遵守）
- 面向普通玩家受众，严禁写成技术文档或底层实现说明。
- 严禁包含代码变量名、常量、NBT键、内部世界名（如 `vh_world`、`vh_sanctuary`）、服务器 tick 周期判定、组件说明等底层实现细节。
- 严禁标注内部界面槽位编号（如“第 50 槽位”、“第 13 槽位”等）。
- 严禁滥用无意义的英文对照与英文括号（如 `(Bows)`、`(DoT)`、`(FFYL)`、`(Incendiary)` 等），统一使用自然中文表达。
- 装备名录严禁剧透隐藏/首领专属红字装备的名称、特技细节、数值与铭文台词。红字内容仅在 Boss 概览中简要提及战利品名称，保留玩家在游戏内的探索惊喜。

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
