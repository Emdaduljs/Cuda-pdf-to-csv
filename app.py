import streamlit as st
import pandas as pd
from pdf_to_csv.converter import extract_tables_from_pdf

st.set_page_config(page_title="PDF to CSV + OCR", layout="wide")
st.title("📄 PDF Table + OCR CSV Extractor")

uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_pdf:
    with st.spinner("Processing..."):
        tables = extract_tables_from_pdf(uploaded_pdf)

    if tables:
        tabs = st.tabs([f"Table {i+1}" for i in range(len(tables))])
        for i, tab in enumerate(tabs):
            with tab:
                df = tables[i]
                edited_df = st.data_editor(df, use_container_width=True)
                csv = edited_df.to_csv(index=False).encode("utf-8")
                st.download_button(f"Download Table {i+1} as CSV", csv,
                                   file_name=f"table_{i+1}.csv", mime="text/csv")
    else:
        st.warning("No tables found—even via OCR. Try a higher-resolution PDF or image.")
