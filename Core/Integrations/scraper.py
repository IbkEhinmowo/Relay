import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def _scrape_single_url(context, url: str):
    """Helper function to scrape a single URL."""
    stealth = Stealth()
    await stealth.apply_stealth_async(context)  # Apply stealth to the context
    page = await context.new_page()
    try:
        # Add additional headers to mimic a real browser
        await page.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-CH-UA': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # More robust navigation with timeout and wait until options
        try:
            await page.goto(url, wait_until='networkidle', timeout=60000)
        except Exception as e:
            print(f"Error navigating to {url}: {str(e)}")
            # Try alternative approach with load state
            await page.goto(url, wait_until='load', timeout=60000)
            # Wait for content to be likely loaded
            await page.wait_for_timeout(2000)
        
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # Tags to strip from the HTML
        tags_to_strip = [
            "script", "style", "noscript", "iframe", "svg", "canvas", 
            "meta", "link", "header", "footer", "nav", "aside", "form",
            "video", "img", "picture"
        ]
        for s in soup(tags_to_strip):
            s.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        return '\n'.join(line for line in lines if line)
    finally:
        await page.close()

async def scrape(urls: list[str]) -> list[str]:
    """
    Scrapes a list of URLs concurrently and returns their text content.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-web-security',
                '--disable-site-isolation-trials'
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=2,
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation'],
            java_script_enabled=True,
            bypass_csp=True,
            has_touch=False,
        )
        
        # Enable JavaScript and cookies
        await context.add_cookies([{
            'name': 'session_consent',
            'value': 'true',
            'domain': '.washingtonpost.com',
            'path': '/',
        }])
        
        results = []
        for url in urls:
            try:
                result = await _scrape_single_url(context, url)
                results.append(result)
            except Exception as e:
                print(f"Failed to scrape {url}: {str(e)}")
                results.append(f"Error scraping content: {str(e)}")
        
        await browser.close()

    return results

# if __name__ == "__main__":
#     # Define the list of URLs you want to scrape here
#     urls_to_scrape = [
#         "https://www.reddit.com/r/discordapp/comments/1emu7eh/i_created_a_llm_powered_discord_bot_that_can_also/"
#     ]

#     print(f"--- Starting to scrape {len(urls_to_scrape)} URL(s) ---")
    
#     # asyncio.run() 
#     scraped_results = asyncio.run(scrape(urls_to_scrape))
    
#     print("\n--- Scraping complete ---")

    