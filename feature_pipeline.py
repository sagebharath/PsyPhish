def build_feature_vector(url, crawl, vt, gsb, pt):
    return [
        url["url_length"],
        url["dot_count"],
        url["has_at"],
        url["uses_https"],
        url["has_hyphen"],
        url["has_ip"],
        url["suspicious_tld"],

        crawl["redirect_count"],
        crawl["login_form_detected"],
        crawl["external_links"],
        crawl["suspicious_scripts"],
        crawl["iframes_detected"],
        crawl["unreachable"],

        vt,
        gsb,
        pt
    ]