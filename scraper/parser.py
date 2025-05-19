# scraper/parser.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import re
from scraper.fetch import fetch_entry_pages


def extract_entry_data(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    entry_div = soup.find("div", id=lambda x: x and x.startswith("entry-"))
    if not entry_div:
        return "N/A", "N/A"

    entry_text = entry_div.get_text(separator=" ", strip=True)
    date_match = re.search(r"[A-Z][a-z]{2}\.? \d{1,2}, \d{4}", entry_text)

    if date_match:
        raw_date = date_match.group(0).replace('.', '')
        try:
            parsed = datetime.strptime(raw_date, "%b %d, %Y")
            date = parsed.strftime("%b %d, %Y")
        except ValueError:
            date = raw_date
    else:
        date = "N/A"

    a_tag = entry_div.find("a", href=True)
    link = urljoin(base_url, a_tag["href"]) if a_tag else "N/A"

    return date, link


def parse_case_page(url, detail="", topic=""):
    base_url = "https://www.courtlistener.com"

    base_resp, first_resp, latest_resp = fetch_entry_pages(url)
    if not base_resp:
        return None  # Handle failure in main script

    soup = BeautifulSoup(base_resp.text, "html.parser")

    # ---- Case Title ----
    full_title = soup.title.string.strip() if soup.title else "N/A"
    title = re.split(r",\s*\d", full_title)[0]

    # ---- Court Name ----
    court_h2 = soup.find("h2")
    court = court_h2.get_text(strip=True) if court_h2 else "N/A"

    orig_date, orig_link = (
        extract_entry_data(first_resp.text, base_url) if first_resp else ("N/A", "N/A")
    )
    latest_date, latest_link = (
        extract_entry_data(latest_resp.text, base_url) if latest_resp else ("N/A", "N/A")
    )

    return {
        "Case": f'<a href="{url}">{title}</a>',
        "Topic": topic,
        "Original": f'<a href="{orig_link}">{orig_date}</a>',
        "Latest":  f'<a href="{latest_link}">{latest_date}</a>',
        "Tag": detail,
    }