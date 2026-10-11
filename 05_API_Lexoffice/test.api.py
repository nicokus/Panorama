import os
import requests
import json

# Trage hier deinen Lexoffice API-Key ein oder speichere ihn als Umgebungsvariable
API_KEY = "DEIN_LEXOFFICE_API_KEY"

url = "https://api.lexoffice.io/v1/invoices"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

def test_lexoffice_connection():
    print("Verbinde mit Lexoffice API...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Erfolgreich verbunden! Anzahl abgerufener Rechnungen: {len(data.get('content', []))}\n")
        
        # Zeige die Struktur des ersten Datensatzes als Beispiel
        if data.get('content'):
            print("Beispiel-Datenstruktur des ersten Datensatzes:")
            print(json.dumps(data['content'][0], indent=4, ensure_ascii=False))
        else:
            print("Keine Rechnungen im Account gefunden.")
    else:
        print(f"Fehler bei der Verbindung: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_lexoffice_connection()