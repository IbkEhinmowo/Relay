import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def _scrape_single_url(context, url: str):
    """Helper function to scrape a single URL."""
    page = await context.new_page()
    try:
        await stealth_async(page)
        await page.goto(url)
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
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        
        tasks = [_scrape_single_url(context, url) for url in urls]
        scraped_texts = await asyncio.gather(*tasks)
        
        await browser.close()

    # for text in scraped_texts:
    #     print(text) 

    return scraped_texts

# if __name__ == "__main__":
#     # Define the list of URLs you want to scrape here
#     urls_to_scrape = [
#         "https://www.reddit.com/r/discordapp/comments/1emu7eh/i_created_a_llm_powered_discord_bot_that_can_also/"
#     ]

#     print(f"--- Starting to scrape {len(urls_to_scrape)} URL(s) ---")
    
#     # asyncio.run() 
#     scraped_results = asyncio.run(scrape(urls_to_scrape))
    
#     print("\n--- Scraping complete ---")

    