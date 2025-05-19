# scraper/fetch.py
import time
import random
import requests

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
]

def get_headers():
    return {"User-Agent": random.choice(user_agents)}

def jittered_delay(base=2.0, variance=0.5):
    time.sleep(random.uniform(base - variance, base + variance))

def fetch_with_retries(url, max_retries=5, delay=2):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=get_headers(), timeout=10)

            if response.status_code == 200:
                return response

            elif response.status_code == 202:
                print(f"[{attempt+1}] 202 Accepted for {url} — retrying...")
                jittered_delay(base=delay, variance=1.0)

            elif response.status_code in {429, 503}:
                print(f"[{attempt+1}] Status {response.status_code} for {url} — retrying...")
                if "Retry-After" in response.headers:
                    retry_after = int(response.headers["Retry-After"])
                    print(f"Retry-After: {retry_after} seconds")
                    time.sleep(retry_after)
                else:
                    jittered_delay(base=delay, variance=1.0)

            elif response.status_code in {400, 401, 403, 404}:
                print(f"Fast-fail for status {response.status_code} on {url}")
                return None

            else:
                print(f"Unhandled status {response.status_code} for {url}")
                return None

        except requests.RequestException as e:
            print(f"[{attempt+1}] Request error: {e} for {url}")
            jittered_delay(base=delay, variance=1.0)

    print(f"Failed to fetch {url} after {max_retries} retries.")
    return None

def fetch_entry_pages(case_url):
    base_resp = fetch_with_retries(case_url)
    asc_resp = fetch_with_retries(f"{case_url}?order_by=asc")
    desc_resp = fetch_with_retries(f"{case_url}?order_by=desc")
    return base_resp, asc_resp, desc_resp
