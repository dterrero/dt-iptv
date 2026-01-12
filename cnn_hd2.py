from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://tvpass.org/channel/cnn-us")

    # Wait for the .m3u8 request to appear
    def handle_request(request):
        if ".m3u8" in request.url:
            qs = parse_qs(urlparse(request.url).query)
            print("token:", qs.get("token", [None])[0])
            print("user_id:", qs.get("user_id", [None])[0])
            print("expires:", qs.get("expires", [None])[0])

    page.on("request", handle_request)

    # Let page load for a few seconds
    page.wait_for_timeout(5000)
    browser.close()
