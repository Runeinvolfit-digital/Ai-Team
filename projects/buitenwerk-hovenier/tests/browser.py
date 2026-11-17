"""Functional Chromium tests; local server is owned and stopped by this runner.
Requires Python Playwright, Chromium; optional --axe /path/to/axe.min.js.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import argparse,json,threading
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('--axe',type=Path);parser.add_argument('--artifacts',type=Path,default=Path('/tmp/buitenwerk-review'))
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
  context=browser.new_context(accept_downloads=True);page=context.new_page()
  errors=[];external=[];http_errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) and not r.url.startswith(base) else None)
  page.on('response',lambda r:http_errors.append(r.url) if r.status>=400 else None)
  for width,height in [(1440,1000),(390,844),(320,720),(844,390)]:
   page.set_viewport_size({'width':width,'height':height})
   assert page.goto(base+'/index.html').status==200
   page.wait_for_load_state('networkidle')
   assert page.locator('main h1').count()==1
   assert 'Buiten begint' in page.locator('h1').inner_text()
   assert page.locator('h1').evaluate('(el)=>parseFloat(getComputedStyle(el).fontSize)<=56')
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow {width}'
   assert page.locator('.eyebrow,.step-index,.service-number,.arrow').count()==0
   assert page.locator('html').get_attribute('lang')=='nl'
   assert 'werknaam' in page.locator('.concept-note').inner_text()
   assert page.locator('img').evaluate('async img=>{await img.decode();return img.naturalWidth>0}')
   assert page.locator('form,input,textarea,a[href^="mailto:"],a[href^="tel:"]').count()==0
   for link in page.locator('a[href^="#"]').all():assert page.locator(link.get_attribute('href')).count()==1
   if args.axe:
    page.evaluate(args.axe.read_text())
    scan=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
    assert not scan['violations'],json.dumps(scan['violations'],indent=2)
   page.screenshot(path=str(args.artifacts/f'home-{width}.png'),animations='disabled')
   page.locator('#tuinverkenner').scroll_into_view_if_needed();page.wait_for_timeout(200)
   page.screenshot(path=str(args.artifacts/f'explorer-{width}.png'),animations='disabled')
   passed(f'{width}x{height}: responsive layout, headings, image, links and honest concept labels'+(', axe WCAG scan' if args.axe else ''))
  page.set_viewport_size({'width':390,'height':844});page.goto(base+'/index.html')
  menu=page.get_by_role('button',name='Menu',exact=True)
  menu.focus();page.keyboard.press('Enter');assert menu.get_attribute('aria-expanded')=='true'
  page.keyboard.press('Escape');assert menu.get_attribute('aria-expanded')=='false'
  assert menu.evaluate('(el)=>document.activeElement===el')
  menu.click();page.get_by_role('navigation').get_by_role('link',name='Diensten',exact=True).click()
  assert page.url.endswith('#diensten');assert menu.get_attribute('aria-expanded')=='false'
  assert page.locator('#diensten').evaluate('(el)=>document.activeElement===el')
  passed('mobile keyboard menu, Escape, focus and anchor navigation')
  page.locator('[data-choice=rust]').focus();page.keyboard.press('Enter');page.wait_for_timeout(80)
  assert page.locator('#idea-title').inner_text()=='Een plek om te blijven'
  assert page.locator('.garden-scene').get_attribute('data-garden')=='rust'
  assert page.locator('[data-choice=rust]').get_attribute('aria-pressed')=='true'
  assert page.locator('[data-choice=groen]').get_attribute('aria-pressed')=='false'
  assert page.locator('.scene-terrace').evaluate('(el)=>el.getAnimations().length>0')
  assert 'Een plek om te blijven' in page.locator('#garden-title').text_content()
  passed('garden explorer: keyboard selection, animated scene, live result and accessible SVG title')
  page.locator('[data-choice=gemak]').click()
  assert page.locator('#idea-title').inner_text()=='Overzichtelijk en groen'
  assert 'Onderhoudsvrij wordt een tuin nooit' in page.locator('#idea-description').inner_text()
  with page.expect_download() as download_info:page.get_by_role('button',name='Bewaar mijn tuinidee').click()
  download=download_info.value;assert download.suggested_filename=='mijn-tuinidee-gemak.txt'
  target=args.artifacts/download.suggested_filename;download.save_as(target)
  contents=target.read_text()
  assert 'Overzichtelijk en groen' in contents and 'Buitenwerk (werknaam)' in contents and 'Geen offerte' in contents
  assert 'niets verstuurd' in page.locator('#idea-status').inner_text()
  passed('real text download reflects selected garden, limitations and no submission')
  page.emulate_media(reduced_motion='reduce');page.locator('[data-choice=groen]').click()
  assert page.locator('#idea-title').inner_text()=='Een tuin die leeft'
  assert page.locator('.scene-plants').evaluate('(el)=>getComputedStyle(el).transitionDuration')=='0s'
  assert page.locator('.scene-plants').evaluate('(el)=>el.getAnimations().length===0')
  assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
  passed('reduced motion: choice works with plant transitions and smooth scrolling disabled')
  touch_context=browser.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
  touch=touch_context.new_page();touch.goto(base+'/index.html')
  touch.locator('[data-choice=rust]').tap();assert touch.locator('#idea-title').inner_text()=='Een plek om te blijven'
  touch.locator('[data-choice=gemak]').tap();assert touch.locator('#idea-title').inner_text()=='Overzichtelijk en groen'
  assert touch.locator('[data-choice=gemak]').bounding_box()['height']>=44
  touch_context.close();passed('touch input changes garden choices; target height at least 44px')
  nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
  plain=nojs.new_page();plain.goto(base+'/index.html')
  assert plain.get_by_role('navigation').is_visible()
  plain.get_by_role('navigation').get_by_role('link',name='Verken uw tuin').click()
  assert plain.url.endswith('#tuinverkenner')
  assert plain.locator('.garden-choices').is_hidden()
  assert plain.get_by_role('button',name='Bewaar mijn tuinidee').is_disabled()
  assert 'JavaScript' in plain.locator('noscript').inner_text()
  passed('JavaScript disabled: navigation, static garden inspiration and clear fallback')
  standalone=browser.new_page(viewport={'width':390,'height':844})
  offline_requests=[];offline_errors=[]
  standalone.on('request',lambda r:offline_requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
  standalone.on('pageerror',lambda e:offline_errors.append(str(e)))
  standalone.set_content((root/'index.html').read_text())
  assert standalone.locator('img').evaluate('async img=>{await img.decode();return img.naturalWidth>0}')
  standalone.locator('[data-choice=gemak]').click();assert standalone.locator('#idea-title').inner_text()=='Overzichtelijk en groen'
  with standalone.expect_download() as offline_download:standalone.get_by_role('button',name='Bewaar mijn tuinidee').click()
  assert offline_download.value.suggested_filename=='mijn-tuinidee-gemak.txt'
  assert not offline_requests,offline_requests
  assert not offline_errors,offline_errors
  passed('standalone HTML: embedded photo, animated garden and real download without server requests')
  assert not errors,errors
  assert not external,external
  assert not http_errors,http_errors
  assert context.cookies()==[]
  assert page.evaluate('localStorage.length+sessionStorage.length')==0
  passed('no JS/HTTP errors, external requests, cookies or browser storage')
  browser.close()
 (args.artifacts/'results.json').write_text(json.dumps({'passed':results,'axe':bool(args.axe)},indent=2))
 print(f'{len(results)} browser check groups passed.')
finally:server.shutdown();server.server_close()
