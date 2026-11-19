import json
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = 'https://www.carrefour.fr/p/console-ps5-slim-sony-0711719021247'
OUT = Path('docs')
OUT.mkdir(exist_ok=True)
result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'product_url': URL, 'status': 'not_verified', 'note': 'Store-by-store stock checking is not implemented or validated yet.'}
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale='fr-FR')
        page.goto(URL, wait_until='domcontentloaded', timeout=45000)
        result['page_title'] = page.title()
        result['status'] = 'product_page_reached'
        browser.close()
except Exception as exc:
    result['error'] = str(exc)[:300]
(OUT / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
