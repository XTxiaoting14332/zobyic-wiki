// =============================================================
// Zobyic Realms Wiki — GitHub API 代理网关 (Cloudflare Worker)
// -------------------------------------------------------------
// 调用链: 浏览器(Decap CMS) -> 本 Worker -> api.github.com
//   /auth     团队登录页（共享口令，或 Cloudflare Access 免密），签发会话 JWT
//   其余路径   校验会话 JWT 后，注入你的 GitHub PAT 转发到 GitHub API
//
// 部署（在 proxy/ 目录下执行）:
//   wrangler deploy
//   wrangler secret put GITHUB_TOKEN      # 细粒度 PAT，仅授权 wiki 仓库 Contents 读+写
//   wrangler secret put SESSION_SECRET    # 会话签名密钥（随机长字符串）
//   wrangler secret put ADMIN_PASSWORD    # 团队成员共享登录口令
// 然后把 docs/public/admin/config.yml 里的代理三行启用并改成你的 worker 域名
// =============================================================

const GITHUB_API = 'https://api.github.com';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin');

    // CORS 预检
    if (request.method === 'OPTIONS') {
      return cors(new Response(null, { status: 204 }), origin, env);
    }

    const path = url.pathname;
    // 登录页/表单提交是浏览器整页流程（不是 CORS 调用），不受 Origin 白名单限制
    if (path === '/auth' || path === '/auth/') {
      return handleAuth(request, env, url);
    }

    // 只允许配置的站点跨域调用 API（浏览器请求会带 Origin）
    if (origin && !isAllowedOrigin(origin, env)) {
      return new Response('Forbidden: origin not allowed', { status: 403 });
    }

    if (path === '/' || path === '/health') {
      return cors(json({ service: 'zobyic-wiki-gateway', ok: true }), origin, env);
    }
    return handleApi(request, env, url, origin);
  },
};

// ---------------- 登录 ----------------

async function handleAuth(request, env, url) {
  const accessEmail = request.headers.get('Cf-Access-Authenticated-User-Email');

  if (request.method === 'GET') {
    const target = resolveRedirect(url.searchParams.get('redirect_uri'), env);
    if (target === null) return new Response('配置错误：ALLOWED_ORIGINS 未设置或 redirect_uri 非法', { status: 400 });
    if (accessEmail) return issueSession(target, env); // 已过 Cloudflare Access，免口令
    return html(loginPage(target, env));
  }

  if (request.method === 'POST') {
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';

    if (accessEmail) {
      const target = resolveRedirect((await request.formData()).get('redirect_uri'), env);
      if (target === null) return new Response('Invalid redirect_uri', { status: 400 });
      return issueSession(target, env);
    }

    if (await loginBlocked(env, ip)) {
      return html(loginPage(resolveRedirect(null, env) || '/', env, '失败次数过多，请 10 分钟后再试'));
    }

    const form = await request.formData();
    const target = resolveRedirect(form.get('redirect_uri'), env);
    if (target === null) return new Response('Invalid redirect_uri', { status: 400 });

    if (form.get('password') !== env.ADMIN_PASSWORD) {
      await recordLoginFail(env, ip);
      return html(loginPage(target, env, '口令错误，请重试'));
    }
    await clearLoginFails(env, ip);
    return issueSession(target, env);
  }

  return new Response('Method Not Allowed', { status: 405 });
}

