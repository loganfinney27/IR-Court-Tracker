# main.py
from scraper.urls import load_urls
from scraper.fetch import fetch_ready_page
from scraper.parser import parse_case_page
from scraper.pipeline import write_to_csv

def main():
    cases = load_urls()
    rows = []

    for case in cases:
        topic = case["topic"]
        url = case["url"]

        response = fetch_ready_page(url, delay=2)
        if response is None:
            print(f"Skipping {topic} ({url})")
            continue

        row = parse_case_page(response.text, url)
        row["Topic"] = topic  # Add topic to output
        rows.append(row)

    write_to_csv(rows)

if __name__ == "__main__":
    main()
