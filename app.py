import streamlit as st
from pdf_to_csv.converter import extract_tables_from_pdf
import pandas as pd

st.set_page_config(page_title="PDF to CSV", layout="wide")
st.title("📄 PDF Table Extractor")

uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_pdf:
    with st.spinner("Extracting tables..."):
        tables = extract_tables_from_pdf(uploaded_pdf)

    if tables:
        tabs = st.tabs([f"Table {i+1}" for i in range(len(tables))])
        for i, tab in enumerate(tabs):
            with tab:
                df = tables[i]
                edited_df = st.data_editor(df, use_container_width=True)
                csv = edited_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    f"Download Table {i+1} as CSV",
                    csv,
                    file_name=f"table_{i+1}.csv",
                    mime="text/csv"
                )
    else:
        st.warning("⚠️ No tables were found in the PDF. Try a different file or scanned version.")