function resolveRedirect(uri, env) {
  const origins = (env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  if (origins.length === 0) return null;
  const target = uri || `${origins[0]}/admin/`;
  try {
    const u = new URL(target);
    return isAllowedOrigin(u.origin, env) ? target : null;
  } catch {
    return null;
  }
}

async function issueSession(redirectUri, env) {
  const now = Math.floor(Date.now() / 1000);
  const ttl = parseInt(env.SESSION_TTL_SECONDS || '604800', 10) || 604800;
  const token = await signJwt({ sub: 'team', iat: now, exp: now + ttl }, env.SESSION_SECRET);
  const sep = redirectUri.includes('?') ? '&' : '?';
  return Response.redirect(`${redirectUri}${sep}provider=github&token=${encodeURIComponent(token)}&scope=repo`, 302);
}

// ---------------- API 代理 ----------------

async function handleApi(request, env, url, origin) {
  // 1) 会话校验：必须是本网关签发的、未过期的 JWT
  const auth = request.headers.get('Authorization') || '';
  const token = auth.startsWith('Bearer ') ? auth.slice(7) : '';
  if (!(await verifyJwt(token, env.SESSION_SECRET))) {
    return cors(json({ message: '会话无效或已过期，请重新登录' }, 401), origin, env);
  }

  // 2) 路径白名单：只放行 /user 与配置的 wiki 仓库
  const repo = (env.ALLOWED_REPO || '').trim().toLowerCase();
  const p = url.pathname;
  const allowed = p === '/user' || p === '/rate_limit'
    || (repo && (p === `/repos/${repo}` || p.startsWith(`/repos/${repo}/`)));
  if (!allowed) {
    return cors(json({ message: 'Forbidden: path not allowed' }, 403), origin, env);
  }

  // 3) 可选限流（需要 KV binding `LIMITS`，未配置时自动跳过）
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (await rateLimited(env, ip)) {
    return cors(json({ message: '请求过于频繁，请稍后再试' }, 429), origin, env);
  }

  // 4) 注入 owner 的 PAT 转发到 GitHub（忽略客户端发来的 Authorization）
  const target = new URL(GITHUB_API + p);
  target.search = url.search;
  const headers = new Headers();
  headers.set('Authorization', `Bearer ${env.GITHUB_TOKEN}`);
  headers.set('User-Agent', 'zobyic-wiki-gateway'); // GitHub API 强制要求 UA
  headers.set('Accept', request.headers.get('Accept') || 'application/vnd.github+json');
  const ct = request.headers.get('Content-Type');
  if (ct) headers.set('Content-Type', ct);
  const inm = request.headers.get('If-None-Match');
  if (inm) headers.set('If-None-Match', inm);

  const hasBody = !['GET', 'HEAD'].includes(request.method);
  const upstream = await fetch(target.toString(), {
    method: request.method,
    headers,
    body: hasBody ? request.body : undefined,
  });

  // 5) 透传上游响应（附 CORS 头）
  return cors(new Response(upstream.body, { status: upstream.status, headers: upstream.headers }), origin, env);
}

// ---------------- 工具 ----------------

function isAllowedOrigin(origin, env) {
  const allowed = (env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  return allowed.includes(origin);
}

function cors(res, origin, env) {
  const headers = new Headers(res.headers);
  if (origin && isAllowedOrigin(origin, env)) {
    headers.set('Access-Control-Allow-Origin', origin);
    headers.set('Vary', 'Origin');
  }
  headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Authorization, Content-Type, Accept, If-None-Match');
  headers.set('Access-Control-Max-Age', '86400');
  return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}

function html(body) {
  return new Response(body, { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
}

// 可选限流：每 IP 每分钟 600 次 API 请求（正常编辑远用不到这个量）
async function rateLimited(env, ip) {
  if (!env.LIMITS) return false;
  const key = `rl:${ip}:${Math.floor(Date.now() / 60000)}`;
  const n = parseInt((await env.LIMITS.get(key)) || '0', 10);
  if (n >= 600) return true;
  await env.LIMITS.put(key, String(n + 1), { expirationTtl: 120 });
  return false;
}

// 登录失败熔断：每 IP 10 分钟内最多 5 次错误
async function loginBlocked(env, ip) {
  if (!env.LIMITS) return false;
  const n = parseInt((await env.LIMITS.get(`fail:${ip}`)) || '0', 10);
  return n >= 5;
}

async function recordLoginFail(env, ip) {
  if (!env.LIMITS) return;
  const key = `fail:${ip}`;
  const n = parseInt((await env.LIMITS.get(key)) || '0', 10);
  await env.LIMITS.put(key, String(n + 1), { expirationTtl: 600 });
}

async function clearLoginFails(env, ip) {
  if (!env.LIMITS) return;
  await env.LIMITS.delete(`fail:${ip}`);
}

// ---------------- JWT (HS256, 零依赖) ----------------

const enc = new TextEncoder();

function b64url(input) {
  const bytes = typeof input === 'string' ? enc.encode(input) : input;
  let bin = '';
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function b64urlDecode(str) {
  return atob(str.replace(/-/g, '+').replace(/_/g, '/'));
}

async function hmacSha256(secret, data) {
  const key = await crypto.subtle.importKey(
    'raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign'],
  );
  return new Uint8Array(await crypto.subtle.sign('HMAC', key, enc.encode(data)));
}

async function signJwt(payload, secret) {
  const header = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const body = b64url(JSON.stringify(payload));
  const sig = b64url(await hmacSha256(secret, `${header}.${body}`));
  return `${header}.${body}.${sig}`;
}

async function verifyJwt(token, secret) {
  if (!token) return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [header, body, sig] = parts;
  const expected = b64url(await hmacSha256(secret, `${header}.${body}`));
  if (sig !== expected) return null;
  try {
    const payload = JSON.parse(b64urlDecode(body));
    const now = Math.floor(Date.now() / 1000);
    if (typeof payload.exp !== 'number' || payload.exp < now) return null;
    return payload;
  } catch {
    return null;
  }
}

// ---------------- 登录页 ----------------

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function loginPage(redirectUri, env, error = '') {
  return `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Wiki 内容管理 - 登录</title>
<style>
  body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #0f1115; color: #e6e6e6; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
  .card { background: #1a1d24; border: 1px solid #2a2f3a; border-radius: 12px; padding: 32px; width: 320px; }
  h1 { font-size: 18px; margin: 0 0 4px; }
  p { color: #9aa3b2; font-size: 13px; margin: 0 0 20px; }
  input[type=password] { width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 8px; border: 1px solid #333a47; background: #0f1115; color: #e6e6e6; font-size: 14px; }
  button { width: 100%; margin-top: 14px; padding: 10px; border: 0; border-radius: 8px; background: #3b82f6; color: #fff; font-size: 14px; cursor: pointer; }
  button:hover { background: #2f6fe0; }
  .err { color: #f87171; font-size: 13px; margin-top: 12px; }
</style>
</head>
<body>
<div class="card">
  <h1>Wiki 内容管理</h1>
  <p>请输入团队共享口令登录</p>
  ${error ? `<div class="err">${error}</div>` : ''}
  <form method="POST" action="/auth">
    <input type="hidden" name="redirect_uri" value="${escapeHtml(redirectUri)}">
    <input type="password" name="password" placeholder="登录口令" autofocus required>
    <button type="submit">登录</button>
  </form>
</div>
</body>
</html>`;
}

// 导出供本地测试
export { signJwt, verifyJwt };