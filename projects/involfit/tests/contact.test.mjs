import assert from 'node:assert/strict';
import { once } from 'node:events';
import { mkdir, mkdtemp, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { createWebsiteServer } from '../server.mjs';

const valid = {
  name: ' Test Bezoeker ',
  email: 'bezoeker@example.test',
  organization: 'Testorganisatie',
  message: 'Ik wil een organisatievraag bespreken.',
  website: '',
};
const config = { RESEND_API_KEY: 'test-placeholder', CONTACT_FROM: 'form@example.test' };

async function runServer(t, options) {
  const server = createWebsiteServer(options);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(() => new Promise((resolve, reject) => server.close((error) => {
    if (error) reject(error);
    else resolve();
  })));
  const base = `http://127.0.0.1:${server.address().port}`;
  return {
    base,
    submit(payload, { headers, body } = {}) {
      return fetch(`${base}/api/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Origin: base, ...headers },
        body: body ?? JSON.stringify(payload),
      });
    },
  };
}

test('forwards validated details to configured provider, then reports acceptance', async (t) => {
  const calls = [];
  const { submit } = await runServer(t, {
    config,
    fetchImpl: async (...args) => {
      calls.push(args);
      return Response.json({ id: 'local-test-acceptance' });
    },
  });
  const response = await submit(valid);
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { ok: true });
  assert.equal(response.headers.get('cache-control'), 'no-store');
  assert.equal(calls.length, 1);
  const [url, request] = calls[0];
  assert.equal(url, 'https://api.resend.com/emails');
  assert.equal(request.headers.Authorization, 'Bearer test-placeholder');
  assert.equal(request.redirect, 'error');
  assert.deepEqual(JSON.parse(request.body), {
    from: 'form@example.test',
    to: ['info@involfit.nl'],
    reply_to: 'bezoeker@example.test',
    subject: 'Bericht via het Involfit-contactformulier',
    text: 'Naam: Test Bezoeker\nE-mailadres: bezoeker@example.test\nOrganisatie: Testorganisatie\n\nIk wil een organisatievraag bespreken.',
  });
});

test('rejects bad origin, format, oversized data, invalid fields and honeypot values', async (t) => {
  let providerCalls = 0;
  const { base, submit } = await runServer(t, {
    config,
    fetchImpl: async () => {
      providerCalls += 1;
      return Response.json({ id: 'accepted' });
    },
  });
  assert.equal((await submit(valid, { headers: { Origin: 'https://other.example.test' } })).status, 403);
  assert.equal((await submit(valid, { headers: { Origin: 'null' } })).status, 403);
  assert.equal((await submit(valid, { headers: { 'Content-Type': 'text/plain' } })).status, 415);
  assert.equal((await submit({ ...valid, message: 'x'.repeat(25_000) })).status, 413);
  const largeStream = new ReadableStream({
    start(controller) {
      controller.enqueue(new TextEncoder().encode('x'.repeat(25_000)));
      controller.close();
    },
  });
  assert.equal((await fetch(`${base}/api/contact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Origin: base },
    body: largeStream,
    duplex: 'half',
  })).status, 413);
  assert.equal((await submit({}, { body: '{' })).status, 400);
  const invalid = await submit({ name: '', email: 'bad', organization: 5, message: ' ' });
  assert.equal(invalid.status, 400);
  assert.deepEqual(Object.keys((await invalid.json()).errors), ['name', 'email', 'organization', 'message']);
  assert.equal((await submit({ ...valid, website: 'spam' })).status, 400);
  const method = await fetch(`${base}/api/contact`);
  assert.equal(method.status, 405);
  assert.equal(method.headers.get('allow'), 'POST');
  assert.equal(providerCalls, 0);
});

