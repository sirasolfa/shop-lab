// 이미지 URL 프록시 — 브라우저에서 CORS로 막히는 이미지(운영 shop-api 등)를 서버에서 받아 같은 출처로 돌려준다.
// 사내 전용(Vercel 로그인 뒤)이지만 열린 프록시가 되지 않도록 https·공인 IP·이미지·용량만 허용한다.
const dns = require('dns').promises;
const net = require('net');

const MAX_BYTES = 20 * 1024 * 1024;
const MAX_REDIRECTS = 3;
const TIMEOUT_MS = 10000;

function isPrivateIp(ip) {
  if (net.isIPv4(ip)) {
    const [a, b] = ip.split('.').map(Number);
    return a === 0 || a === 10 || a === 127 || (a === 100 && b >= 64 && b <= 127) || (a === 169 && b === 254) ||
      (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168) || (a === 198 && (b === 18 || b === 19)) || a >= 224;
  }
  const v = ip.toLowerCase();
  if (v.startsWith('::ffff:')) return isPrivateIp(v.slice(7));
  return v === '::' || v === '::1' || v.startsWith('fc') || v.startsWith('fd') || v.startsWith('fe80');
}

async function checkUrl(raw) {
  let u;
  try { u = new URL(raw); } catch (e) { throw Object.assign(new Error('URL 형식이 아니에요'), { status: 400 }); }
  if (u.protocol !== 'https:') throw Object.assign(new Error('https 주소만 불러올 수 있어요'), { status: 400 });
  if (u.username || u.password || (u.port && u.port !== '443')) throw Object.assign(new Error('허용되지 않는 주소예요'), { status: 400 });
  const addrs = net.isIP(u.hostname) ? [{ address: u.hostname }] : await dns.lookup(u.hostname, { all: true });
  if (!addrs.length || addrs.some(a => isPrivateIp(a.address))) throw Object.assign(new Error('허용되지 않는 주소예요'), { status: 400 });
  return u;
}

module.exports = async (req, res) => {
  try {
    let url = await checkUrl(req.query && req.query.url);
    let r;
    for (let i = 0; ; i++) {
      r = await fetch(url, { redirect: 'manual', signal: AbortSignal.timeout(TIMEOUT_MS), headers: { accept: 'image/*' } });
      if (r.status >= 300 && r.status < 400 && r.headers.get('location')) {
        if (i >= MAX_REDIRECTS) throw Object.assign(new Error('리다이렉트가 너무 많아요'), { status: 502 });
        url = await checkUrl(new URL(r.headers.get('location'), url).href);
        continue;
      }
      break;
    }
    if (!r.ok) throw Object.assign(new Error(`원본 서버 응답 ${r.status}`), { status: 502 });
    const type = (r.headers.get('content-type') || '').split(';')[0].trim();
    if (!/^image\/(png|jpeg|webp|gif)$/.test(type)) throw Object.assign(new Error('이미지 주소가 아니에요'), { status: 415 });
    if (Number(r.headers.get('content-length')) > MAX_BYTES) throw Object.assign(new Error('20MB를 넘는 이미지예요'), { status: 413 });
    const chunks = []; let size = 0;
    for await (const c of r.body) {
      size += c.length;
      if (size > MAX_BYTES) throw Object.assign(new Error('20MB를 넘는 이미지예요'), { status: 413 });
      chunks.push(c);
    }
    res.setHeader('Content-Type', type);
    res.setHeader('Cache-Control', 'private, max-age=300');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.status(200).send(Buffer.concat(chunks.map(c => Buffer.from(c))));
  } catch (e) {
    const status = e.status || (e.name === 'TimeoutError' ? 504 : 502);
    res.status(status).json({ error: e.status ? e.message : '이미지를 받아오지 못했어요' });
  }
};
