from urllib.parse import urlparse

def detect_phishing(url):
  score = 0

  if len(url)>75:
    score += 1

  if '@' in url:
    score += 1
  
  if not url.startswith("https://"):
    score += 1
  
  domain = urlparse(url).netloc

  if '-' in domain:
    score += 1

  return score

url = input("Enter a URL: ")
risk_score = detect_phishing(url)

print("\n--- Phishing Detection Report ---")
print("URL:", url)
print("Risk Score:", risk_score)

if risk_score >= 3:
  print("High Risk: Phishing detected")
else:
  print("Legitimate Website.")