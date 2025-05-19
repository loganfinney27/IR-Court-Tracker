# main.py
import os
import csv
from scraper.urls import load_urls
from scraper.fetch import fetch_entry_page
from scraper.parser import parse_case_page
from scraper.pipeline import write_to_csv
from scraper.failures import log_failure
from scraper.commit import commit_and_push_outputs


def main():
    if os.path.exists("failed_urls.csv"):
        os.remove("failed_urls.csv")

    with open("failed_urls.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Topic", "URL", "Reason"])

    cases = load_urls()

    rows = []

    for case in cases:
        topic = case["topic"]
        url = case["url"]
        detail = case["detail"]

        response = fetch_ready_page(url, delay=2)
        if response is None:
            reason = "Failed to fetch (network error or non-200 response)"
            log_failure(topic, url, reason)
            print(f"Skipping {topic} ({url})")
            continue

        row = parse_case_page(response.text, url, detail=detail, topic=topic)
        rows.append(row)

    write_to_csv(rows)

    commit_and_push_outputs()

if __name__ == "__main__":
    main()
