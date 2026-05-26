from playwright.sync_api import sync_playwright

def scrape_job(url: str) -> dict:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })

            page.goto(url, wait_until="networkidle", timeout=15000)

            # Wait for body content to load
            page.wait_for_selector("body", timeout=10000)

            # Grab full visible text
            text = page.inner_text("body")

            # Clean up excessive blank lines
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = "\n".join(lines)

            # Trim to 4000 chars
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