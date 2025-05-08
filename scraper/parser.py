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

    entry_divs = soup.find_all("div", id=lambda x: x and x.startswith("entry-"))

    latest_date = "N/A"
    latest_link = "N/A"

    if entry_divs:
        latest_entry = entry_divs[-1]
        entry_text = latest_entry.get_text(separator=" ", strip=True)

        date_match = re.search(r"[A-Z][a-z]{2} \d{1,2}, \d{4}", entry_text)
        if date_match:
            raw_date = date_match.group(0)
            try:
                parsed_date = datetime.strptime(raw_date, "%b %d, %Y")
                latest_date = parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                latest_date = raw_date

        a_tag = latest_entry.find("a", href=True)
        if a_tag:
            latest_link = urljoin(base_url, a_tag["href"])

    return {
        "Case": title,
        "Topic": topic,
        "Original Filing": f'<a href="{url}">Document</a>',
        "Latest Filing": f'<a href="{latest_link}">{latest_date}</a>',
        "Detail": detail
    }
