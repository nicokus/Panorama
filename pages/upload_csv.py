import streamlit as st
import pandas as pd

st.markdown(
    """
    <div style="border: 2px solid #333; padding: 20px; border-radius: 5px; text-align: center; background-color: #f9f9f9; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #333;">Upload CSV</h3>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("DATEV-Konformes CSV mit Umsätzen hochladen", type=["csv"])

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
    
    st.write("Anteprima dei dati adattati:")
    st.dataframe(df)