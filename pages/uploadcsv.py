import streamlit as st
import pandas as pd

st.title("Upload CSV")

uploaded_file = st.file_uploader("Carica il tuo file CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Anteprima dei dati:")
    st.dataframe(df)