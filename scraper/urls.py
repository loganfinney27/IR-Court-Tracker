# scraper/urls.py
def load_urls(filename="case_urls.txt"):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]
