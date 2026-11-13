### GRAFICA ###
import streamlit as st
import psycopg2

st.title("Panorama")
st.write("was läuft auf Panorama")

### CONNECT TO POSTGRE-SQL SU RAILWAY ###
try:
    conn = psycopg2.connect("postgresql://postgres:foLkCkJTsFCZTqavpMefCAMCBsjgYjkO@switchyard.proxy.rlwy.net:28916/railway")
    st.success("Verbindung mit dem Database PostgreSQL auf Railway aktiv")
    conn.close()
except Exception as e:
    st.error(f"Fehler bei der Verbindung mit dem Database PostgreSQL auf Railway: {e}")