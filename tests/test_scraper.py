import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Core.Integrations.scraper import scrape

async def test_Scraper():
    try:
        url = "https://quotes.toscrape.com"
        content = await scrape([url])
        print("Scraper test passed.")
    except Exception as e:
        print(f"Scraper test failed: {e}")
    
    
import asyncio

if __name__ == "__main__":
    answer = asyncio.run(test_Scraper())
 