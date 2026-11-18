"""Verify the built Astro site in Chromium against its Node server."""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    "/": "home",
    "/over-sander/": "over-sander",
    "/diensten/": "diensten",
    "/ervaring/": "ervaring",
    "/contact/": "contact",
    "/privacy/": "privacy",
}
VIEWPORTS = (320, 390, 768, 1024, 1440)


@contextmanager
def serve():
    script = """
    import {createWebsiteServer} from './server.mjs';
    const server = createWebsiteServer({config: {}});
    server.listen(0, '127.0.0.1', () => console.log(server.address().port));
    """
    with subprocess.Popen(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT, stdout=subprocess.PIPE, text=True,
    ) as server:
        try:
            yield f"http://127.0.0.1:{int(server.stdout.readline())}"
        finally:
            server.terminate()


def check_layout(browser, base, screenshots, axe):
    scans = 0
    for width in VIEWPORTS:
        page = browser.new_page(viewport={"width": width, "height": 844 if width <= 390 else 1000})
        for route, name in ROUTES.items():
            assert page.goto(base + route, wait_until="networkidle").ok
            page.evaluate("document.fonts.ready")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (route, width)
            expect(page.locator("h1")).to_be_visible()
            if width in (390, 1440):
                if axe:
                    page.add_script_tag(path=str(axe))
                    result = page.evaluate("async () => await axe.run({runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa']})")
                    assert not result["violations"], (route, width, [v["id"] for v in result["violations"]])
                    scans += 1
                if screenshots:
                    device = "desktop" if width == 1440 else "mobiel"
                    page.screenshot(path=screenshots / f"{name}-{device}.png", full_page=True, animations="disabled")
        page.close()
    return scans


def check_interactions(browser, base):
    page = browser.new_page(viewport={"width": 390, "height": 844}, has_touch=True, reduced_motion="reduce")
    page.goto(base)
    page.keyboard.press("Tab")
    expect(page.get_by_role("link", name="Naar de inhoud")).to_be_focused()
    menu = page.locator(".mobile-nav")
    summary = menu.locator("summary")
    summary.focus()
    page.keyboard.press("Enter")
    expect(menu).to_have_attribute("open", "")
    expect(menu.locator("nav")).to_have_css("animation-name", "none")
    expect(menu.get_by_role("link", name="Home")).to_have_attribute("aria-current", "page")
    page.keyboard.press("Escape")
    expect(menu).not_to_have_attribute("open", "")
    expect(summary).to_be_focused()
    summary.tap()
    menu.get_by_role("link", name="Diensten").tap()
    expect(page).to_have_url(base + "/diensten/")
    service = page.locator("#organisatieadvies")
    service.locator("summary").focus()
    page.keyboard.press("Enter")
    expect(service).to_have_attribute("open", "")
    expect(service.locator(".service-content")).to_have_css("animation-name", "none")
    service.get_by_role("link", name="Bekijk dit werkgebied").click()
    expect(page).to_have_url(base + "/ervaring/#organisatieadvies")
    page.get_by_role("link", name="Bespreek uw vraagstuk").click()
    expect(page.locator("main a")).to_have_attribute("href", "mailto:info@involfit.nl")
    page.goto(base)
    page.locator(".expertise-links").get_by_role("link", name="Organisatieverbetering").click()
    expect(page.locator("#verbetering")).to_have_attribute("open", "")
    page.close()

    page = browser.new_page(viewport={"width": 320, "height": 844}, java_script_enabled=False)
    page.goto(base + "/diensten/")
    page.locator(".mobile-nav summary").click()
    expect(page.locator(".mobile-nav nav")).to_be_visible()
    page.locator(".mobile-nav summary").click()
    page.locator("#organisatieadvies summary").click()
    expect(page.locator("#organisatieadvies .service-content")).to_be_visible()
    page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenshots", type=Path)
    parser.add_argument("--axe", type=Path)
    parser.add_argument("--results", type=Path)
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)

    with serve() as base, sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"),
            args=["--no-sandbox"],
        )
        scans = check_layout(browser, base, args.screenshots, args.axe)
        check_interactions(browser, base)
        results = {
            "status": "passed",
            "chromium": browser.version,
            "routes": list(ROUTES),
            "widths": VIEWPORTS,
            "layoutChecks": len(ROUTES) * len(VIEWPORTS),
            "axeScans": scans,
            "interactions": ["skip link", "mobile menu", "Escape and focus", "touch", "service accordion",
                             "service deep link", "experience", "mailto", "reduced motion", "no JavaScript"],
        }
        browser.close()

    summary = json.dumps(results, indent=2)
    if args.results:
        args.results.write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
