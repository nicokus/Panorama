import os
import requests
import json

# API-Key aus den GitHub Secrets / Umgebungsvariablen laden
api_key = os.environ.get("LEXOFFICE_API_KEY")

# Abbruch, falls kein Schlüssel hinterlegt wurde
if not api_key:
    raise ValueError("API-Key nicht gefunden.")

# Ziel-URL für den Abruf von Zahlungen / Payments definieren
url = "https://api.lexoffice.io/v1/payments"

# Header für die Authentifizierung und das erwartete Format (JSON) setzen
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

# Anfrage an den Lexoffice-Server senden
response = requests.get(url, headers=headers)

# Prüfen, ob die Verbindung erfolgreich war (Status 200)
if response.status_code == 200:
    # Antwortdaten als JSON-Struktur einlesen
    data = response.json()
    
    # Überprüfen, ob Zahlungen vorhanden sind, und den ersten Datensatz verarbeiten
    if data.get('content'):
        erster_datensatz = data['content'][0]
else:
    # Bei einem Fehler den Statuscode und die Fehlermeldung verarbeiten
    pass