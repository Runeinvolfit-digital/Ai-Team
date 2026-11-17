"""Test standalone HTML without a server or external requests.
Managed Chromium blocks file://, so load its exact bytes with set_content.
This validates the standalone document, not the user's local browser settings.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
root = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    for width, height in [(1440,1000),(390,844)]:
        page = browser.new_page(viewport={'width':width,'height':height})
        errors = []; external = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: external.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
        html=(root/'review/involfit-preview.html').read_text()
        page.set_content(html)
        frame = page.frame_locator('#preview')
        assert 'Ruimte voor' in frame.locator('h1').inner_text()
        assert frame.locator('img').first.evaluate('async img => { await img.decode(); return img.naturalWidth > 0; }')
        if width == 390: frame.get_by_role('button',name='Menu').click()
        frame.get_by_role('navigation').get_by_role('link',name='Projecten',exact=True).click()
        frame.get_by_role('button',name='Wonen',exact=True).click()
        assert frame.locator('.project:visible').count()==1
        if width == 390: frame.get_by_role('button',name='Menu').click()
        frame.get_by_role('navigation').get_by_role('link',name='Contact',exact=True).click()
        submit=frame.get_by_role('button',name='Controleer mijn demo-invoer')
        submit.click();assert frame.locator('[aria-invalid="true"]').count()==3
        frame.locator('#name').fill('Demo Gebruiker')
        frame.locator('#email').fill('demo@example.com')
        frame.locator('#message').fill('Dit is een fictief idee voor de lokale preview.')
        submit.click()
        assert 'Er is niets verstuurd of opgeslagen' in frame.locator('#form-status').inner_text()
        if width==390: frame.get_by_role('button',name='Menu').click()
        frame.get_by_role('navigation').get_by_role('link',name='Home',exact=True).click()
        assert 'Ruimte voor' in frame.locator('h1').inner_text()
        assert not external,external
        assert not errors,errors
        print(f'PASS offline {width}x{height}: navigation, images, filter, invalid/valid form, routing and no external requests or JS errors')
        page.close()
    browser.close()
