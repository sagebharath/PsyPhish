from feature_pipeline import build_feature_vector
from url_features import extract_url_features
from crawler_features import crawl_website
from reputation_features import get_virustotal_score, google_safe_browsing_flag

url = "https://quantasey.com/tsgindcz/"

url_f = extract_url_features(url)
crawl_f = crawl_website(url)
vt = get_virustotal_score(url)
gsb = google_safe_browsing_flag(url)
pt = 0

features = build_feature_vector(url_f, crawl_f, vt, gsb, pt)

print("Feature Vector:")
print(features)