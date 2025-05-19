# scraper/fetch.py
import time
import random
import requests
import json
import os
from datetime import datetime, timedelta

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
]

CACHE_FILE = "cache_202.json"
COOLDOWN_MINUTES = 15


def load_202_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_202_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def should_skip_url(url):
    cache = load_202_cache()
    if url in cache:
        try:
            ts = datetime.fromisoformat(cache[url])
            if datetime.utcnow() < ts + timedelta(minutes=COOLDOWN_MINUTES):
                print(f"Skipping {url} — within 202 cooldown window.")
                return True
        except ValueError:
            print(f"Invalid timestamp in cache for {url}, ignoring.")
    return False


def update_202_cache(url):
    cache = load_202_cache()
    cache[url] = datetime.utcnow().isoformat()
    save_202_cache(cache)


def get_headers():
    return {"User-Agent": random.choice(user_agents)}


def jittered_delay(base=2.0, variance=0.5):
    time.sleep(random.uniform(base - variance, base + variance))


def fetch_with_retries(url, max_retries=5, delay=2):
    if should_skip_url(url):
        return None

    for attempt in range(max_retries):
        try:
            print(f"[{attempt+1}] Fetching: {url}", flush=True)
            response = requests.get(url, headers=get_headers(), timeout=10)

            if response.status_code == 200:
                print(f"[{attempt+1}] Success (200): {url}", flush=True)
                return response

            elif response.status_code == 202:
                print(f"[{attempt+1}] 202 Accepted: {url}", flush=True)
                update_202_cache(url)
                print(f"URL {url} added to cooldown cache. Skipping retries.", flush=True)
                return None  # Do not retry further

            elif response.status_code in {429, 503}:
                print(f"[{attempt+1}] Status {response.status_code} for {url} — retrying...", flush=True)
                if "Retry-After" in response.headers:
                    retry_after = int(response.headers["Retry-After"])
                    print(f"Retry-After: {retry_after} seconds", flush=True)
                    time.sleep(retry_after)
                else:
                    jittered_delay(base=delay, variance=1.0)

            elif response.status_code in {400, 401, 403, 404}:
                print(f"[{attempt+1}] Fast-fail ({response.status_code}) for {url}", flush=True)
                return None

            else:
                print(f"[{attempt+1}] Unhandled status {response.status_code} for {url}", flush=True)
                return None

        except requests.RequestException as e:
            print(f"[{attempt+1}] Request error: {e} for {url}", flush=True)
            jittered_delay(base=delay, variance=1.0)

    print(f"Failed to fetch {url} after {max_retries} retries.", flush=True)
    return None



def fetch_entry_pages(case_url):
    print(f"\n--- Fetching pages for case: {case_url} ---", flush=True)

    base_url = case_url
    asc_url = f"{case_url}?order_by=asc"
    desc_url = f"{case_url}?order_by=desc"

    print(f"Fetching base page: {base_url}", flush=True)
    base_resp = fetch_with_retries(base_url)

    print(f"Fetching ascending entry page: {asc_url}", flush=True)
    asc_resp = fetch_with_retries(asc_url)

    print(f"Fetching descending entry page: {desc_url}", flush=True)
    desc_resp = fetch_with_retries(desc_url)

    return base_resp, asc_resp, desc_resp
