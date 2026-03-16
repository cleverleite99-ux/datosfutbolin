import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def scrape_flashscore():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto('https://www.flashscore.com/', wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(3000)
            match_urls = await page.evaluate('''
                () => {
                    const links = Array.from(document.querySelectorAll('a[href*="/match/football/"]'));
                    return links.map(link => link.href).filter(url => url.includes('flashscore.com/match/football/'));
                }
            ''')
            await browser.close()
            return match_urls
        except Exception as e:
            print(f"Error scraping flashscore: {e}")
            await browser.close()
            return []

async def main():
    urls = await scrape_flashscore()
    data = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "total_urls": len(urls),
        "urls": list(set(urls))
    }
    with open('urlstoday.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
    print(f"Scraped {len(urls)} URLs and saved to urlstoday.json")

if __name__ == '__main__':
    asyncio.run(main())
