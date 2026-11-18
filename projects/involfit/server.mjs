import { createServer } from 'node:http';
import { readFile, realpath } from 'node:fs/promises';
import { resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const defaultRoot = fileURLToPath(new URL('./dist/', import.meta.url));
const routes = new Map([
  ['/', 'index.html'],
  ['/over-sander/', 'over-sander/index.html'],
  ['/diensten/', 'diensten/index.html'],
  ['/ervaring/', 'ervaring/index.html'],
  ['/contact/', 'contact/index.html'],
  ['/privacy/', 'privacy/index.html'],
]);
const types = {
  css: 'text/css; charset=utf-8',
  html: 'text/html; charset=utf-8',
  ico: 'image/x-icon',
  js: 'text/javascript; charset=utf-8',
  mjs: 'text/javascript; charset=utf-8',
  png: 'image/png',
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  svg: 'image/svg+xml',
  txt: 'text/plain; charset=utf-8',
  webp: 'image/webp',
  avif: 'image/avif',
  woff2: 'font/woff2',
  xml: 'application/xml; charset=utf-8',
};
const policies = {
  'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
};
const maxBodyBytes = 24_576;
const windowMs = 15 * 60_000;
const addressLimit = 6;
const globalLimit = 60;
const emailPattern = /^[^\s@<>]+@[^\s@<>.]+(?:\.[^\s@<>.]+)+$/u;

function sendJson(response, status, body) {
  response.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
  });
  response.end(JSON.stringify(body));
}

function fail(response, status, message, errors) {
  sendJson(response, status, errors ? { ok: false, message, errors } : { ok: false, message });
}

function sameOrigin(request, configuredOrigin) {
  if (!request.headers.origin || request.headers['sec-fetch-site'] === 'cross-site') {
    return false;
  }
  try {
    const origin = new URL(request.headers.origin);
    if (origin.origin !== request.headers.origin) return false;
    if (configuredOrigin) return origin.origin === new URL(configuredOrigin).origin;
    return ['https:', 'http:'].includes(origin.protocol) && origin.host === request.headers.host;
  } catch {
    return false;
  }
}

async function readJson(request) {
  const body = [];
  let length = 0;
  for await (const chunk of request.iterator({ destroyOnReturn: false })) {
    length += chunk.length;
    if (length > maxBodyBytes) {
      request.resume();
      return { tooLarge: true };
    }
    body.push(chunk);
  }
  try {
    return { payload: JSON.parse(Buffer.concat(body).toString('utf8')) };
  } catch {
    return { payload: null };
  }
}

function validate(payload) {
  const errors = {};
  const data = {};
  const fields = [
    ['name', 'naam', 120, true],
    ['email', 'e-mailadres', 254, true],
    ['organization', 'organisatie', 160, false],
    ['message', 'bericht', 5000, true],
  ];
  for (const [key, label, maximum, required] of fields) {
    const input = Object.hasOwn(payload, key) ? payload[key] : '';
    const value = typeof input === 'string' ? input.trim() : '';
    if (typeof input !== 'string') {
      errors[key] = `Vul een geldige waarde in voor ${label}.`;
    } else if (required && !value) {
      errors[key] = `Vul je ${label} in.`;
    } else if (value.length > maximum) {
      errors[key] = `Gebruik maximaal ${maximum} tekens.`;
    } else if (key === 'email' && !emailPattern.test(value)) {
      errors[key] = 'Vul een geldig e-mailadres in.';
    } else {
      data[key] = value;
    }
  }
  return { errors, data };
}

function createRateLimiter() {
  const addresses = new Map();
  let accepted = 0;
  let resetAt = 0;

  return (address) => {
    const now = Date.now();
    if (now >= resetAt) {
      addresses.clear();
      accepted = 0;
      resetAt = now + windowMs;
    }
    const count = addresses.get(address) ?? 0;
    if (accepted >= globalLimit || count >= addressLimit) {
      return Math.ceil((resetAt - now) / 1000);
    }
    addresses.set(address, count + 1);
    accepted += 1;
    return 0;
  };
}

