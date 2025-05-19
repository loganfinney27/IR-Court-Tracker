# main.py
import os
import csv
from scraper.urls import load_urls
from scraper.fetch import session
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


        try:
            print(f"Fetching case page: {url}")
            response = session.get(url, timeout=10)
            if response.status_code != 200:
                reason = f"Status {response.status_code}"
                log_failure(topic, url, reason)
                print(f"Skipping {topic} ({url}) — {reason}")
                continue

            row = parse_case_page(response.text, url, detail=detail, topic=topic)
            rows.append(row)

        except Exception as e:
            reason = f"Exception: {e}"
            log_failure(topic, url, reason)
            print(f"Skipping {topic} ({url})")
            continue

        row = parse_case_page(response.text, url, detail=detail, topic=topic)
        rows.append(row)

    write_to_csv(rows)

    commit_and_push_outputs()

if __name__ == "__main__":
    main()
