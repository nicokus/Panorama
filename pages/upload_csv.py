import streamlit as st
import pandas as pd
import hashlib
import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import COLONNE_CONFIG


### INTERFACCIA GRAFICA PER CARICARE IL CSV ###
st.markdown(
    """
    <div style="border: 2px solid #333; padding: 20px; border-radius: 5px; text-align: center; background-color: #f9f9f9; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #333;">Upload CSV</h3>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "DATEV-Konformes CSV mit Umsätzen hochladen", type=["csv"]
    )


colonne_csv = [col['nome'] for col in COLONNE_CONFIG]

### TABELLA PER VEDERE ANTEPRIMA DEL CSV ###
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, header=None, sep=';', encoding='latin1', dtype=str)

    
    if df.shape[1] >= len(colonne_csv):
        df = df.iloc[:, :len(colonne_csv)]
        df.columns = colonne_csv
    
    st.write("CSV Vorschau:")
    st.dataframe(df)




    ### PULSANTE PER CONFERMARE L´UPLOAD A RAILWAY
    if st.button("Bestätigen und Hochladen"):
        try:
            # Recupero della stringa di connessione dai Secrets di Streamlit
            db_url = st.secrets["DATABASE_URL"]
            
            # Connessione al database PostgreSQL su Railway
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()


            
            ### CALCOLO HASH DETERMINISTICO (unique_id)
            def calcola_hash(row):
                campi_stabili = "".join([
                    str(row.get('buchungstag', '')),
                    str(row.get('wertstellung', '')),
                    str(row.get('betrag', '')),
                    str(row.get('gegenpartei_iban', '')),
                    str(row.get('verwendungszweck_1', '')),
                    str(row.get('geschaeftsart', ''))
                ])
                return hashlib.sha256(campi_stabili.encode('utf-8')).hexdigest()
            
            df['unique_id'] = df.apply(calcola_hash, axis=1)
            
            nomi_colonne = [col["nome"] for col in COLONNE_CONFIG]
            colonne_insert_sql = ", ".join(nomi_colonne)
            placeholders_sql = ", ".join(["%s"] * len(COLONNE_CONFIG))

            insert_query = f"""
                INSERT INTO bank_transaktionen ({colonne_insert_sql})
                VALUES ({placeholders_sql})
                ON CONFLICT (unique_id) DO NOTHING;
            """

            inseriti = 0
            duplicati = 0

            for _, row in df.iterrows():
                valori = tuple(row.get(col["nome"]) for col in COLONNE_CONFIG)
                cur.execute(insert_query, valori)
                if cur.rowcount > 0:
                    inseriti += 1
                else:
                    duplicati += 1

            conn.commit()
            cur.close()
            conn.close()

            st.success(f"Caricamento completato! Record inseriti: {inseriti}, duplicati saltati: {duplicati}.")

        except Exception as e:
            st.error(f"Errore durante la connessione o l'inserimento nel database: {e}")