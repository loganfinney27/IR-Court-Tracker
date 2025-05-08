# scraper/pipeline.py
import csv

def write_to_csv(rows, filename="output.csv"):
    if not rows:
        print("No data to write.")
        return
    fieldnames = ["Case", "Topic", "Original Filing", "Latest Filing", "Detail"]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {filename}")
