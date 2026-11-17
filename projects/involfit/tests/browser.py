"""Check the production build through the actual Node server in Chromium.

Run after npm run build. Optional arguments select axe-core and a screenshot
directory. The mail-success test uses an injected provider on an isolated port.
"""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = (360, 390, 768, 1024, 1440, 1920)
ROUTES = {"/": "home", "/diensten/": "diensten", "/contact/": "contact", "/privacy/": "privacy"}
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
SERVER = """
import {createWebsiteServer} from './server.mjs';
const mock = process.argv.includes('--mock');
const server = createWebsiteServer(mock ? {
  config: {CONTACT_FROM: 'test@involfit.example', RESEND_API_KEY: 'fake'},
  fetchImpl: async (_url, request) => {
    const email = JSON.parse(request.body);
    if (!email.text.includes('Testbericht') || email.reply_to !== 'test@example.com') {
      return new Response(null, {status: 422});
    }
    return Response.json({id: 'test-provider-acceptance'});
  },
} : {config: {}});
server.listen(0, '127.0.0.1', () => console.log(server.address().port));
"""


@contextmanager
def serve(mock=False):
    args = ["node", "--input-type=module", "-e", SERVER]
    if mock:
        args.extend(["--", "--mock"])
    proc = subprocess.Popen(args, cwd=ROOT, stdout=subprocess.PIPE, text=True)
    try:
        line = proc.stdout.readline()
        if not line.strip().isdigit():
            raise RuntimeError(f"Node server failed to report its port: {line!r}")
        yield f"http://127.0.0.1:{line.strip()}"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def open_route(page, base, route):
    response = page.goto(base + route, wait_until="networkidle")
    assert response.status == 200, (route, response.status)
    assert "noindex" in response.headers["x-robots-tag"]
    expect(page.locator("h1")).to_have_count(1)
    expect(page.locator("main")).to_be_visible()
    assert page.locator('link[rel="canonical"]').get_attribute("href") == "https://involfit.nl" + route


def audit(page, axe):
    page.evaluate(axe.read_text())
    violations = page.evaluate("(tags) => axe.run({runOnly: {type: 'tag', values: tags}}).then(r => r.violations.map(v => ({id: v.id, nodes: v.nodes.map(n => n.target)})))", TAGS)
    assert not violations, (page.url, violations)


def layout_matrix(browser, base, screenshots, axe):
    for width in VIEWPORTS:
        height = 844 if width <= 390 else 1000
        context = browser.new_context(viewport={"width": width, "height": height})
        page = context.new_page()
        issues = []
        page.on("pageerror", lambda error: issues.append(str(error)))
        page.on("console", lambda message: issues.append(message.text[:300]) if message.type == "error" else None)
        failures = []
        page.on("response", lambda response: failures.append((response.status, response.url)) if response.status >= 400 else None)
        for route, name in ROUTES.items():
            open_route(page, base, route)
            assert page.evaluate("document.documentElement.scrollWidth === innerWidth"), (width, route)
            assert page.evaluate("document.fonts.check('16px Manrope Variable')"), (width, route)
            if route in ("/", "/diensten/", "/contact/"):
                current = page.locator('nav[aria-label="Hoofdnavigatie"] [aria-current="page"]')
                expect(current).to_have_attribute("href", route)
            if route == "/":
                founder_image = page.locator(".founder figure img")
                founder_image.scroll_into_view_if_needed()
                page.wait_for_function("document.querySelector('.founder figure img').naturalWidth > 0")
                page.evaluate("scrollTo(0, 0)")
            if route == "/contact/":
                expect(page.get_by_role("button", name="Verstuur bericht")).to_be_visible()
            if width in (390, 1440):
                if screenshots and route != "/privacy/":
                    form = "mobiel" if width == 390 else "desktop"
                    page.screenshot(path=str(screenshots / f"{name}-{form}.png"), full_page=True)
                if axe:
                    audit(page, axe)
        assert not issues, (width, issues)
        assert not failures, (width, failures)
        context.close()

    # Use the 320 CSS pixel reflow reference width of WCAG 1.4.10.
    context = browser.new_context(viewport={"width": 320, "height": 800})
    page = context.new_page()
    for route in ROUTES:
        open_route(page, base, route)
        assert page.evaluate("document.documentElement.scrollWidth === innerWidth"), (320, route)
    context.close()


