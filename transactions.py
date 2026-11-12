import os
import requests
import pandas as pd

api_key = os.getenv("LEXOFFICE_API_KEY")

url = "https://api.lexoffice.io/v1/transactions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

all_transactions = []
page = 0

while True:
    params = {"page": page, "size": 50}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Fehler bei Anfrage: {response.status_code} - {response.text}")
        break
        
    data = response.json()
    transactions = data.get('content', []) if isinstance(data, dict) else data
    
    if not transactions:
        break
        
    for tx in transactions:
        booking_date = tx.get("bookingDate", "")
        if booking_date.startswith("2026-10"):
            all_transactions.append({
                "Transaktions-ID": tx.get("id", ""),
                "Buchungsdatum": booking_date,
                "Betrag": tx.get("amount", ""),
                "Währung": tx.get("currency", "EUR"),
                "Verwendungszweck": tx.get("remittanceInformation", ""),
                "Typ": tx.get("type", "")
            })
            
    # Prüfen ob es weitere Seiten gibt
    if isinstance(data, dict) and data.get("last", True):
        break
    page += 1
    if page > 10: # Sicherheitsabbruch
        break

df = pd.DataFrame(all_transactions)

if not df.empty:
    df.to_excel("transaktionen_oktober_2026.xlsx", index=False)
    print(f"Erfolgreich gespeichert! {len(df)} Transaktionen gefunden.")
    print(df)
else:
    print("Keine Transaktionen für Oktober 2026 gefunden.").