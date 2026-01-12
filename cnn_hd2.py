import requests
from urllib.parse import urlparse, parse_qs

url = "https://tvpass.org/channel/cnn-us"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://tvpass.org/",
}

r = requests.get(url, headers=headers)

# Extract query parameters
qs = parse_qs(urlparse(r.url).query)

print("token:", qs.get("token"))
print("user_id:", qs.get("user_id"))
print("expires:", qs.get("expires"))

