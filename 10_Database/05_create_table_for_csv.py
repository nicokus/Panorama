import psycopg2

DATABASE_URL = "postgresql://postgres:foLkCkJTsFCZTqavpMefCAMCBsjgYjkO@switchyard.proxy.rlwy.net:28916/railway"

create_table_query = """
CREATE TABLE IF NOT EXISTS bank_transaktionen (
    bic_auftraggeber TEXT,
    iban_auftraggeber TEXT,
    reserviert_c TEXT,
    reserviert_d TEXT,
    buchungstag DATE,
    wertstellung DATE,
    betrag NUMERIC(12, 2),
    gegenpartei_name TEXT,
    reserviert_i TEXT,
    reserviert_j TEXT,
    gegenpartei_iban TEXT,
    verwendungszweck_1 TEXT,
    verwendungszweck_2 TEXT,
    verwendungszweck_3 TEXT,
    verwendungszweck_4 TEXT,
    verwendungszweck_5 TEXT,
    waehrung TEXT,
    geschaeftsart TEXT,
    zuordnungsstatus TEXT,
    extra_t TEXT,
    extra_u TEXT,
    extra_v TEXT,
    extra_w TEXT,
    extra_x TEXT,
    extra_y TEXT,
    extra_z TEXT,
    extra_aa TEXT,
    extra_ab TEXT,
    extra_ac TEXT,
    extra_ad TEXT,
    extra_ae TEXT,
    extra_af TEXT,
    extra_ag TEXT,
    extra_ah TEXT,
    id_riga SERIAL PRIMARY KEY,
    codice_univoco VARCHAR(64) UNIQUE NOT NULL,
    dateiname TEXT,
    import_zeitstempel TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lade_strategie VARCHAR(20) DEFAULT 'skip',
    bearbeitungs_status TEXT
);

CREATE INDEX IF NOT EXISTS idx_codice_univoco ON bank_transaktionen(codice_univoco);
"""

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()
    print("Tabella 'bank_transaktionen' e indice creati con successo su Railway!")
except Exception as e:
    print(f"Errore durante la creazione della tabella: {e}")
    