## Customer Experience Analytics for Fintech Apps

**Overview**

This project analyzes customer reviews of Ethiopian banks' mobile apps. It collects, preprocesses, and analyzes Google Play Store reviews to derive actionable insights for app improvement.

Project Structure
data/ – Contains raw and cleaned CSVs.
scripts/ – Python scripts for scraping and preprocessing.
notebooks/ – Jupyter notebooks for exploratory analysis and Task 2 sentiment analysis.
configs/ – Configuration files (.env, requirements.txt).
README.md – This file.
**Tasks**
## Task 1: Data Collection and Preprocessing
- Scrape 400+ unique reviews per bank using google-play-scraper.
- Clean the data (remove duplicates, handle <5% missing values, and normalize dates to YYYY-MM-DD).
- Export final CSV with columns: review, rating, date, bank, source.

## Task 2: Sentiment and Thematic Analysis (Partial)
- Use NLP tools (e.g., VADER or Hugging Face models) to compute sentiment labels and scores.
- Extract keywords to identify themes from the reviews.
- Setup & Execution
Install dependencies:
```bash pip install -r requirements.txt```
Configure environment variables in configs/.env.
Run scraping/preprocessing:
python src/scrape_and_preprocess.py
Open the notebooks in notebooks/ for further analysis.