def enlarged_text(browser, base):
    # Bypass CSP only for injecting this test stylesheet into the page.
    for width in (920, 1024, 1440):
        context = browser.new_context(viewport={"width": width, "height": 1000}, bypass_csp=True)
        page = context.new_page()
        for route in ROUTES:
            open_route(page, base, route)
            page.add_style_tag(content=":root { font-size: 212% !important; }")
            page.evaluate("document.fonts.ready")
            assert page.evaluate("document.documentElement.scrollWidth === innerWidth"), (width, route)
            overflow = page.locator("h1, h2, h3").evaluate_all(
                "(headings) => headings.filter(el => el.scrollWidth > el.clientWidth + 2).map(el => el.innerText)"
            )
            assert not overflow, (width, route, overflow)
            if route == "/":
                panel = page.locator(".question-answer:visible")
                links = panel.locator(".answer-links")
                assert links.bounding_box()["y"] + links.bounding_box()["height"] <= panel.bounding_box()["y"] + panel.bounding_box()["height"]
        context.close()


def interactions(browser, base, axe):
    context = browser.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
    page = context.new_page()
    open_route(page, base, "/")
    page.keyboard.press("Tab")
    expect(page.get_by_role("link", name="Naar de inhoud")).to_be_focused()
    page.keyboard.press("Enter")
    expect(page.locator("main")).to_be_focused()
    initial = page.get_by_role("radio", name="We hebben tijdelijk versterking nodig")
    choice = page.get_by_role("radio", name="We zoeken richting voor een verandering")
    expect(initial).to_be_checked()
    initial.focus()
    page.keyboard.press("ArrowDown")
    expect(choice).to_be_checked()
    expect(choice).to_be_focused()
    expect(initial).not_to_be_checked()
    answer = page.get_by_role("link", name="Bekijk organisatieadvies")
    expect(answer).to_be_visible()
    panel = page.locator(".question-answer:visible")
    assert panel.evaluate("(el) => getComputedStyle(el).animationDuration") == "0s"
    page.get_by_role("link", name="Bespreek deze situatie").click()
    expect(page).to_have_url(base + "/contact/?onderwerp=organisatieadvies")
    expect(page.get_by_role("textbox", name="Bericht")).to_have_value("Ik wil graag kennismaken over organisatieadvies.\n\n")
    page.go_back(wait_until="networkidle")
    if not choice.is_checked():
        initial.focus()
        page.keyboard.press("ArrowDown")
    answer.click()
    expect(page).to_have_url(base + "/diensten/#organisatieadvies")
    dienst = page.get_by_role("tab", name="Diensten")
    dienst.focus()
    page.keyboard.press("ArrowRight")
    training = page.get_by_role("tab", name="Trainingen")
    expect(training).to_be_focused()
    expect(training).to_have_attribute("aria-selected", "true")
    expect(page.get_by_role("tabpanel", name="Trainingen")).to_be_visible()
    expect(page.get_by_role("tabpanel", name="Diensten", include_hidden=True)).to_be_hidden()
    if axe:
        audit(page, axe)
    page.go_back(wait_until="networkidle")
    expect(dienst).to_have_attribute("aria-selected", "true")
    page.reload(wait_until="networkidle")
    expect(dienst).to_have_attribute("aria-selected", "true")
    page.get_by_role("link", name="Bespreek interimmanagement").click()
    expect(page.get_by_role("textbox", name="Bericht")).to_have_value("Ik wil graag kennismaken over interimmanagement.\n\n")
    page.get_by_role("link", name="Privacyverklaring").first.click()
    expect(page).to_have_url(base + "/privacy/")
    response = page.goto(base + "/bestaat-niet/")
    assert response.status == 404
    expect(page.get_by_role("heading", name="Pagina niet gevonden.")).to_be_visible()
    page.get_by_role("link", name="Naar de homepage").click()
    expect(page).to_have_url(base + "/")
    main_nav = page.get_by_role("navigation", name="Hoofdnavigatie")
    for label, route in (("Diensten", "/diensten/"), ("Contact", "/contact/"), ("Home", "/")):
        main_nav.get_by_role("link", name=label).click()
        expect(page).to_have_url(base + route)
    context.close()

    mobile = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    page = mobile.new_page()
    open_route(page, base, "/")
    page.get_by_text("We zoeken richting voor een verandering", exact=True).tap()
    expect(page.get_by_role("link", name="Bekijk organisatieadvies")).to_be_visible()
    page.get_by_text("We willen een knelpunt aanpakken", exact=True).tap()
    expect(page.get_by_role("link", name="Bekijk organisatieverbetering")).to_be_visible()
    expect(page.get_by_role("radio", checked=True)).to_have_count(1)
    page.get_by_role("link", name="Bespreek deze situatie").tap()
    expect(page).to_have_url(base + "/contact/?onderwerp=verbetering")
    expect(page.get_by_role("textbox", name="Bericht")).to_have_value("Ik wil graag kennismaken over organisatieverbetering.\n\n")
    open_route(page, base, "/")
    page.get_by_role("link", name="Bekijk de trainingsthema’s").tap()
    expect(page.get_by_role("tab", name="Trainingen")).to_have_attribute("aria-selected", "true")
    mobile.close()

    no_script = browser.new_context(java_script_enabled=False)
    page = no_script.new_page()
    open_route(page, base, "/")
    page.get_by_text("We zoeken richting voor een verandering", exact=True).click()
    expect(page.get_by_role("link", name="Bekijk organisatieadvies")).to_be_visible()
    open_route(page, base, "/diensten/")
    expect(page.get_by_role("heading", name="Organisatieontwikkeling", exact=True)).to_be_visible()
    open_route(page, base, "/contact/")
    expect(page.locator("noscript")).to_be_visible()
    expect(page.get_by_role("button", name="Verstuur bericht")).to_be_disabled()
    assert page.get_by_role("link", name="info@involfit.nl").first.get_attribute("href") == "mailto:info@involfit.nl"
    no_script.close()