async function submitContact(request, response, config, fetchImpl, consumeQuota) {
  if (request.method !== 'POST') {
    response.setHeader('Allow', 'POST');
    return fail(response, 405, 'Gebruik POST voor het contactformulier.');
  }
  if (!sameOrigin(request, config.CONTACT_ORIGIN)) {
    return fail(response, 403, 'Open het formulier op de Involfit-website.');
  }
  if (request.headers['content-type']?.split(';')[0].trim().toLowerCase() !== 'application/json') {
    return fail(response, 415, 'Dit berichtformaat wordt niet ondersteund.');
  }
  if (Number(request.headers['content-length']) > maxBodyBytes) {
    request.resume();
    return fail(response, 413, 'Het bericht is te groot.');
  }

  const retryAfter = consumeQuota(request.socket.remoteAddress ?? '');
  if (retryAfter) {
    response.setHeader('Retry-After', retryAfter);
    return fail(response, 429, 'Er zijn te veel berichten verstuurd. Probeer het later opnieuw.');
  }

  const { payload, tooLarge } = await readJson(request);
  if (tooLarge) return fail(response, 413, 'Het bericht is te groot.');
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    return fail(response, 400, 'Het bericht kon niet worden gelezen.');
  }
  if (Object.hasOwn(payload, 'website') && payload.website !== '') {
    return fail(response, 400, 'Het formulier bevat een ongeldige waarde.');
  }

  const { errors, data } = validate(payload);
  if (Object.keys(errors).length) {
    return fail(response, 400, 'Controleer de gemarkeerde velden.', errors);
  }
  if (!config.RESEND_API_KEY || !config.CONTACT_FROM) {
    return fail(response, 503, 'Het formulier is tijdelijk niet beschikbaar. Stuur ons rechtstreeks een e-mail.');
  }

  const text = [
    `Naam: ${data.name}`,
    `E-mailadres: ${data.email}`,
    ...(data.organization ? [`Organisatie: ${data.organization}`] : []),
    '',
    data.message,
  ].join('\n');

  try {
    const provider = await fetchImpl('https://api.resend.com/emails', {
      method: 'POST',
      redirect: 'error',
      signal: AbortSignal.timeout(8000),
      headers: {
        Authorization: `Bearer ${config.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: config.CONTACT_FROM,
        to: [config.CONTACT_TO || 'info@involfit.nl'],
        reply_to: data.email,
        subject: 'Bericht via het Involfit-contactformulier',
        text,
      }),
    });
    if (provider.ok && typeof (await provider.json()).id === 'string') {
      return sendJson(response, 200, { ok: true });
    }
    await provider.body?.cancel();
  } catch {
    // Provider errors can include credentials or form contents. Return a generic reply.
  }
  return fail(response, 502, 'We konden je bericht niet versturen. Probeer het later opnieuw of stuur ons een e-mail.');
}

function sendText(response, status, message, head = false) {
  response.writeHead(status, { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
  response.end(head ? undefined : message);
}

async function servePage(request, response, pathname, distRoot, indexable) {
  const head = request.method === 'HEAD';
  if (request.method !== 'GET' && !head) {
    response.setHeader('Allow', 'GET, HEAD');
    return sendText(response, 405, 'Deze methode is niet beschikbaar.');
  }
  if (routes.has(`${pathname}/`)) {
    response.writeHead(308, { Location: `${pathname}/` });
    return response.end();
  }

  if (pathname === '/robots.txt' && !indexable) {
    return sendText(response, 200, 'User-agent: *\nDisallow: /\n', head);
  }
  const asset = /^\/(?:[A-Za-z0-9_-]+\/)*[A-Za-z0-9_-][A-Za-z0-9_.-]*\.(css|ico|js|mjs|png|jpg|jpeg|svg|txt|webp|avif|woff2|xml)$/u.exec(pathname);
  const page = routes.get(pathname);
  const relative = page ?? asset?.[0].slice(1) ?? '404.html';
  const status = page || asset ? 200 : 404;

  let data;
  try {
    const root = await realpath(distRoot);
    const file = await realpath(resolve(root, relative));
    if (!file.startsWith(`${root}${sep}`)) return sendText(response, 404, 'Deze pagina bestaat niet.', head);
    data = await readFile(file);
  } catch (error) {
    if (['ENOENT', 'ENOTDIR', 'EISDIR'].includes(error.code)) {
      return sendText(response, 404, 'Deze pagina bestaat niet.', head);
    }
    throw error;
  }
  response.writeHead(status, {
    'Content-Type': page || !asset ? types.html : types[asset[1]],
    'Content-Length': data.length,
    'Cache-Control': page || !asset ? 'no-cache' : 'public, max-age=3600',
  });
  return response.end(head ? undefined : data);
}

export function createWebsiteServer({
  config = process.env,
  fetchImpl = globalThis.fetch,
  distRoot = defaultRoot,
} = {}) {
  const consumeQuota = createRateLimiter();
  const indexable = config.SITE_INDEXABLE === '1';

  return createServer({ requestTimeout: 30_000 }, async (request, response) => {
    for (const [header, value] of Object.entries(policies)) response.setHeader(header, value);
    if (!indexable) response.setHeader('X-Robots-Tag', 'noindex, nofollow');
    // Match the raw path so unexpected dot segments never become a valid route.
    const pathname = request.url?.split('?', 1)[0] ?? '';
    const api = pathname === '/api/contact';
    try {
      if (api) return await submitContact(request, response, config, fetchImpl, consumeQuota);
      return await servePage(request, response, pathname, distRoot, indexable);
    } catch {
      if (response.headersSent || response.destroyed) return;
      if (api) return fail(response, 500, 'Het bericht kon niet worden verwerkt.');
      return sendText(response, 500, 'Er is tijdelijk een probleem met de website.', request.method === 'HEAD');
    }
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const host = process.env.HOST || '0.0.0.0';
  const port = Number(process.env.PORT || 3000);
  createWebsiteServer().listen(port, host, () => console.log(`Involfit luistert op ${host}:${port}`));
}
