import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

class SimpleEnricher:
    """
    Enriches company data with LinkedIn URLs and industry info using simple heuristics
    and lightweight search-like patterns.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def enrich_dataframe(self, df):
        print(f"Starting enrichment for {len(df)} companies...")
        
        enriched_data = []
        for index, row in df.iterrows():
            company_name = row['name']
            website = row.get('website', '')
            description = row.get('description', '')

            # Heuristic for LinkedIn (often companies have it on their site)
            linkedin_url = self._find_linkedin_on_site(website) if website else ""
            
            # Deterministic signals from description
            industry = self._detect_industry(description)
            keywords = self._extract_keywords(description)
            
            enriched_row = row.to_dict()
            enriched_row.update({
                "linkedin_url": linkedin_url,
                "industry": industry,
                "keywords": keywords,
                "enriched_summary": description[:200] + "..." if len(description) > 200 else description
            })
            enriched_data.append(enriched_row)
            
        return pd.DataFrame(enriched_data)

    def _find_linkedin_on_site(self, website):
        """Attempts to find a LinkedIn link on the company website."""
        if not website or not website.startswith("http"):
            return ""
        try:
            # We only try to fetch the homepage for LinkedIn links
            response = requests.get(website, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                if "linkedin.com/company" in href:
                    return href
        except:
            pass
        return ""

    def _detect_industry(self, description):
        """Simple keyword-based industry detection for CAMX exhibitors."""
        desc = description.lower()
        if any(w in desc for w in ["aerospace", "aircraft", "aviation", "uav"]):
            return "Aerospace & Defense"
        if any(w in desc for w in ["composite", "carbon fiber", "fiberglass", "prepreg"]):
            return "Composites Manufacturing"
        if any(w in desc for w in ["automotive", "vehicle", "car", "transportation"]):
            return "Automotive & Transportation"
        if any(w in desc for w in ["medical", "healthcare", "orthopedic"]):
            return "Medical Technology"
        if any(w in desc for w in ["energy", "wind", "turbine", "solar"]):
            return "Renewable Energy"
        if any(w in desc for w in ["software", "digital", "simulation", "ai"]):
            return "Engineering Software"
        return "Advanced Manufacturing"

    def _extract_keywords(self, description):
        """Extracts top relevant keywords from description."""
        technical_terms = [
            "CNC", "3D Printing", "Thermoplastic", "Resin", "Tooling", 
            "Vacuum Bagging", "Autoclave", "Pultrusion", "Injection Molding",
            "Carbon Fiber", "Graphene", "Nanotechnology", "Additive Manufacturing",
            "Filament Winding", "Prepreg", "NDI", "MRO"
        ]
        found = [term for term in technical_terms if term.lower() in description.lower()]
        return ", ".join(found)

if __name__ == "__main__":
    # Test logic
    enricher = SimpleEnricher()
    test_df = pd.DataFrame([{
        "name": "Advanced Composites Inc.",
        "website": "https://www.advancedcomposites.com",
        "description": "Specializing in carbon fiber solutions for aerospace and automotive industries."
    }])
    print(enricher.enrich_dataframe(test_df))
