import requests
import gzip
import json
import time
from io import BytesIO
from phishtank_db import init_db, insert_urls

PHISHTANK_FEED = "https://data.phishtank.com/data/online-valid.json.gz"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (PhishingDetector-Research)"
}

init_db()

while True:
    print("Updating PhishTank DB...")

    try:
        r = requests.get(PHISHTANK_FEED, headers=HEADERS, timeout=60)

        if r.status_code != 200:
            print("HTTP error:", r.status_code)
            time.sleep(3600)
            continue

        # Decompress GZIP
        with gzip.GzipFile(fileobj=BytesIO(r.content)) as f:
            data = json.loads(f.read().decode("utf-8"))

        urls = [entry["url"] for entry in data]
        insert_urls(urls)

        print(f"Stored {len(urls)} phishing URLs")

    except Exception as e:
        print("Update failed:", e)

    time.sleep(3600)  # update every hour