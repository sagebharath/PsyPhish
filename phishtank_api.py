import requests

PHISHTANK_API = "http://checkurl.phishtank.com/checkurl/"

def check_phishtank_api(url):
    try:
        r = requests.post(
            PHISHTANK_API,
            data={"url": url, "format": "json"},
            timeout=10
        )
        res = r.json()["results"]
        return int(res.get("in_database") and res.get("verified"))
    except:
        return 0