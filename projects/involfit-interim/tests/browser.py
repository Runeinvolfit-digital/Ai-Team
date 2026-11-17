"""Browser checks and screenshots. No deployment, message sending or external requests.
Requires installed Python Playwright and /usr/bin/chromium. Optional --axe path.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import argparse,json,threading
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser()
parser.add_argument('--axe',type=Path)
parser.add_argument('--artifacts',type=Path,default=Path('/tmp/involfit-interim-review'))
args=parser.parse_args();args.artifacts.mkdir(parents=True,exist_ok=True)
root=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}';results=[]
def passed(name):results.append(name);print('PASS:',name,flush=True)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  context=browser.new_context();page=context.new_page()
  errors=[];external=[];http_errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) and not r.url.startswith(base) else None)
  page.on('response',lambda r:http_errors.append(r.url) if r.status>=400 else None)
  for width,height in [(1440,1000),(390,844),(320,720),(844,390)]:
   page.set_viewport_size({'width':width,'height':height})
   assert page.goto(base+'/index.html').status==200
   page.wait_for_load_state('networkidle')
   assert page.locator('.eyebrow,.service-number,.step-index,.arrow').count()==0
   assert page.locator('h1').evaluate('(el)=>parseFloat(getComputedStyle(el).fontSize)<=56')
   assert page.locator('h1').count()==1
   assert page.locator('main h1').count()==1
   assert 'Richting en' in page.locator('h1').inner_text()
   assert page.locator('html').get_attribute('lang')=='nl'
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow at {width}'
   assert page.get_by_role('img',name='Gereserveerde ruimte',exact=False).is_visible()
   assert page.locator('input,textarea,form').count()==0
   for link in page.locator('a[href^="#"]').all():
    target=link.get_attribute('href')
    assert page.locator(target).count()==1
   for link in page.locator('a[href^="mailto:"]').all():
    assert link.get_attribute('href').split('?')[0]=='mailto:info@involfit.nl'
   assert page.locator('meta[name=robots]').get_attribute('content')=='noindex,nofollow'
   if args.axe:
    page.evaluate(args.axe.read_text())
    scan=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
    assert not scan['violations'],json.dumps(scan['violations'],indent=2)
   page.screenshot(path=str(args.artifacts/f'home-{width}.png'),animations='disabled')
   page.locator('#werkwijze').scroll_into_view_if_needed();page.wait_for_timeout(150)
   page.screenshot(path=str(args.artifacts/f'explorer-{width}.png'),animations='disabled')
   page.locator('#contact').scroll_into_view_if_needed();page.wait_for_timeout(150)
   page.screenshot(path=str(args.artifacts/f'contact-{width}.png'),animations='disabled')
   passed(f'{width}x{height}: layout, anchor targets, content, mailto, placeholder'+(', axe WCAG scan' if args.axe else ''))
  page.set_viewport_size({'width':390,'height':844});page.goto(base+'/index.html')
  toggle=page.get_by_role('button',name='Menu')
  toggle.focus();page.keyboard.press('Enter')
  assert toggle.get_attribute('aria-expanded')=='true'
  assert page.get_by_role('navigation').is_visible()
  page.keyboard.press('Escape')
  assert toggle.get_attribute('aria-expanded')=='false'
  assert toggle.evaluate('(el)=>document.activeElement===el')
  toggle.click();page.get_by_role('navigation').get_by_role('link',name='Diensten',exact=True).click()
  assert page.url.endswith('#dienstverlening')
  assert toggle.get_attribute('aria-expanded')=='false'
  assert page.locator('#dienstverlening').evaluate('(el)=>document.activeElement===el')
  passed('mobile keyboard menu, Escape, focus restoration and actual anchor navigation')
  page.set_viewport_size({'width':1440,'height':1000})
  assert page.get_by_role('navigation').is_visible()
  passed('navigation available after mobile-to-desktop resize')
  page.locator('[data-choice="advies"]').focus();page.keyboard.press('Enter')
  assert page.locator('[data-choice="advies"]').get_attribute('aria-pressed')=='true'
  assert page.locator('#route-title').inner_text()=='Organisatieadvies'
  assert 'Organisatieadvies' in page.locator('.route-contact').get_attribute('href')
  assert page.locator('.question-tool').get_attribute('data-selected')=='advies'
  assert page.locator('.route-advies').evaluate('(el)=>el.getAnimations().length>0')
  passed('question explorer: keyboard selection, animated path, meaningful result and matching email subject')
  page.emulate_media(reduced_motion='reduce')
  assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
  page.locator('[data-choice="interim"]').click()
  assert page.locator('#route-title').inner_text()=='Interimmanagement'
  assert page.locator('.route-interim').evaluate('(el)=>el.getAnimations().length===0')
  assert page.locator('.route-end').evaluate('(el)=>getComputedStyle(el).transitionDuration')=='0s'
  assert 'Interimmanagement' in page.locator('.route-contact').get_attribute('href')
  passed('reduced motion: no path/circle animation, question explorer remains functional')
  touch_context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
  touch_page=touch_context.new_page();touch_page.goto(base+'/index.html')
  touch_page.locator('[data-choice="advies"]').tap()
  assert touch_page.locator('#route-title').inner_text()=='Organisatieadvies'
  assert 'Organisatieadvies' in touch_page.locator('.route-contact').get_attribute('href')
  touch_page.locator('[data-choice="interim"]').tap()
  assert touch_page.locator('#route-title').inner_text()=='Interimmanagement'
  assert touch_page.locator('[data-choice="interim"]').bounding_box()['height']>=44
  touch_context.close()
  passed('touch: both question choices respond and preserve the correct contact subject')
  nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
  plain=nojs.new_page();plain.goto(base+'/index.html')
  assert plain.get_by_role('navigation').is_visible()
  plain.get_by_role('navigation').get_by_role('link',name='Contact',exact=True).click()
  assert plain.url.endswith('#contact')
  assert plain.locator('#contact a[href="mailto:info@involfit.nl"]').is_visible()
  assert plain.locator('.question-tool').is_hidden()
  assert 'uw vraag begrijpen' in plain.locator('#werkwijze noscript').inner_text()
  passed('JavaScript disabled: navigation, contact and static approach available')
  standalone=browser.new_page(viewport={'width':390,'height':844})
  offline_errors=[];offline_requests=[]
  standalone.on('pageerror',lambda e:offline_errors.append(str(e)))
  standalone.on('request',lambda r:offline_requests.append(r.url))
  standalone.set_content((root/'index.html').read_text())
  assert standalone.locator('h1').is_visible()
  standalone.get_by_role('button',name='Menu').click()
  standalone.get_by_role('navigation').get_by_role('link',name='Over Sander',exact=True).click()
  assert standalone.url.endswith('#sander')
  assert standalone.locator('#sander').evaluate('(el)=>document.activeElement===el')
  standalone.locator('[data-choice=advies]').click()
  assert standalone.locator('#route-title').inner_text()=='Organisatieadvies'
  assert not offline_requests,offline_requests
  assert not offline_errors,offline_errors
  passed('standalone document: layout and menu with zero resource requests')
  assert context.cookies()==[]
  assert page.evaluate('localStorage.length+sessionStorage.length')==0
  assert not errors,errors
  assert not external,external
  assert not http_errors,http_errors
  passed('no JS/HTTP errors, external requests, cookies or browser storage')
  browser.close()
 (args.artifacts/'results.json').write_text(json.dumps({'passed':results,'axe':bool(args.axe)},indent=2))
 print(f'{len(results)} browser check groups passed.')
finally:server.shutdown();server.server_close()
