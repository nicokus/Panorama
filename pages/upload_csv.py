import streamlit as st
import pandas as pd
import hashlib
import psycopg2
import os



### INTERFACCIA GRAFICA PER CARICARE IL CSV ###
st.markdown(
    """
    <div style="border: 2px solid #333; padding: 20px; border-radius: 5px; text-align: center; background-color: #f9f9f9; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #333;">Upload CSV</h3>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("DATEV-Konformes CSV mit Umsätzen hochladen", type=["csv"])




### TABELLA PER VEDERE ANTEPRIMA DEL CSV ###
if uploaded_file is not None:
    # I file bancari senza intestazioni usano solitamente il punto e virgola come separatore e codifiche standard
    df = pd.read_csv(uploaded_file, header=None, sep=';', encoding='latin1', dtype=str)
    
    # Assegnazione dei nomi delle colonne dalla A alla AH
    colonne_csv = [
        "bic_auftraggeber", "iban_auftraggeber", "reserviert_c", "reserviert_d",
        "buchungstag", "wertstellung", "betrag", "gegenpartei_name",
        "reserviert_i", "reserviert_j", "gegenpartei_iban",
        "verwendungszweck_1", "verwendungszweck_2", "verwendungszweck_3",
        "verwendungszweck_4", "verwendungszweck_5", "waehrung",
        "geschaeftsart", "zuordnungsstatus", "extra_t", "extra_u",
        "extra_v", "extra_w", "extra_x", "extra_y", "extra_z",
        "extra_aa", "extra_ab", "extra_ac", "extra_ad", "extra_ae",
        "extra_af", "extra_ag", "extra_ah"
    ]
    
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


            
            ### CALCOLO HASH DETERMINISTICO (codice_univoco)
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
            
            df['codice_univoco'] = df.apply(calcola_hash, axis=1)
            
            inseriti = 0
            duplicati = 0

            for _, row in df.iterrows():
                # Gestione duplicati tramite ON CONFLICT (codice_univoco) DO NOTHING nella query SQL
                if cur.rowcount > 0:
                    inseriti += 1
                else:
                    duplicati += 1

            
            
            
            
            
            # Iterazione e inserimento riga per riga con clausola ON CONFLICT DO NOTHING
            for _, row in df.iterrows():
                query = """
                    INSERT INTO bank_transaktionen (
                        codice_univoco, bic_auftraggeber, iban_auftraggeber, reserviert_c, reserviert_d,
                        buchungstag, wertstellung, betrag, gegenpartei_name,
                        reserviert_i, reserviert_j, gegenpartei_iban,
                        verwendungszweck_1,wendungszweck_2, verwendungszweck_3,
                        verwendungszweck_4, verwendungszweck_5, waehrung,
                        geschaeftsart, zuordnungsstatus, extra_t, extra_u,
                        extra_v, extra_w, extra_x, extra_y, extra_z,
                        extra_aa, extra_ab, extra_ac, extra_ad, extra_ae,
                        extra_af, extra_ag, extra_ah
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (codice_univoco) DO NOTHING;
                """
                
                valori = (
                    row['codice_univoco'], row['bic_auftraggeber'], row['iban_auftraggeber'], row['reserviert_c'], row['reserviert_d'],
                    row['buchungstag'], row['wertstellung'], row['betrag'], row['gegenpartei_name'],
                    row['reserviert_i'], row['reserviert_j'], row['gegenpartei_iban'],
                    row['verwendungszweck_1'], row['verwendungszweck_2'], row['verwendungszweck_3'],
                    row['verwendungszweck_4'], row['verwendungszweck_5'], row['waehrung'],
                    row['geschaeftsart'], row['zuordnungsstatus'], row['extra_t'], row['extra_u'],
                    row['extra_v'], row['extra_w'], row['extra_x'], row['extra_y'], row['extra_z'],
                    row['extra_aa'], row['extra_ab'], row['extra_ac'], row['extra_ad'], row['extra_ae'],
                    row['extra_af'], row['extra_ag'], row['extra_ah']
                )
                
                cur.execute(query, valori)
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




### 




