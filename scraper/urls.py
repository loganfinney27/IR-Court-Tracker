# scraper/urls.py
import csv

INPUT_FILE = "case_urls.csv"

def load_urls(filename=INPUT_FILE):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]