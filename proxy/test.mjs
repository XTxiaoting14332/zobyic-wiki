// Zobyic wiki 网关本地测试（Node 18+）
import worker, { signJwt, verifyJwt } from './src/index.js';

const env = {
  ALLOWED_ORIGINS: 'https://wiki.example.com',
  ALLOWED_REPO: 'owner/zobyic-wiki',
  ADMIN_PASSWORD: 'hunter2',
  SESSION_SECRET: 'test-session-secret',
  SESSION_TTL_SECONDS: '3600',
  GITHUB_TOKEN: 'ghp_FAKE_TEST',
};

let pass = 0, fail = 0;
function check(name, cond) {
  if (cond) { pass++; console.log(`  ✓ ${name}`); }
  else { fail++; console.log(`  ✗ ${name}`); }
}

// ---- JWT 单元测试 ----
console.log('[JWT]');
{
  const t = await signJwt({ sub: 'team', iat: 1, exp: 9999999999 }, env.SESSION_SECRET);
  const ok = await verifyJwt(t, env.SESSION_SECRET);
  check('签发/验证 round-trip', ok && ok.sub === 'team');
  check('错误密钥被拒绝', (await verifyJwt(t, 'wrong-secret')) === null);
  check('篡改签名被拒绝', (await verifyJwt(t.slice(0, -6) + 'AAAAAA', env.SESSION_SECRET)) === null);
  const expired = await signJwt({ sub: 'team', iat: 1, exp: 1 }, env.SESSION_SECRET);
  check('过期 token 被拒绝', (await verifyJwt(expired, env.SESSION_SECRET)) === null);
  check('空 token 被拒绝', (await verifyJwt('', env.SESSION_SECRET)) === null);
}

// ---- 登录流程 ----
console.log('[登录]');
const base = 'https://proxy.example.com';
const adminUri = encodeURIComponent('https://wiki.example.com/admin/');

{
  const res = await worker.fetch(new Request(`${base}/auth?redirect_uri=${adminUri}&scope=repo&site_domain=wiki.example.com`), env);
  const body = await res.text();
  check('GET /auth 返回登录页', res.status === 200 && body.includes('登录口令'));
  check('登录页不泄露口令', !body.includes('hunter2'));
}

let sessionToken = null;
{
  const wrong = new URLSearchParams({ password: 'nope', redirect_uri: 'https://wiki.example.com/admin/' });
  const res = await worker.fetch(new Request(`${base}/auth`, { method: 'POST', body: wrong, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }), env);
  const body = await res.text();
  check('错误口令留在登录页', res.status === 200 && body.includes('口令错误'));
}

{
  const good = new URLSearchParams({ password: 'hunter2', redirect_uri: 'https://wiki.example.com/admin/' });
  const res = await worker.fetch(new Request(`${base}/auth`, { method: 'POST', body: good, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }), env);
  check('正确口令 -> 302 跳回 admin', res.status === 302);
  const loc = res.headers.get('location') || '';
  check('带 provider/token/scope 参数', loc.includes('provider=github') && loc.includes('token=') && loc.includes('scope=repo'));
  sessionToken = new URL(loc).searchParams.get('token');
  check('token 是合法 JWT', sessionToken && (await verifyJwt(sessionToken, env.SESSION_SECRET)) !== null);
}

{
  const bad = new URLSearchParams({ password: 'hunter2', redirect_uri: 'https://evil.com/admin/' });
  const res = await worker.fetch(new Request(`${base}/auth`, { method: 'POST', body: bad, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }), env);
  check('恶意 redirect_uri 被拒绝', res.status === 400);
}

{
  const res = await worker.fetch(new Request(`${base}/auth`), env);
  const body = await res.text();
  check('无 redirect_uri 时回退到默认后台地址', res.status === 200 && body.includes('value="https://wiki.example.com/admin/"'));
}

{
  const emptyEnv = { ...env, ALLOWED_ORIGINS: '' };
  const res = await worker.fetch(new Request(`${base}/auth`), emptyEnv);
  check('未配置 origins 时给出配置错误', res.status === 400);
}

// ---- API 转发（mock 上游）----
console.log('[API 代理]');
const calls = [];
const realFetch = globalThis.fetch;
globalThis.fetch = async (url, init) => {
  calls.push({ url: String(url), method: init?.method || 'GET', headers: init?.headers });
  return new Response(JSON.stringify({ login: 'owner', id: 1 }), { status: 200, headers: { 'Content-Type': 'application/json' } });
};
try {
  {
    const res = await worker.fetch(new Request(`${base}/user`, { headers: { Authorization: `Bearer ${sessionToken}`, Origin: 'https://wiki.example.com' } }), env);
    const body = await res.json();
    check('GET /user 转发成功', res.status === 200 && body.login === 'owner');
    check('上游收到注入的 PAT', calls[0]?.headers?.get?.('Authorization') === 'Bearer ghp_FAKE_TEST');
    check('上游地址正确', calls[0]?.url === 'https://api.github.com/user');
    check('响应带 CORS 头', res.headers.get('Access-Control-Allow-Origin') === 'https://wiki.example.com');
  }
  {
    const res = await worker.fetch(new Request(`${base}/repos/owner/zobyic-wiki/git/refs/heads/main`, { headers: { Authorization: `Bearer ${sessionToken}` } }), env);
    check('仓库路径放行', res.status === 200);
  }
  {
    const res = await worker.fetch(new Request(`${base}/repos/other/repo/contents/x.md`, { headers: { Authorization: `Bearer ${sessionToken}` } }), env);
    check('非白名单仓库被拦截 403', res.status === 403);
  }
  {
    const res = await worker.fetch(new Request(`${base}/user`), env);
    check('无会话 token -> 401', res.status === 401);
  }
  {
    const res = await worker.fetch(new Request(`${base}/user`, { headers: { Authorization: `Bearer ${sessionToken}`, Origin: 'https://evil.com' } }), env);
    check('非法 Origin -> 403', res.status === 403);
  }
  {
    const res = await worker.fetch(new Request(`${base}/user`, { method: 'OPTIONS', headers: { Origin: 'https://wiki.example.com', 'Access-Control-Request-Method': 'PUT' } }), env);
    check('OPTIONS 预检放行', res.status === 204 && res.headers.get('Access-Control-Allow-Headers')?.includes('Authorization'));
  }
  {
    const tampered = sessionToken.slice(0, -6) + 'ZZZZZZ';
    const res = await worker.fetch(new Request(`${base}/user`, { headers: { Authorization: `Bearer ${tampered}` } }), env);
    check('伪造会话被拒 401', res.status === 401);
  }
} finally {
  globalThis.fetch = realFetch;
}

console.log(`\n结果: ${pass} 通过, ${fail} 失败`);
process.exit(fail ? 1 : 0);