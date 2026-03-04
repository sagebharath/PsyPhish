from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import numpy as np
from xgboost import XGBClassifier

from url_features import extract_url_features
from crawler_features import crawl_website
from reputation_features import get_virustotal_score, google_safe_browsing_flag
from phishtank_db import check_url
from feature_pipeline import build_feature_vector

app = FastAPI()

# Load model safely
model = XGBClassifier()
model.load_model("xgb_model.json")
print("Model loaded successfully")

class URLInput(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/analyze")
def analyze(data: URLInput):
    try:
        url = data.url.strip()

        # 1️⃣ PhishTank DB override (Local check)
        if check_url(url):
            return JSONResponse({
                "risk_score": 99,
                "status": "Phishing",
                "reasons": ["PhishTank confirmed phishing (Local DB)"]
            })

        # 2️⃣ Real-time PhishTank API check (if not in local DB)
        from phishtank_api import check_phishtank_api
        from phishtank_db import insert_urls
        if check_phishtank_api(url):
            # Update the local database immediately so next time it's faster
            insert_urls([url])
            return JSONResponse({
                "risk_score": 99,
                "status": "Phishing",
                "reasons": ["PhishTank confirmed phishing (API)"]
            })

        # 3️⃣ Feature extraction
        url_f = extract_url_features(url)
        crawl_f = crawl_website(url)

        vt = float(get_virustotal_score(url))
        gsb = int(google_safe_browsing_flag(url))
        pt = 0

        features = build_feature_vector(url_f, crawl_f, vt, gsb, pt)
        X = np.array([features], dtype=float)

        prob = float(model.predict_proba(X)[0][1])
        risk = round(prob * 100, 2)

        if risk > 70:
            status = "Phishing"
        elif risk > 40:
            status = "Suspicious"
        else:
            status = "Safe"

        reasons = []
        if crawl_f["login_form_detected"]:
            reasons.append("Login form detected")
        if crawl_f["redirect_count"] > 2:
            reasons.append("Multiple redirects")
        if vt > 0.3:
            reasons.append("VirusTotal flagged")
            
        # Add heuristics based on new URL features
        if url_f["is_shortened"]:
            reasons.append("URL shortener service used")
            if risk < 50: risk += 20 # Bump risk heuristically
        if url_f["num_digits"] > 10:
            reasons.append("High number of digits in URL")
            if risk < 30: risk += 10
        if url_f["path_length"] > 50:
            reasons.append("Unusually long URL path")
        if url_f["num_parameters"] > 3:
            reasons.append("Multiple query parameters")
            
        # Ensure risk stays within 0-100 bounds
        risk = min(100.0, risk)
        if risk > 70: status = "Phishing"
        elif risk > 40: status = "Suspicious"
        else: status = "Safe"

        return JSONResponse({
            "risk_score": risk,
            "status": status,
            "reasons": reasons,
            "url_features": url_f,
            "crawl_features": crawl_f
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "risk_score": -1,
                "status": "Error",
                "reasons": [str(e)]
            }
        )