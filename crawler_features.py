from playwright.sync_api import sync_playwright

def crawl_website(url):
    data = {
        "redirect_count": 0,
        "login_form_detected": 0,
        "external_links": 0,
        "suspicious_scripts": 0,
        "iframes_detected": 0,
        "unreachable": 0
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=8000)

            data["login_form_detected"] = int(page.locator("input[type='password']").count() > 0)
            data["external_links"] = page.locator("a[href^='http']").count()
            data["iframes_detected"] = page.locator("iframe").count()

            browser.close()
    except:
        data["unreachable"] = 1

    return data