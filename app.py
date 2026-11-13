### GRAFICA ###
import streamlit as st
import psycopg2

st.title("Panorama")
st.write("Panorama läuft xfun")

### CONNECT TO POSTGRE-SQL SU RAILWAY ###
try:
    conn = psycopg2.connect("postgresql://postgres:foLkCkJTsFCZTqavpMefCAMCBsjgYjkO@switchyard.proxy.rlwy.net:28916/railway")
    st.success("Connessione al database PostgreSQL su Railway riuscita!")
    conn.close()
except Exception as e:
    st.error(f"Errore di connessione: {e}")