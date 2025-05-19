# main.py
import os
import csv
from scraper.urls import load_urls
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

        row = parse_case_page(url, detail=detail, topic=topic)
        if row is None:
            reason = "Failed to fetch main case page"
            log_failure(topic, url, reason)
            print(f"Skipping {topic} ({url}) - {reason}")
            continue

        rows.append(row)

    write_to_csv(rows)
    commit_and_push_outputs()

if __name__ == "__main__":
    main()