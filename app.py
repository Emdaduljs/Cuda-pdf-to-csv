import streamlit as st
from pdf_to_csv.converter import extract_tables_tabula
import pandas as pd

st.set_page_config(page_title="PDF to CSV", layout="wide")
st.title("📄 PDF to Excel-like CSV Tool")

uploaded_pdf = st.file_uploader("Upload PDF with Tables", type="pdf")

if uploaded_pdf:
    with st.spinner("Extracting tables..."):
        tables = extract_tables_tabula(uploaded_pdf)

    if tables:
        tabs = st.tabs([f"Table {i+1}" for i in range(len(tables))])
        for i, tab in enumerate(tabs):
            with tab:
                st.subheader(f"Table {i+1}")
                df = tables[i]
                edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

                csv = edited_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"⬇️ Download Table {i+1} as CSV",
                    data=csv,
                    file_name=f"table_{i+1}.csv",
                    mime="text/csv"
                )
    else:
        st.warning("No tables were found in the PDF.")
