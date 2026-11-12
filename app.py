### GRAFICA ###
import streamlit as st
import psycopg2

st.title("Panorama")
st.write("Panorama läuft xfun")

### CONNECT TO POSTGRE-SQL ###
try:
    conn = psycopg2.connect(
        dbname="lexoffice_db",
        user="postgres",
        password="secretpassword",
        host="localhost",
        port="5432"
    )
    st.success("Connessione al database PostgreSQL riuscita!")
    conn.close()
except Exception as e:
    st.error(f"Errore di connessione: {e}")