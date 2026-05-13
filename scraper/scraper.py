import asyncio
import pandas as pd
from playwright.async_api import async_playwright
import os
import random

class CAMXScraper:
    def __init__(self, base_url, output_path="scraper/data/exhibitors.csv"):
        self.base_url = base_url
        self.output_path = output_path
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    async def scrape(self, limit=None):
        async with async_playwright() as p:
            # Use a realistic User-Agent to avoid 403s
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            print(f"Navigating to Gallery: {self.base_url}")
            await page.goto(self.base_url, wait_until="networkidle", timeout=60000)
            
            # MapYourShow often needs a bit of extra time for the JS to populate the list
            await asyncio.sleep(5)

            # Wait for exhibitor links to appear
            # Common MapYourShow selector for exhibitor names
            selector = "a.mys-exhibitor-name, a[data-exhid]"
            try:
                await page.wait_for_selector(selector, timeout=20000)
            except:
                print("Selector not found. The page might be protected or layout changed.")
                # Fallback: take a screenshot for debugging if this was a real run
                # await page.screenshot(path="debug_gallery.png")
                await browser.close()
                return pd.DataFrame()

            exhibitor_elements = await page.query_selector_all(selector)
            links = []
            for el in exhibitor_elements:
                name = await el.inner_text()
                href = await el.get_attribute("href")
                if href and "/exhibitor/" in href:
                    links.append({"name": name.strip(), "url": f"https://camx2026.mapyourshow.com{href}"})

            # Remove duplicates
            unique_links = {l['url']: l for l in links}.values()
            links = list(unique_links)
            
            if limit:
                links = links[:limit]

            print(f"Found {len(links)} exhibitors. Starting detail extraction...")

            results = []
            for i, link in enumerate(links):
                print(f"[{i+1}/{len(links)}] Scraping: {link['name']}")
                detail_data = await self.scrape_detail(page, link['url'])
                detail_data['name'] = link['name']
                results.append(detail_data)
                # Polite delay
                await asyncio.sleep(random.uniform(1, 3))

            await browser.close()
            
            df = pd.DataFrame(results)
            df.to_csv(self.output_path, index=False)
            print(f"Saved {len(df)} records to {self.output_path}")
            return df

    async def scrape_detail(self, page, url):
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)

            # Selectors based on standard MapYourShow templates
            website_el = await page.query_selector("a.mys-exhibitor-details-website, a[target='_blank']")
            booth_el = await page.query_selector(".mys-exhibitor-details-booth, .mys-booth-link")
            desc_el = await page.query_selector(".mys-exhibitor-details-description, #exhibitor-description")
            category_els = await page.query_selector_all(".mys-exhibitor-details-categories li, .mys-category-link")

            website = await website_el.get_attribute("href") if website_el else ""
            booth = await booth_el.inner_text() if booth_el else ""
            description = await desc_el.inner_text() if desc_el else ""
            categories = [await c.inner_text() for c in category_els]

            return {
                "source_url": url,
                "website": website,
                "booth": booth.replace("Booth:", "").strip(),
                "description": description.strip(),
                "categories": ", ".join(categories)
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {"source_url": url, "website": "", "booth": "", "description": "", "categories": ""}

if __name__ == "__main__":
    scraper = CAMXScraper("https://camx2026.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm?featured=false")
    asyncio.run(scraper.scrape(limit=5))
