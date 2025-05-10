# scraper/fetch.py
import time
import random
import requests

session = requests.Session()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)",
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
]


def get_headers():
    return {"User-Agent": random.choice(user_agents)}


def jittered_delay(base=2.0, variance=0.5):
    time.sleep(random.uniform(base - variance, base + variance))


def fetch_ready_page(url, session=session, headers=None, max_retries=5, delay=5):
    headers = headers or get_headers()
    fast_fail_statuses = {400, 401, 403, 404}

    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response

            elif response.status_code in fast_fail_statuses:
                print(f"Attempt {attempt + 1}: Status {response.status_code} - Not retrying.")
                return None

            elif response.status_code in {202, 429, 503}:
                print(f"Attempt {attempt + 1}: Status {response.status_code}, retrying...")

                if response.status_code == 429 and "Retry-After" in response.headers:
                    retry_after = int(response.headers["Retry-After"])
                    print(f"Retry-After header present. Waiting {retry_after} seconds.")
                    time.sleep(retry_after)
                else:
                    jittered_delay(base=delay, variance=0.5)

            else:
                print(f"Attempt {attempt + 1}: Unhandled status {response.status_code}, not retrying.")
                break

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}: Error fetching {url} - {e}, retrying...")
            jittered_delay(base=delay, variance=0.5)

    print(f"Failed to fetch {url} after {max_retries} attempts.")
    return None


def fetch_first_entry_page(case_url, session=session):
    asc_url = f"{case_url}?order_by=asc"
    return fetch_ready_page(asc_url, session=session)


def fetch_latest_entry_page(case_url, session=session):
    desc_url = f"{case_url}?order_by=desc"
    return fetch_ready_page(desc_url, session=session)
