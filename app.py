import streamlit as st
import pandas as pd
import pdfplumber
from gspread_dataframe import set_with_dataframe
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Auto PDF → Sheet → CSV")

st.title("📄 PDF → Google Sheet → CSV Export")

uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
export_set = st.selectbox("Select Export Set", ["5 Set1", "5 Set2", "5 Set3", "5 Set4"])

if st.button("Run & Upload to Sheet") and uploaded_pdf:
    # Extract tables
    tables = []
    with pdfplumber.open(uploaded_pdf) as pdf:
        for page in pdf.pages:
            for tbl in page.extract_tables():
                df = pd.DataFrame(tbl[1:], columns=tbl[0])
                tables.append(df)

    if not tables:
        st.warning("No tables found in PDF.")
    else:
        df_merged = pd.concat(tables, ignore_index=True)  # customize merging logic

        # Connect to Google Sheets
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        gc = gspread.authorize(creds)
        ss = gc.open_by_url(st.secrets["private_gsheets_url"])

        sheet_name = f"Set_{export_set.replace(' ', '_')}"
        try:
            ws = ss.add_worksheet(title=sheet_name, rows=str(len(df_merged)+10), cols=str(len(df_merged.columns)))
        except gspread.exceptions.APIError:
            ws = ss.worksheet(sheet_name)
        
        set_with_dataframe(ws, df_merged)

        st.success(f"✅ Data uploaded to Google Sheet tab: {sheet_name}")
        st.dataframe(df_merged)

        csv_bytes = df_merged.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv_bytes, file_name=f"{sheet_name}.csv", mime="text/csv")
