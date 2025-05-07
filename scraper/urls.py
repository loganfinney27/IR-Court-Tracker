# scraper/urls.py
import csv

def load_urls(filename="case_urls.csv"):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [{"topic": row["topic"], "url": row["url"]} for row in reader]
