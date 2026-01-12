from urllib.parse import urlparse, parse_qs

url = "https://tvpass.org/channel/cnn-us"

qs = parse_qs(urlparse(url).query)

print(qs["token"][0])
print(qs["user_id"][0])
print(qs["expires"][0])
