import re
from urllib.parse import urlparse

SUSPICIOUS_TLDS = [".tk", ".ml", ".ga", ".cf"]
SHORTENER_DOMAINS = ["bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "t.co", "is.gd", "buff.ly", "adf.ly", "bit.do", "cutt.ly"]

def extract_url_features(url):
    p = urlparse(url)
    domain = p.netloc

    return {
        "url_length": len(url),
        "dot_count": url.count("."),
        "has_at": int("@" in url),
        "uses_https": int(p.scheme == "https"),
        "has_hyphen": int("-" in domain),
        "has_ip": int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", url))),
        "suspicious_tld": int(any(domain.endswith(t) for t in SUSPICIOUS_TLDS)),
        "subdomain_count": domain.count("."),
        
        # New features for heuristics and UI
        "path_length": len(p.path),
        "num_digits": sum(c.isdigit() for c in url),
        "num_parameters": len(p.query.split("&")) if p.query else 0,
        "is_shortened": int(any(shortener in domain for shortener in SHORTENER_DOMAINS)),
        "domain_length": len(domain)
    }