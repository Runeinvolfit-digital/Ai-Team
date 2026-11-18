"""Exercise the showroom in Chromium against a running static HTTP server."""

import argparse
import json
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

MODELS = {"aurelio-gt": "Aurelio GT", "veldt-touring": "Veldt Touring"}
WIDTHS = (320, 390, 1440)


def load(page, url):
    response = page.goto(url, wait_until="networkidle")
    assert response and response.ok, url
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), url
    for img in page.locator("img:visible").all():
        expect(img).to_be_visible()
        assert img.evaluate("img => img.complete && img.naturalWidth > 0"), url


def check_detail(page, name, narrow):
    image = page.locator("#car-image")
    original = image.get_attribute("src")
    for index in range(1, 9):
        image_url = f"-{index % 8}.webp"
        page.get_by_role("button", name="Draai naar rechts").click()
        expect(image).to_have_attribute("src", original.replace("-0.webp", image_url))
        image.evaluate("img => img.decode()")
    page.locator("#stage").press("ArrowLeft")
    expect(image).to_have_attribute("src", original.replace("-0.webp", "-7.webp"))
    stage = page.locator("#stage")
    stage.scroll_into_view_if_needed()
    box = stage.bounding_box()
    x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x + 54, y, steps=4)
    page.mouse.up()
    expect(image).to_have_attribute("src", original)
    if narrow:
        cdp = page.context.new_cdp_session(page)
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]})
        cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x - 54, "y": y}]})
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
        expect(image).to_have_attribute("src", original.replace("-0.webp", "-7.webp"))
        page.get_by_role("button", name="Draai naar rechts").click()
    page.get_by_role("button", name="Interieur").click()
    expect(image).to_have_attribute("src", original.replace("-0.webp", "-interieur.webp"))
    image.evaluate("img => img.decode()")
    expect(page.get_by_role("button", name="Draai naar rechts")).to_be_hidden()
    page.get_by_role("button", name="Exterieur").click()
    expect(image).to_have_attribute("src", original)
    page.get_by_role("link", name="Vraag een proefrit aan").click()
    page.get_by_role("button", name="Bekijk demokeuze").click()
    expect(page.locator("#drive-status")).to_be_empty()
    page.get_by_label("Voorkeursmoment").select_option("Middag")
    page.get_by_role("button", name="Bekijk demokeuze").click()
    expect(page.locator("#drive-status")).to_have_text(f"{name} · middag. Dit is een demokeuze.")
    assert page.evaluate("location.hash") == "#proefrit"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:43832/")
    parser.add_argument("--review", type=Path, default=Path("review"))
    args = parser.parse_args()
    args.review.mkdir(parents=True, exist_ok=True)
    errors = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"),
            args=["--no-sandbox"],
        )
        version = browser.version
        for width in WIDTHS:
            device = "desktop" if width == 1440 else "mobiel" if width == 390 else ""
            page = browser.new_page(
                viewport={"width": width, "height": 960 if width == 1440 else 844},
                is_mobile=width < 500, has_touch=width < 500,
            )
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("response", lambda response: errors.append(f"{response.status} {response.url}") if response.status >= 400 else None)
            load(page, args.base)
            if device:
                page.screenshot(path=args.review / f"aanbod-{device}.png", full_page=True)
            page.get_by_label("Merk").select_option("Aurelio")
            expect(page.locator("#result")).to_have_text("1 demoauto")
            page.get_by_label("Budget").select_option("50000")
            expect(page.locator("#result")).to_have_text("0 demoauto’s")
            page.get_by_role("button", name="Wis filters").click()
            page.get_by_label("Brandstof").select_option("Hybride")
            expect(page.locator("#cars")).to_contain_text("Veldt Touring")
            expect(page.locator("#cars")).not_to_contain_text("Aurelio GT")
            page.get_by_role("button", name="Wis filters").click()
            for model, name in MODELS.items():
                page.get_by_role("link", name=name, exact=False).click()
                expect(page.get_by_role("heading", level=1)).to_have_text(name)
                load(page, args.base + f"auto/?model={model}")
                if device:
                    page.screenshot(path=args.review / f"{model}-{device}.png", full_page=True)
                check_detail(page, name, width < 500)
                page.get_by_role("link", name="Terug naar autoaanbod").click()
                expect(page.get_by_role("heading", level=1)).to_have_text("Autoaanbod")
            load(page, args.base + "auto/?model=onbekend")
            expect(page.locator("#missing")).to_be_visible()
            page.close()
        browser.close()

    assert not errors, errors
    result = {"status": "passed", "chromium": version, "widths": WIDTHS, "models": list(MODELS),
              "checks": ["filters", "all 8 exterior angles", "keyboard", "drag", "touch", "interior", "demo test drive", "unknown model"]}
    (args.review / "test-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
