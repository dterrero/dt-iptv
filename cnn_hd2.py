import requests

url = "https://example.com/api/endpoint"
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