import os
import requests
import pandas as pd

api_key = os.getenv("LEXOFFICE_API_KEY")

if not api_key:
    print("Fehler: Das Secret LEXOFFICE_API_KEY wurde nicht gefunden!")
    exit()

url = "https://api.lexoffice.io/v1/voucherlist"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

params = {
    "voucherType": "salesinvoice",
    "voucherStatus": "paid",
    "page": 0,
    "size": 50
}

try:
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('content', [])
        
        extracted_data = []
        for item in items:
            extracted_data.append({
                "Belegnummer": item.get("voucherNumber", ""),
                "Belegdatum": item.get("voucherDate", ""),
                "Kunde / Kontakt": item.get("contactName", ""),
                "Betrag": item.get("totalAmount", ""),
                "Währung": item.get("currency", "EUR")
            })
            
        df = pd.DataFrame(extracted_data)
        
        # Als CSV und Excel speichern
        df.to_csv("bezahlte_rechnungen.csv", index=False, encoding="utf-8-sig")
        df.to_excel("bezahlte_rechnungen.xlsx", index=False)
        
        print("Erfolgreich gespeichert!")
        print("\nÜbersicht der bezahlten Rechnungen:")
        print(df)
    else:
        print(f"Fehler bei der Abfrage: {response.status_code} - {response.text}")

except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")