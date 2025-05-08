# scraper/parser.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import re

def parse_case_page(html, url, detail="", topic=""):
    base_url = "https://www.courtlistener.com"
    soup = BeautifulSoup(html, "html.parser")

    full_title = soup.title.string.strip() if soup.title else "N/A"
    title = re.split(r", \d", full_title)[0]

    court_name_tag = soup.find("h2")
    court_name = court_name_tag.get_text(strip=True) if court_name_tag else "N/A"

    date_filed = "N/A"
    headers = soup.find_all("span", class_="meta-data-header")
    for header in headers:
        if "Date Filed:" in header.get_text():
            value_span = header.find_next_sibling("span", class_="meta-data-value")
            if value_span:
                raw_date = value_span.get_text(strip=True).replace('.', '')
                try:
                    parsed_date = datetime.strptime(raw_date, "%B %d, %Y")
                    date_filed = parsed_date.strftime("%B %d, %Y")
                except ValueError:
                    date_filed = raw_date
            break

    entry_divs = soup.find_all("div", id=lambda x: x and x.startswith("entry-"))
    latest_date = "N/A"
    latest_link = "N/A"

    if entry_divs:
        latest_entry = entry_divs[-1]
        entry_text = latest_entry.get_text(separator=" ", strip=True)

        date_match = re.search(r"[A-Z][a-z]{2}\.? \d{1,2}, \d{4}", entry_text)
        if date_match:
            raw_date = date_match.group(0).replace('.', '')
            try:
                parsed_date = datetime.strptime(raw_date, "%b %d, %Y")
                latest_date = parsed_date.strftime("%b %d, %Y")
            except ValueError:
                latest_date = raw_date

        a_tag = latest_entry.find("a", href=True)
        if a_tag:
            latest_link = urljoin(base_url, a_tag["href"])

    return {
        "Case":  f'<a href="{url}">{title}</a>',
        "Topic": topic,
        "Original Filing": f'<a href="{url}">{date_filed}</a>',
        "Latest Filing": f'<a href="{latest_link}">{latest_date}</a>',
        "Detail": detail,
    }
