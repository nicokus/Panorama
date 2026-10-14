import os
import requests

api_key = os.getenv("LEXOFFICE_API_KEY")

url = "https://api.lexoffice.io/v1/voucherlist"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

params = {
    "voucherType": "salesinvoice",
    "voucherStatus": "open",
    "page": 0,
    "size": 50
}

response = requests.get(url, headers=headers, params=params)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Erfolg! Gefundene Belege: {len(data.get('content', []))}")
else:
    print(f"Fehler: {response.text}")