test('checks the explicit production origin and rate limits attempts', async (t) => {
  const origin = 'https://involfit.nl';
  let providerCalls = 0;
  const { submit } = await runServer(t, {
    config: { ...config, CONTACT_ORIGIN: origin },
    fetchImpl: async () => {
      providerCalls += 1;
      return Response.json({ id: 'accepted' });
    },
  });
  assert.equal((await submit(valid)).status, 403);
  for (let attempt = 0; attempt < 6; attempt += 1) {
    assert.equal((await submit(valid, { headers: { Origin: origin } })).status, 200);
  }
  const limited = await submit(valid, { headers: { Origin: origin, 'X-Forwarded-For': '192.0.2.1' } });
  assert.equal(limited.status, 429);
  assert.ok(Number(limited.headers.get('retry-after')) > 0);
  assert.equal(providerCalls, 6);
});

test('shows an honest failure when configuration is missing or the provider fails', async (t) => {
  const noConfig = await runServer(t, { config: {} });
  const unavailable = await noConfig.submit(valid);
  assert.equal(unavailable.status, 503);
  assert.equal((await unavailable.json()).ok, false);
  const badProvider = await runServer(t, {
    config,
    fetchImpl: async () => new Response('provider message with internal details', { status: 401 }),
  });
  const rejected = await badProvider.submit(valid);
  assert.equal(rejected.status, 502);
  const body = await rejected.json();
  assert.equal(body.ok, false);
  assert.doesNotMatch(body.message, /internal details/);
  const invalidProvider = await runServer(t, {
    config,
    fetchImpl: async () => Response.json({}),
  });
  assert.equal((await invalidProvider.submit(valid)).status, 502);
});

test('serves documented pages and protects the static root', async (t) => {
  const folder = await mkdtemp(join(tmpdir(), 'involfit-test-'));
  t.after(() => rm(folder, { force: true, recursive: true }));
  const distRoot = join(folder, 'dist');
  await mkdir(distRoot);
  for (const path of ['over-sander', 'diensten', 'ervaring', 'contact', 'privacy']) {
    await mkdir(join(distRoot, path));
    await writeFile(join(distRoot, path, 'index.html'), `<h1>${path}</h1>`);
  }
  await writeFile(join(distRoot, 'index.html'), '<h1>Involfit</h1>');
  await writeFile(join(distRoot, 'style.css'), 'body { margin: 0 }');
  await writeFile(join(distRoot, 'robots.txt'), 'User-agent: *\nAllow: /\n');
  await writeFile(join(distRoot, '.env.txt'), 'test content outside asset allowlist');
  await writeFile(join(folder, 'outside.txt'), 'outside build');
  await symlink(join(folder, 'outside.txt'), join(distRoot, 'outside.txt'));

  const { base } = await runServer(t, { config: {}, distRoot });
  for (const path of ['/', '/over-sander/', '/diensten/', '/ervaring/', '/contact/', '/privacy/']) {
    const response = await fetch(base + path);
    assert.equal(response.status, 200);
    assert.match(await response.text(), /<h1>/);
    assert.match(response.headers.get('content-security-policy'), /frame-ancestors 'none'/);
    assert.equal(response.headers.get('x-robots-tag'), 'noindex, nofollow');
  }
  const redirect = await fetch(`${base}/diensten`, { redirect: 'manual' });
  assert.equal(redirect.status, 308);
  assert.equal(redirect.headers.get('location'), '/diensten/');
  const head = await fetch(`${base}/style.css`, { method: 'HEAD' });
  assert.equal(head.status, 200);
  assert.match(head.headers.get('content-type'), /^text\/css/);
  assert.equal(await head.text(), '');
  for (const path of ['/outside.txt', '/.env.txt', '/index.html', '/missing/', '/.env']) {
    assert.equal((await fetch(base + path)).status, 404);
  }
  assert.match(await (await fetch(`${base}/robots.txt`)).text(), /Disallow: \//);
  const production = await runServer(t, { config: { SITE_INDEXABLE: '1' }, distRoot });
  const robots = await fetch(`${production.base}/robots.txt`);
  assert.match(await robots.text(), /Allow: \//);
  assert.equal(robots.headers.get('x-robots-tag'), null);
});
