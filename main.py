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
    print("--- CAMX GTM Outreach Engine ---")
    
    # 1. Scraping
    scraper = CAMXScraper("https://camx2026.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm?featured=false")
    # For demonstration/testing, we'll limit to 5 if not specified otherwise
    # In a full run, we'd remove the limit
    df = await scraper.scrape(limit=10)
    
    if df.empty:
        print("No data scraped. Ensure you have internet and the site layout hasn't changed.")
        # Load mock data for demonstration if scraper fails (common in restricted environments)
        df = pd.DataFrame([
            {"name": "Hexcel Corporation", "website": "https://www.hexcel.com", "description": "Global leader in advanced composites technology, including carbon fiber and structural adhesives."},
            {"name": "Toray Composite Materials", "website": "https://www.toraycma.com", "description": "Producing high-quality carbon fiber for aerospace and industrial applications."},
            {"name": "Gurit", "website": "https://www.gurit.com", "description": "Specializing in advanced composite materials, engineering services, and tooling solutions."},
            {"name": "Owens Corning", "website": "https://www.owenscorning.com", "description": "Developing and producing insulation, roofing, and fiberglass composites."},
            {"name": "Solvay", "website": "https://www.solvay.com", "description": "Providing high-performance polymers and composite materials for extreme environments."},
        ])
        print("Using sample data for demonstration.")

    # 2. Enrichment
    enricher = SimpleEnricher()
    df = enricher.enrich_dataframe(df)

    # 3. AI Personalization
    try:
        personalizer = GroqPersonalizer()
        df = personalizer.generate_first_lines(df)
    except Exception as e:
        print(f"Skipping AI Personalization: {e}")
        df['personalized_first_line'] = "Noticed your focus on advanced materials — curious how your CAMX showcase is coming along."

    # 4. Save Locally
    output_path = "output/final_enriched_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Final data saved to {output_path}")

    # 5. Upload to Google Sheets
    uploader = GSheetsUploader()
    uploader.upload_data(df)

    print("--- Workflow Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
