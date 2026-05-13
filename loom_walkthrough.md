# Loom Walkthrough Script: CAMX GTM Outreach Engine

**Duration**: 5–8 Minutes

---

## 1. Introduction (30 Seconds)
"Hi, I’m [Name]. Today, I’m walking you through the CAMX GTM Outreach Engine—a custom automation built to help GTM teams turn raw conference data into high-converting outreach pipelines. We’re targeting the CAMX 2026 exhibitor gallery, enriching the data, and using AI to write personalized openers."

## 2. The Scraper Logic (1 Minute)
"First, let’s look at the scraper. MapYourShow galleries are notoriously dynamic, so I used **Playwright** to handle the heavy JavaScript rendering. 
- We navigate to the gallery.
- Extract unique exhibitor links.
- Visit each individual detail page.
The scraper handles rate limiting and captures booth numbers, descriptions, and websites into a clean pandas DataFrame."

## 3. Enrichment Strategy (1 Minute)
"Once we have the data, we move to the enrichment phase. 
- I built a `SimpleEnricher` that uses heuristics to find LinkedIn URLs by checking the company website.
- It also performs **deterministic industry classification**. By scanning descriptions for terms like 'carbon fiber' or 'aerospace', we can categorize these companies automatically, which is critical for segmenting outreach."

## 4. Prompt Engineering & AI (2 Minutes)
"This is the heart of the engine. I’m using the **Groq API** with the **Llama-3.3-70b** model for speed and quality. 
The prompt I designed—which you can see in `prompts/personalization_prompt.txt`—is built on SDR best practices. 
Instead of saying 'I love your company,' the AI looks for a specific signal—like a certain composite tooling solution—and asks a curiosity-based question. 
This makes the email feel like it was written by a researcher, not a bot."

## 5. Google Sheets Integration (1 Minute)
"Finally, the data is pushed to Google Sheets via the `gspread` library. 
Using a service account allows this to run autonomously in the cloud or on a schedule. 
The result is a shared sheet where the sales team can immediately see the company details, their LinkedIn profile, and a ready-to-use personalized first line."

## 6. Closing (30 Seconds)
"The engine is modular, easy to scale, and focuses on the one thing that matters in GTM: quality at scale. Thanks for watching!"
