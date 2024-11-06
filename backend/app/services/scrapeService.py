from datetime import datetime, timedelta
from app import db
from app.models.url_scrape import URLScrape
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re

def scrape_content(url):
    """
    Retrieves cached content from the database if available and recent; otherwise, scrapes content from the URL.
    """
    expiration_days = 7
    expiration_date = datetime.utcnow() - timedelta(days=expiration_days)

    existing_entry = URLScrape.query.filter_by(url=url).first()
    if existing_entry and existing_entry.last_scraped > expiration_date:
        print("Using cached content from database.")
        return existing_entry.scraped_content

    print("Scraping new content for URL.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        retries = 3
        for attempt in range(retries):
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_load_state("networkidle")
                break
            except Exception as e:
                if attempt < retries - 1:
                    print(f"Retrying... ({attempt + 1}/{retries})")
                else:
                    print("Failed to load page after retries.")
                    raise e

        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, 'html.parser')
    cleaned_content = clean_text(soup.get_text())

    if existing_entry:
        existing_entry.scraped_content = cleaned_content
        existing_entry.last_scraped = datetime.utcnow()
    else:
        new_entry = URLScrape(url=url, scraped_content=cleaned_content, last_scraped=datetime.utcnow())
        db.session.add(new_entry)

    db.session.commit()
    return cleaned_content

def clean_text(text):
    """
    Cleans text by reducing multiple whitespaces/newlines to a single newline.
    """
    return re.sub(r'\s*\n\s*', '\n', text).strip()
