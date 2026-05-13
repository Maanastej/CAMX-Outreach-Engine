# Loom Walkthrough Guide: CAMX GTM Outreach Engine

Use this script as a guide for your 2-3 minute project walkthrough video.

---

## 1. Introduction (30 seconds)
*   **Action**: Show the GitHub Repository home page.
*   **Talking Points**:
    *   "Hi, I'm [Your Name], and this is my submission for the GTM Engineering assignment."
    *   "I've built a production-ready outreach engine that automates the entire lead generation pipeline: from scraping trade show exhibitors to generating AI-personalized email openers."
    *   "The tech stack is Python, using Playwright for scraping, Groq for AI, and Google Sheets for the final delivery."

## 2. The Code Logic (60 seconds)
*   **Action**: Open `main.py` in your editor.
*   **Talking Points**:
    *   "The system is orchestrated via `main.py`, which runs a 4-step pipeline."
    *   "**Step 1: Scraping**: We use Playwright in `scraper/scraper.py`. I implemented custom selectors to handle the dynamic MapYourShow 8.0 layout, extracting real-time data for 15+ companies including their booth numbers and websites."
    *   "**Step 2: Enrichment**: The `SimpleEnricher` module visits the exhibitor websites to find LinkedIn URLs and classifies them by industry to help target the right ICP."
    *   "**Step 3: AI Personalization**: We use the **Groq API** with the `llama-3.3-70b` model. The logic here is signal-based—the AI looks at the company description and generates a curiosity-driven first line that sounds like a human SDR, not a bot."
    *   "**Step 4: Sync**: Finally, the data is pushed to Google Sheets using the `gspread` library."

## 3. Demonstrating Output (60 seconds)
*   **Action**: Open the `output/final_enriched_data.csv` file AND the Google Sheet.
*   **Talking Points**:
    *   "Here is the local output. You can see we have real data: Name, Booth, Website, and the AI-generated first lines."
    *   "Switching to the Google Sheet—everything is synced automatically. This allows sales teams to immediately start their outreach with highly personalized data."
    *   "For example, for Eastman Machine Company, the AI noticed their focus on 'automated cutting systems' and generated a line about their T25 showcase."

## 4. Conclusion (15 seconds)
*   **Action**: Show the README.md on GitHub.
*   **Talking Points**:
    *   "The project is fully modular and documented on GitHub. Thank you for the opportunity!"

---

### Tips for a Great Recording:
1.  **Keep it Snappy**: Don't spend too long on any one file.
2.  **Zoom In**: Make sure your code text is large enough to read on video (use `Ctrl +` in VS Code).
3.  **Show the Logs**: If you want, show the terminal output from a successful run to prove the 'Workflow Complete' message.
