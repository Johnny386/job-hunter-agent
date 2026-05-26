from playwright.sync_api import sync_playwright
import os

def scrape_job(url: str) -> dict:
    try:
        with sync_playwright() as p:
            # Use system chromium on cloud, default on local
            chromium_path = "/usr/bin/chromium-browser" if os.path.exists("/usr/bin/chromium-browser") else None

            browser = p.chromium.launch(
                headless=True,
                executable_path=chromium_path
            )
            page = browser.new_page()

            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })

            page.goto(url, wait_until="networkidle", timeout=15000)
            page.wait_for_selector("body", timeout=10000)

            text = page.inner_text("body")
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = "\n".join(lines)
            clean_text = clean_text[:8000]

            browser.close()

            return {
                "raw_text": clean_text,
                "error": None
            }

    except Exception as e:
        return {
            "raw_text": None,
            "error": str(e)
        }