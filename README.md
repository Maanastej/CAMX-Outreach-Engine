# CAMX GTM Outreach Engine 🚀

A professional, production-ready automation engine built for the GTM Engineering Internship Assignment at Precise Leads. This tool scrapes exhibitors from CAMX 2026, enriches company data, generates AI-personalized outreach lines using Groq, and syncs everything to Google Sheets.

## 🏗 Project Structure

```
CAMX_GTM_Outreach_Engine/
├── scraper/
│   ├── scraper.py          # Playwright-based exhibitor scraper
│   └── data/               # Local CSV storage
├── enrichment/
│   ├── enricher.py         # Deterministic enrichment & LinkedIn discovery
│   └── personalizer.py     # Groq AI personalization logic
├── prompts/
│   └── personalization_prompt.txt  # High-fidelity AI prompt
├── sheets/
│   └── gsheets_uploader.py  # Google Sheets integration (gspread)
├── output/
│   ├── final_enriched_data.csv
│   └── personalization_examples.md
├── main.py                 # Orchestration script
├── requirements.txt        # Dependencies
├── .env.example            # Environment template
└── README.md
```

## 🛠 Setup Instructions

### 1. Prerequisites
- Python 3.8+
- [Groq API Key](https://console.groq.com/)
- Google Service Account Credentials (`.json` file)

### 2. Installation
```bash
# Clone the repository
pip install -r requirements.txt
playwright install chromium
```

### 3. Configuration
Copy `.env.example` to `.env` and fill in your keys:
```bash
GROQ_API_KEY=your_key
GOOGLE_SHEET_ID=your_id
GOOGLE_SERVICE_ACCOUNT_FILE=path/to/credentials.json
```

### 4. Running the Engine
```bash
python main.py
```

## 🧠 Workflow Explanation

1.  **Scraping**: Uses **Playwright** to handle the dynamic MapYourShow gallery. It collects exhibitor names and visits each detail page to extract websites, booth numbers, and descriptions.
2.  **Enrichment**:
    -   **LinkedIn Discovery**: A lightweight heuristic search that checks the company website for social links.
    -   **Deterministic Logic**: Classifies industries and extracts technical keywords (e.g., "Carbon Fiber", "CNC") based on the scraped description.
3.  **AI Personalization**: Uses the **Groq API** (Llama-3.3-70b) with a specialized SDR prompt. The engine identifies a specific product signal (e.g., "lightweight tooling") and generates a natural-sounding opener.
4.  **Google Sheets**: Automatically authenticates via a Service Account and updates a designated sheet with the final enriched dataset.

## 🎯 Personalization Quality
The prompt is designed to avoid "fluff" and "generic compliments." Instead, it focuses on:
-   **Observation**: "Noticed you're showcasing..."
-   **Relevance**: "...specifically for aerospace-grade resins."
-   -   **Curiosity**: "...curious how the new benchmarks are impacting your yield."

## 📜 Loom Walkthrough Talking Points
1.  **Introduction**: Overview of the CAMX Outreach Engine and the GTM problem it solves.
2.  **Scraper**: Explaining why Playwright is used for MapYourShow's dynamic structure.
3.  **Enrichment**: How we find LinkedIn URLs and classify industries without heavy APIs.
4.  **Prompt Engineering**: Breakdown of the SDR prompt and why it produces human-like openers.
5.  **Google Sheets**: Showing the live sync and data structure.
6.  **Outreach Impact**: How these personalized lines increase open and reply rates for SDRs.

## 🚀 Suggested Improvements
-   **Scale**: Add proxy rotation for large-scale scraping (1000+ exhibitors).
-   **CRM Integration**: Directly push to HubSpot or Salesforce instead of just Google Sheets.
-   **Email Automation**: Integrate with Instantly.ai or Smartlead.ai to trigger campaigns automatically.
-   **Enhanced Search**: Use a SERP API (like Serper.dev) for more reliable LinkedIn URL discovery.
