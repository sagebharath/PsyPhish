from reputation_features import (
    get_virustotal_score,
    google_safe_browsing_flag,
    phishtank_flag
)

url = "http://secure-login-bank.tk/login"

print("VT Score:", get_virustotal_score(url))
print("GSB Flag:", google_safe_browsing_flag(url))
print("PhishTank Flag:", phishtank_flag(url))