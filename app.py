import streamlit as st
from pdf_to_csv.converter import extract_tables_from_pdf
import pandas as pd

st.title("📄 PDF to CSV Extractor")

uploaded_pdf = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_pdf:
    tables = extract_tables_from_pdf(uploaded_pdf)

    if tables:
        table_names = [name for name, df in tables]
        selected_table = st.selectbox("Select a table", table_names)
        df = dict(tables)[selected_table]
        st.dataframe(df)

        if st.button("Download CSV"):
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "selected_table.csv", "text/csv")
    else:
        st.warning("No tables found in the PDF.")