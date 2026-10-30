import requests
resp = requests.get("https://api.xposedornot.com/v1/check-email/test@example.com")
print(resp.status_code)
print(resp.json())