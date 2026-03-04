def get_virustotal_score(url):
    return 0.0  # SAFE fallback for demo

def google_safe_browsing_flag(url):
    keywords = ["login", "verify", "secure", "update"]
    return int(any(k in url.lower() for k in keywords))