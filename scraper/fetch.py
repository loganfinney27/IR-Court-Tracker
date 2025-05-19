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

cached_202 = set()  # optionally persisted later

def get_headers():
    return {"User-Agent": random.choice(user_agents)}

def jittered_delay(base=2.0, variance=0.5):
    time.sleep(random.uniform(base - variance, base + variance))

def fetch_entry_page(case_url, order="asc", session=session, max_retries=5, delay=2):
    url = f"{case_url}?order_by={order}"
    if url in cached_202:
        print(f"Skipping cached 202: {url}")
        return None

    headers = get_headers()
    fast_fail = {400, 401, 403, 404}

    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response

            elif response.status_code in fast_fail:
                print(f"[{order}] {url} -> {response.status_code} (fast-fail)")
                return None

            elif response.status_code == 202:
                print(f"[{order}] {url} -> 202 (not ready), attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    cached_202.add(url)
                jittered_delay(base=delay, variance=0.5)

            elif response.status_code == 429 and "Retry-After" in response.headers:
                wait = int(response.headers["Retry-After"])
                print(f"[{order}] {url} -> 429, waiting {wait}s")
                time.sleep(wait)

            elif response.status_code == 503:
                print(f"[{order}] {url} -> 503, retrying...")
                jittered_delay(base=delay, variance=0.5)

            else:
                print(f"[{order}] {url} -> {response.status_code}, unhandled.")
                break

        except requests.RequestException as e:
            print(f"[{order}] {url} -> error: {e}")
            jittered_delay(base=delay, variance=0.5)

    print(f"[{order}] {url} failed after {max_retries} attempts.")
    return None

def fetch_first_entry_page(case_url):
    return fetch_entry_page(case_url, order="asc")

def fetch_latest_entry_page(case_url):
    return fetch_entry_page(case_url, order="desc")
