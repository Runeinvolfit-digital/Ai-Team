"""Exercise the site served by a local static HTTP server in Chromium."""

import argparse
import json
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

PAGES = {"": "aanbod", "woning/": "woning", "tour/": "tour"}
ROOMS = ("Hal", "Woonkamer", "Keuken", "Overloop", "Slaapkamer", "Badkamer")
BROWSER = os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium")


def show(page, url):
    response = page.goto(url, wait_until="networkidle")
    assert response and response.ok, url
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), url


def check_tour(page, base, device):
    page.get_by_role("link", name="Bekijk woning", exact=True).click()
    page.get_by_role("link", name="Start de 360°-woningtour").click()
    canvas = page.locator("#panorama")
    expect(canvas).to_be_visible()
    expect(page.locator("#room-name")).to_have_text("Woonkamer")
    before = canvas.screenshot()
    canvas.focus()
    canvas.press("ArrowRight")
    assert before != canvas.screenshot(), "Pijltoets moet het zicht draaien."
    canvas.press("ArrowLeft")
    if device == "desktop":
        box = canvas.bounding_box()
        x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        baseline = canvas.screenshot()
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x - 80, y, steps=3)
        page.mouse.up()
        assert baseline != canvas.screenshot(), "Slepen moet het zicht draaien."
        page.reload()
        expect(canvas).to_be_visible()
    hotspot = page.get_by_role("button", name="Naar de keuken")
    if device == "mobiel":
        hotspot.tap()
    else:
        hotspot.click()
    expect(page.locator("#room-name")).to_have_text("Keuken")
    expect(canvas).to_be_visible()
    page.go_back()
    expect(page.locator("#room-name")).to_have_text("Woonkamer")
    expect(canvas).to_be_visible()
    for i, room in enumerate(ROOMS):
        floor = "Begane grond" if i < 3 else "Eerste verdieping"
        page.get_by_role("button", name=floor, exact=True).click()
        room_button = page.get_by_role("button", name=room, exact=True)
        room_button.click()
        expect(room_button).to_have_attribute("aria-pressed", "true")
        expect(page.locator("#room-name")).to_have_text(room)
        expect(canvas).to_be_visible()
    show(page, base + "woning/")
    show(page, base + "tour/#hal")
    expect(canvas).to_be_visible()
    expect(page.locator("#room-name")).to_have_text("Hal")
    page.get_by_role("link", name="Terug naar woning").click()
    expect(page).to_have_url(base + "woning/")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:43831/")
    parser.add_argument("--review", type=Path, default=Path("review"))
    args = parser.parse_args()
    args.review.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=BROWSER, args=["--no-sandbox", "--enable-unsafe-swiftshader"])
        version = browser.version
        for width, height, device in [(1440, 950, "desktop"), (390, 844, "mobiel"), (320, 700, "")]:
            page = browser.new_page(viewport={"width": width, "height": height}, has_touch=width < 500, is_mobile=width < 500)
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("response", lambda response: errors.append(f"{response.status} {response.url}") if response.status >= 400 else None)
            for path, name in PAGES.items():
                show(page, args.base + path)
                if path == "tour/":
                    expect(page.locator("#panorama")).to_be_visible()
                    expect(page.get_by_role("button", name="Naar de keuken")).to_be_visible()
                else:
                    assert page.locator("img").first.evaluate("img => img.complete && img.naturalWidth > 0")
                if device:
                    page.screenshot(path=args.review / f"{name}-{device}.png", full_page=True)
            show(page, args.base)
            if width < 500:
                toggle = page.get_by_role("button", name="Filters", exact=True)
                expect(toggle).to_have_attribute("aria-expanded", "false")
                toggle.tap()
                expect(toggle).to_have_attribute("aria-expanded", "true")
            page.locator("#price").select_option("500000")
            expect(page.locator("#result")).to_have_text("0 woningen")
            page.get_by_role("button", name="Wis filters").click()
            expect(page.locator("#result")).to_have_text("1 woning")
            if device:
                check_tour(page, args.base, device)
            page.close()
        browser.close()

        fallback = playwright.chromium.launch(executable_path=BROWSER, args=["--no-sandbox", "--disable-webgl"])
        page = fallback.new_page()
        show(page, args.base + "tour/")
        expect(page.locator("#room-photo")).to_be_visible()
        expect(page.locator("#panorama")).to_be_hidden()
        page.get_by_role("button", name="Naar de keuken").click()
        expect(page.locator("#room-name")).to_have_text("Keuken")
        expect(page.locator("#room-photo")).to_have_attribute("src", args.base + "assets/keuken.webp")
        fallback.close()

    assert not errors, errors
    result = {"status": "passed", "chromium": version, "widths": [1440, 390, 320],
              "pages": list(PAGES.values()), "rooms": ROOMS, "webglFallback": "passed"}
    (args.review / "test-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
