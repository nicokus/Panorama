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

uploaded_file = st.file_uploader("neues CSV hochladen", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Anteprima dei dati:")
    st.dataframe(df)