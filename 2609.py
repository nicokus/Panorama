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
            
            if beleg_datum.startswith("2026-09"):
                all_items.append({
                    "ID": item.get("id", ""),
                "Typ": item.get("voucherType", ""),
                "Belegnummer": item.get("voucherNumber", ""),
                "Belegdatum": item.get("voucherDate", ""),
                "DeadLine": item.get("dueDate", ""),
                "Kontakt-ID": item.get("contactId", ""),
                "Kontakt Name": item.get("contactName", ""),
                "Belegstatus": item.get("voucherStatus", ""),
                "Betrag (Brutto)": item.get("totalAmount", ""),
                "Betrag (Netto)": item.get("totalNetAmount", ""),
                "Steuerbetrag": item.get("totalTaxAmount", ""),
                "Währung": item.get("currency", "EUR"),
                "Erstellungsdatum": item.get("createdDate", ""),
                "Aktualisiert am": item.get("updatedDate", "")
                })

df = pd.DataFrame(all_items)

if not df.empty:
    df.to_excel("belege_september_2026.xlsx", index=False)
    print("Erfolgreich gespeichert!")
    print(df)
else:
    print("Keine Belege für September 2026 gefunden.")