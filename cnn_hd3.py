from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Wait for the first .m3u8 request that contains token, user_id, expires
    def is_m3u8_request(request):
        if ".m3u8" in request.url:
            qs = parse_qs(urlparse(request.url).query)
            return all(qs.get(k, [None])[0] for k in ["token", "user_id", "expires"])
        return False

    # Start navigation
    page.goto("https://tvpass.org/channel/cnn-us")

    # Wait for the first matching request
    request = page.wait_for_request(is_m3u8_request, timeout=10000)  # 10s timeout

    # Extract query parameters
    qs = parse_qs(urlparse(request.url).query)
    token = qs["token"][0]
    user_id = qs["user_id"][0]
    expires = qs["expires"][0]

    # Build full URL
    m3u8_url = f"https://e2.thetvapp.to/hls/CNN/tracks-v1a1/mono.m3u8?token={token}&expires={expires}&user_id={user_id}"

    # Save to file (replace if exists)
    with open("cnn_hd2.txt", "w") as f:
        f.write(m3u8_url)

    print("URL saved to cnn_hd2.txt")
    print(m3u8_url)

    browser.close()
