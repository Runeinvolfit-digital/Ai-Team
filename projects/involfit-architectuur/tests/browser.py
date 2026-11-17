"""Real Chromium checks. --axe /path/to/axe.min.js enables WCAG scans.
Requires Python playwright and /usr/bin/chromium. Owns its temporary server.
"""
import argparse, json, threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser()
parser.add_argument('--axe',type=Path)
parser.add_argument('--artifacts',type=Path,default=Path('/tmp/involfit-browser'))
args=parser.parse_args(); args.artifacts.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(Path(__file__).resolve().parents[1])))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'; results=[]
def passed(name):results.append(name);print('PASS:',name,flush=True)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  context=browser.new_context(viewport={'width':1440,'height':1000});page=context.new_page()
  errors=[];failures=[];external=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.on('response',lambda response:failures.append(response.url) if response.status>=400 else None)
  page.on('request',lambda request:external.append(request.url) if not request.url.startswith(base) else None)
  for width,height in [(1440,1000),(390,844),(320,720),(844,390)]:
   page.set_viewport_size({'width':width,'height':height})
   for file in ['index.html','projecten.html','contact.html']:
    assert page.goto(f'{base}/{file}').status==200
    page.wait_for_load_state('networkidle')
    assert page.locator('h1').count()==1
    assert page.locator('nav a[aria-current="page"]').count()==1
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'overflow {file} at {width}'
    assert page.locator('html').get_attribute('lang')=='nl'
    for image in page.locator('img').all():
     image.scroll_into_view_if_needed()
     assert image.evaluate('(img)=>img.complete && img.naturalWidth>0')
    if args.axe:
     page.evaluate(args.axe.read_text())
     scan=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
     assert not scan['violations'],json.dumps(scan['violations'],indent=2)
    page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
    page.screenshot(path=str(args.artifacts/f'{file[:-5]}-{width}.png'),full_page=True,animations='disabled')
   passed(f'3 pages at {width}x{height}: layout, images, headings, navigation'+(', axe scan' if args.axe else ''))
  page.set_viewport_size({'width':390,'height':844});page.goto(base+'/index.html')
  menu=page.get_by_role('button',name='Menu');menu.focus();page.keyboard.press('Enter')
  assert menu.get_attribute('aria-expanded')=='true'
  assert page.get_by_role('navigation').is_visible()
  page.keyboard.press('Escape')
  assert menu.get_attribute('aria-expanded')=='false'
  assert menu.evaluate('(node)=>document.activeElement===node')
  menu.click();page.get_by_role('navigation').get_by_role('link',name='Projecten',exact=True).click()
  assert page.url.endswith('projecten.html')
  passed('mobile keyboard menu, Escape, focus restoration and navigation')
  page.get_by_role('button',name='Wonen',exact=True).click()
  assert page.locator('.project:visible').count()==1
  assert page.locator('#duinwoning').is_visible()
  assert page.locator('#filter-status').inner_text()=='1 fictief project'
  page.get_by_role('button',name='Cultuur',exact=True).click()
  assert page.locator('#bospaviljoen').is_visible()
  assert page.locator('.project:visible').count()==1
  page.get_by_role('button',name='Alle projecten').click()
  assert page.locator('.project:visible').count()==2
  page.locator('#duinwoning summary').click()
  assert page.locator('#duinwoning details').get_attribute('open') is not None
  passed('project filters, live count and disclosure')
  page.goto(base+'/contact.html');page.wait_for_load_state('networkidle')
  assert page.locator('#interest option').count()==3
  page.locator('#interest').select_option('wonen')
  assert page.locator('#interest').input_value()=='wonen'
  submissions=[];page.on('request',lambda request:submissions.append(request.url))
  submit=page.get_by_role('button',name='Controleer mijn demo-invoer')
  submit.click();assert page.locator('[aria-invalid="true"]').count()==3
  assert page.locator('#name').evaluate('(node)=>document.activeElement===node')
  page.locator('#name').fill('Demo Gebruiker');page.locator('#email').fill('ongeldig');page.locator('#message').fill('te kort')
  submit.click();assert page.locator('[aria-invalid="true"]').count()==2
  assert page.locator('#email').evaluate('(node)=>document.activeElement===node')
  page.locator('#email').fill('demo@example.com');page.locator('#message').fill('Een fictief idee voor een rustige woonruimte.')
  submit.click();assert page.locator('[aria-invalid="true"]').count()==0
  assert 'Er is niets verstuurd of opgeslagen' in page.locator('#form-status').inner_text()
  assert page.locator('#form-status').evaluate('(node)=>document.activeElement===node')
  assert not submissions,submissions
  assert context.cookies()==[]
  assert page.evaluate('localStorage.length+sessionStorage.length')==0
  passed('invalid/valid form, accessible errors, focus and zero requests/cookies/storage')
  page.locator('#name').fill('<img src=x onerror=alert(1)>');submit.click()
  assert page.locator('#form-status img').count()==0
  assert not submissions
  passed('input never interpreted as HTML')
  page.emulate_media(reduced_motion='reduce')
  assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
  passed('reduced motion respected')
  assert not errors,errors
  assert not failures,failures
  assert not external,external
  passed('no JS errors, HTTP errors or external requests')
  nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});plain=nojs.new_page()
  plain.goto(base+'/index.html');assert plain.get_by_role('navigation').is_visible()
  plain.get_by_role('navigation').get_by_role('link',name='Projecten',exact=True).click()
  assert plain.locator('.project:visible').count()==2
  assert plain.locator('.filter-bar').is_hidden()
  plain.goto(base+'/contact.html')
  assert plain.get_by_role('button',name='Controleer mijn demo-invoer').is_disabled()
  assert 'JavaScript is uitgeschakeld' in plain.locator('noscript').inner_text()
  passed('without JS: navigation/projects work; form disabled')
  browser.close()
 print(f'{len(results)} browser check groups passed.')
 (args.artifacts/'results.json').write_text(json.dumps({'passed':results,'axe':bool(args.axe)},indent=2))
finally:server.shutdown();server.server_close()
