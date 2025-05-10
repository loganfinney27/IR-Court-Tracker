# scraper/urls.py
import csv


def load_urls(filename="case_urls.csv"):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
