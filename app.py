import streamlit as st
import pandas as pd
import tabula  # requires Java installed
import os
from io import BytesIO

st.set_page_config(page_title="PDF to CSV Converter", layout="centered")

st.title("PDF to CSV Exporter")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

export_options = ["Set 1", "Set 2", "Set 3", "Set 4", "Set 5"]
selected_set = st.selectbox("Select Export Set", export_options)

if st.button("Run & Export CSV"):
    if uploaded_file is not None:
        # Save the uploaded PDF temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        # Extract tables using Tabula (Java-based)
        try:
            dfs = tabula.read_pdf("temp.pdf", pages='all', multiple_tables=True)
            # Simulate picking specific export set logic
            if dfs:
                df = dfs[0] if selected_set == "Set 1" else dfs[min(1, len(dfs)-1)]
                st.success("Data extracted:")
                st.dataframe(df)

                # Prepare download link
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="converted.csv",
                    mime="text/csv"
                )
            else:
                st.error("No tables found in PDF.")
        except Exception as e:
            st.error(f"Failed to extract tables. Error: {str(e)}")

        os.remove("temp.pdf")
    else:
        st.warning("Please upload a PDF file.")
