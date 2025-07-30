import streamlit as st
from converter import extract_tables
import pandas as pd

st.title("📄 PDF Table Extractor")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])
option = st.selectbox("Select Export Set", ["Set1", "Set2", "Set3", "Set4"])
if st.button("Run & Export CSV") and uploaded:
    dfs = extract_tables(uploaded)
    if dfs:
        df = dfs[0]  # choose default or map based on option
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "output.csv", "text/csv")
    else:
        st.warning("No tables found.")
