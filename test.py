import os
import requests
import json

api_key = os.getenv("LEXOFFICE_API_KEY")
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
beleg_id = "b73e2e8b-fd85-4220-baec-8808c511f7c8"

# Korrekturm: Da es ein "voucher" ist, nutzen wir den Vouchers-Endpoint
url = f"https://api.lexoffice.io/v1/vouchers/{beleg_id}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    details = response.json()
    print(json.dumps(details, indent=2, ensure_ascii=False))
else:
    print(f"Fehler: {response.status_code} - {response.text}")