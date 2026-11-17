#!/usr/bin/env python3
"""Build a single-file offline preview from the existing static website.
Only the export embeds assets and scripts. Live website CSP remains unchanged.
"""
from pathlib import Path
import base64
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'review/involfit-preview.html'

def digest(text):
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode()).digest()).decode() + "'"

def build():
    css = (ROOT / 'styles.css').read_text()
    validation = (ROOT / 'validation.mjs').read_text().replace('export function ', 'function ')
    app = re.sub(r'^import[^;]+;\s*', '', (ROOT / 'app.js').read_text(), count=1)
    bridge = '''document.addEventListener('click', event => {
  const link = event.target.closest('a[href]');
  if (!link) return;
  const target = link.getAttribute('href');
  if (/^(index|projecten|contact)\\.html(?:#.*)?$/.test(target)) {
    event.preventDefault(); parent.openPreview(target);
  }
});'''
    inner_script = validation + '\n' + app + '\n' + bridge
    pages = {}
    for name in ['index.html', 'projecten.html', 'contact.html']:
        text = (ROOT / name).read_text()
        text = re.sub(r'<meta\s+http-equiv="Content-Security-Policy"[\s\S]*?/>', '', text, count=1)
        text = re.sub(r'<link\s+rel="stylesheet"[^>]+>', '', text, count=1)
        text = re.sub(r'<script\s+type="module"[^>]*></script>', '', text, count=1)
        text = text.replace('</head>', '<style>' + css + '</style></head>')
        text = text.replace('</body>', '<script>' + inner_script + '</script></body>')
        pages[name] = text
    assets = {}
    for asset in (ROOT / 'assets').iterdir():
        mime = 'image/svg+xml' if asset.suffix == '.svg' else 'image/webp'
        assets['assets/' + asset.name] = 'data:' + mime + ';base64,' + base64.b64encode(asset.read_bytes()).decode()
    # Escape HTML delimiters in the JSON payload to keep inline scripts well formed.
    data = json.dumps({'pages': pages, 'assets': assets}, ensure_ascii=False).replace('<', '\\u003c')
    shell = '''const bundle = BUNDLE;
const frame = document.getElementById('preview');
window.openPreview = target => { location.hash = target; };
function render() {
  const target = location.hash.slice(1) || 'index.html';
  const [name, anchor] = target.split('#');
  const file = Object.hasOwn(bundle.pages, name) ? name : 'index.html';
  let html = bundle.pages[file];
  for (const [path, uri] of Object.entries(bundle.assets)) html = html.replaceAll(path, uri);
  frame.title = 'Involfit offline demo — ' + file;
  frame.onload = () => {
    if (anchor) frame.contentDocument.getElementById(anchor)?.scrollIntoView();
  };
  frame.srcdoc = html;
}
window.addEventListener('hashchange', render);
render();'''.replace('BUNDLE', data)
    outer_css = 'html,body{margin:0;height:100%;background:#f3efe7}iframe{display:block;width:100%;height:100%;border:0}'
    policy = ("default-src 'none'; script-src " + digest(shell) + ' ' + digest(inner_script)
              + '; style-src ' + digest(css) + ' ' + digest(outer_css)
              + "; img-src data:; frame-src 'self' about:; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'")
    result = ('<!doctype html><html lang="nl"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width,initial-scale=1">'
              '<meta name="robots" content="noindex,nofollow">'
              '<meta http-equiv="Content-Security-Policy" content="' + policy + '">'
              '<title>Involfit — offline architectuurpreview</title><style>' + outer_css + '</style></head>'
              '<body><iframe id="preview" title="Involfit offline demo"></iframe>'
              '<noscript>Deze offline preview vereist JavaScript. Er wordt niets verstuurd of opgeslagen.</noscript>'
              '<script>' + shell + '</script></body></html>')
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(result)
    print('Built:', OUTPUT, f'({OUTPUT.stat().st_size:,} bytes)')

if __name__ == '__main__':
    build()
