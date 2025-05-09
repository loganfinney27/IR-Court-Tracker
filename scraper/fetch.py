# scraper/fetch.py
import time
import random
import requests

session = requests.Session()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
]

def get_headers():
    return {"User-Agent": random.choice(user_agents)}


def fetch_ready_page(url, session=session, headers=None, max_retries=5, delay=5):
    headers = headers or get_headers()
    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                return response
            print(f"Attempt {attempt + 1}: Status {response.status_code}, retrying in {delay} seconds...")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}: Error fetching {url} - {e}, retrying in {delay} seconds...")
        time.sleep(delay)
    print(f"Failed to fetch {url} after {max_retries} attempts.")
    return None