def contact(browser, base, mock_base, axe):
    page = browser.new_page()
    open_route(page, base, "/contact/")
    name = page.get_by_role("textbox", name="Naam")
    email = page.get_by_role("textbox", name="E-mailadres")
    message = page.get_by_role("textbox", name="Bericht")
    submit = page.get_by_role("button", name="Verstuur bericht")
    submit.click()
    expect(name).to_be_focused()
    name.fill("   ")
    email.fill("test@example.com")
    message.fill("Testbericht")
    with page.expect_response("**/api/contact") as received:
        submit.click()
    assert received.value.status == 400, received.value.text()
    expect(name).to_have_attribute("aria-invalid", "true")
    expect(name).to_be_focused()
    if axe:
        audit(page, axe)
    name.fill("Testpersoon")
    with page.expect_response("**/api/contact") as received:
        submit.click()
    assert received.value.status == 503, received.value.text()
    expect(page.get_by_role("alert")).to_contain_text("tijdelijk niet beschikbaar")
    expect(message).to_have_value("Testbericht")

    open_route(page, mock_base, "/contact/")
    name.fill("Testpersoon")
    email.fill("test@example.com")
    message.fill("Testbericht")
    with page.expect_response("**/api/contact") as received:
        submit.click()
    assert received.value.status == 200, received.value.text()
    expect(page.get_by_role("status")).to_contain_text("Uw bericht is verstuurd")
    expect(message).to_have_value("")
    page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenshots", type=Path)
    parser.add_argument("--axe", type=Path)
    parser.add_argument("--results", type=Path)
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    with serve() as base, serve(mock=True) as mock_base, sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"), args=["--no-sandbox"])
        layout_matrix(browser, base, args.screenshots, args.axe)
        enlarged_text(browser, base)
        interactions(browser, base, args.axe)
        contact(browser, base, mock_base, args.axe)
        results = {
            "status": "passed",
            "chromium": browser.version,
            "widths": VIEWPORTS,
            "routes": list(ROUTES),
            "layoutChecks": len(ROUTES) * len(VIEWPORTS),
            "reflowReferenceWidth": 320,
            "textResizeChecks": 3 * len(ROUTES),
            "automatedAxeScans": 10 if args.axe else 0,
            "interactions": ["skip link", "worktable with prefilled contact topic", "keyboard tabs", "history", "touch", "reduced motion", "no JavaScript fallback", "custom 404"],
            "contact": ["native validation", "400 server validation", "503 missing mail configuration", "200 with injected provider"],
        }
        browser.close()
    summary = json.dumps(results, indent=2)
    if args.results:
        args.results.write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
