# main.py
import os
from scraper.urls import load_urls
from scraper.fetch import fetch_ready_page
from scraper.parser import parse_case_page
from scraper.pipeline import write_to_csv
from scraper.failures import log_failure

def main():
    if os.path.exists("failed_urls.csv"):
        os.remove("failed_urls.csv")

    cases = load_urls()
    rows = []

    for case in cases:
        topic = case["topic"]
        url = case["url"]

        response = fetch_ready_page(url, delay=2)
        if response is None:
            reason = "Failed to fetch (non-200 response)"
            log_failure(topic, url, reason)
        print(f"Skipping {topic} ({url})")
        continue

        row = parse_case_page(response.text, url)
        row["Topic"] = topic
        rows.append(row)

    write_to_csv(rows)

if __name__ == "__main__":
    main()
