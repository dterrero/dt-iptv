from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    def handle_request(request):
        if ".m3u8" in request.url:
            qs = parse_qs(urlparse(request.url).query)
            token = qs.get("token", [None])[0]
            user_id = qs.get("user_id", [None])[0]
            expires = qs.get("expires", [None])[0]

            # Only print if we actually got the values
            if token and user_id and expires:
                print("token:", token)
                print("user_id:", user_id)
                print("expires:", expires)

    page.on("request", handle_request)
    page.goto("https://tvpass.org/channel/cnn-us")
    page.wait_for_timeout(5000)  # wait a few seconds for requests to fire
    browser.close()
