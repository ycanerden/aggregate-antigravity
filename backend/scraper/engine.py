import asyncio
from playwright.async_api import async_playwright
from config import HEADLESS_BROWSER

async def fetch_portfolio_html(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS_BROWSER, args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=45000)
            # scroll explicitly
            for _ in range(5):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(1500)
                
            await page.wait_for_timeout(3000)
            html = await page.content()
            return html
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            raise
        finally:
            await browser.close()
