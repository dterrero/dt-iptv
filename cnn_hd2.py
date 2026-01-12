import requests

url = "https://tvpass.org/channel/cnn-us"
params = {
    "token": "...",
    "user_id": "...",
    "expires": "..."
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Authorization": "Bearer YOUR_TOKEN"
}

r = requests.get(url, params=params, headers=headers)
print(r.text)
