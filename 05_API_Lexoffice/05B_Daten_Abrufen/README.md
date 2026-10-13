# Lexoffice API Integration

Modulare Python-Skripte zum automatisierten Abruf von Finanzdaten über die offizielle Lexoffice API.

## Struktur

- `invoices.py`: Ruft Ausgangsrechnungen ab.
es ist der tatsächliche UND erwarteter GELDEINGANG

- `vouchers.py`: Ruft Belege und Ausgaben ab.
es ist der tatsächliche UND erwarteter GELDAUSGANG

- `payments.py`: Ruft Zahlungsinformationen und Transaktionen ab.
es sind NUR tatsächliche BANKTRANSATIONEN (IN+OUT )


## Voraussetzungen
- Umgebungsvariable `LEXOFFICE_API_KEY` muss gesetzt sein.

## OUTPUT:
Datenset wird in SQL gespeichert