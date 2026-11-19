import json
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://www.carrefour.fr/p/console-ps5-slim-sony-0711719021247"

OUT = Path("docs")
OUT.mkdir(exist_ok=True)

result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "product_url": URL,
    "status": "not_verified",
    "store_check": "not_implemented",
    "buttons": [],
}

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            locale="fr-FR",
            viewport={"width": 1280, "height": 900}
        )
        page.goto(URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3000)
        result["page_title"] = page.title()
        result["status"] = "product_page_reached"
        buttons = page.locator("button, [role='button']").all()
        for button in buttons[:100]:
            try:
                label = button.inner_text(timeout=1000).strip()
                if label:
                    result["buttons"].append(label[:120])
            except Exception:
                pass
        page.screenshot(path=str(OUT / "carrefour.png"), full_page=False)
        browser.close()
except Exception as exc:
    result["status"] = "error"
    result["error"] = str(exc)[:500]

(OUT / "results.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False))
