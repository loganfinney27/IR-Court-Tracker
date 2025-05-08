# scraper/failures.py
import csv

def log_failure(topic, url, reason, filename="failed_urls.csv"):
    with open(filename, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Topic", "URL", "Reason"])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({"Topic": topic, "URL": url, "Reason": reason})
