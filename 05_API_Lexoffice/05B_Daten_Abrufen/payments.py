import os
import requests
import json
import pandas as pd
import psycopg2

#####↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓#####
# 1. Excel-Konfiguration einlesen
df = pd.read_excel("../../25_Manual_Input_xlsx/manuelle_steuerung.xlsx", sheet_name="Variable")
config = dict(zip(df['Parameter'], df['Wert']))

# 2. Verbindung zur PostgreSQL-Datenbank herstellen
connection = psycopg2.connect(
    dbname=config.get('db_name'),
    user=config.get('db_user'),
    password=config.get('db_password'),
    host=config.get('db_host'),
    port=config.get('db_port')
)
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments_data (
        id SERIAL PRIMARY KEY,
        data JSONB
    );
""")
connection.commit()
#####↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#####

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

    #####↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓##### 
    # Überprüfen, ob Zahlungen vorhanden sind
    if data.get('content'):
        for datensatz in data['content']:
            # In PostgreSQL schreiben (Beispiel-Tabelle: payments_data mit JSONB-Spalte)
            cursor.execute(
                "INSERT INTO payments_data (data) VALUES (%s);",
                [json.dumps(datensatz)]
            )
        connection.commit()
else:
    # Bei einem Fehler den Statuscode und die Fehlermeldung verarbeiten
    pass

cursor.close()
connection.close()