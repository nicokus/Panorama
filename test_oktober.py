import os
import requests
import pandas as pd

api_key = os.getenv("LEXOFFICE_API_KEY")

url = "https://api.lexoffice.io/v1/voucherlist"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

types_to_fetch = ["salesinvoice", "purchaseinvoice", "voucher"]
all_items = []

for v_type in types_to_fetch:
    params = {
        "voucherType": v_type,
        "voucherStatus": "paid",
        "page": 0,
        "size": 50
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for item in data.get('content', []):
            beleg_datum = item.get("voucherDate", "")
            
            if beleg_datum.startswith("2026-10"):
                all_items.append({
                    "Typ": v_type,
                    "Belegnummer": item.get("voucherNumber", ""),
                    "Belegdatum": beleg_datum,
                    "Kontakt": item.get("contactName", ""),
                    "Betrag": item.get("totalAmount", ""),
                    "Währung": item.get("currency", "EUR")
                })

df = pd.DataFrame(all_items)

if not df.empty:
    df.to_excel("belege_oktober_2026.xlsx", index=False)
    print("Erfolgreich gespeichert!")
    print(df)
else:
    print("Keine Belege für Oktober 2026 gefunden.")