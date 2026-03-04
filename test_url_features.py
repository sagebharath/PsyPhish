from url_features import extract_url_features

url = "http://secure-login-bank.tk/login"
features = extract_url_features(url)

for k, v in features.items():
    print(f"{k}: {v}")