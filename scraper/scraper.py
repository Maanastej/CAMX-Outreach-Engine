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
            # Confirmed selector for MapYourShow 8.0 exhibitor links
            selector = "a[href*='exhibitor-details.cfm']"
            try:
                await page.wait_for_selector(selector, timeout=30000)
            except:
                print("Selector not found. The page might be protected or layout changed.")
                await browser.close()
                return pd.DataFrame()

            exhibitor_elements = await page.query_selector_all(selector)
            links = []
            for el in exhibitor_elements:
                name = await el.inner_text()
                href = await el.get_attribute("href")
                # Filter out empty names or non-exhibitor links
                if name.strip() and href and "/exhibitor-details.cfm" in href:
                    # Clean the URL
                    clean_url = href
                    if not clean_url.startswith("http"):
                        clean_url = f"https://camx2026.mapyourshow.com{clean_url}"
                    links.append({"name": name.strip(), "url": clean_url})

            # Remove duplicates while preserving order
            seen = set()
            unique_links = []
            for l in links:
                if l['url'] not in seen:
                    unique_links.append(l)
                    seen.add(l['url'])
            
            links = unique_links
            
            if limit:
                links = links[:limit]

            print(f"Found {len(links)} unique exhibitors. Starting detail extraction...")

            results = []
            for i, link in enumerate(links):
                print(f"[{i+1}/{len(links)}] Scraping: {link['name']}")
                detail_data = await self.scrape_detail(page, link['url'])
                detail_data['name'] = link['name']
                results.append(detail_data)
                await asyncio.sleep(random.uniform(1, 2))

            await browser.close()
            
            df = pd.DataFrame(results)
            df.to_csv(self.output_path, index=False)
            print(f"Saved {len(df)} records to {self.output_path}")
            return df

    async def scrape_detail(self, page, url):
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3) # Wait for JS rendering

            # Website: Look for external links that aren't MapYourShow
            website = ""
            all_links = await page.query_selector_all("a[target='_blank']")
            for link in all_links:
                href = await link.get_attribute("href")
                if href and "http" in href and "mapyourshow.com" not in href:
                    website = href
                    break

            # Booth: Often in a span or paragraph
            booth_el = await page.query_selector(".mys-booth, .booth-number, p:has-text('Booth')")
            booth = await booth_el.inner_text() if booth_el else ""
            
            # Description: Look for the main bio div
            desc_el = await page.query_selector(".mys-exhibitor-details-description, .section--description, p")
            description = await desc_el.inner_text() if desc_el else ""

            # Categories: Grid list
            category_els = await page.query_selector_all(".o-List_Columns--grid li, .section--list__columns-wrapper a")
            categories = [await c.inner_text() for c in category_els]
            # Filter categories to avoid duplicates and non-categories
            categories = list(set([c.strip() for c in categories if c.strip()]))

            return {
                "source_url": url,
                "website": website,
                "booth": booth.replace("Booth:", "").replace("Visit booth", "").strip(),
                "description": description.strip(),
                "categories": ", ".join(categories)
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {"source_url": url, "website": "", "booth": "", "description": "", "categories": ""}

if __name__ == "__main__":
    scraper = CAMXScraper("https://camx2026.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm?featured=false")
    asyncio.run(scraper.scrape(limit=5))
