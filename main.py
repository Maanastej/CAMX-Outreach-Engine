import asyncio
import os
import pandas as pd
from dotenv import load_dotenv
from scraper.scraper import CAMXScraper
from enrichment.enricher import SimpleEnricher
from enrichment.personalizer import GroqPersonalizer
from sheets.gsheets_uploader import GSheetsUploader

load_dotenv()

async def main():
    print("--- CAMX GTM Outreach Engine ---", flush=True)
    
    # 1. Scraping
    scraper = CAMXScraper("https://camx2026.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm?featured=false")
    df = await scraper.scrape(limit=15)
    
    if df.empty:
        print("No data scraped. Ensure you have internet and the site layout hasn't changed.", flush=True)
        return

    # 2. Enrichment
    enricher = SimpleEnricher()
    df = enricher.enrich_dataframe(df)

    # 3. AI Personalization
    try:
        personalizer = GroqPersonalizer()
        df = personalizer.generate_first_lines(df)
    except Exception as e:
        print(f"Skipping AI Personalization: {e}", flush=True)
        df['personalized_first_line'] = "Noticed your focus on advanced materials — curious how your CAMX showcase is coming along."

    # 4. Save Locally
    output_path = "output/final_enriched_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Final data saved to {output_path}", flush=True)

    # 5. Upload to Google Sheets
    uploader = GSheetsUploader()
    uploader.upload_data(df)

    print("--- Workflow Complete ---", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
