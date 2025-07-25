import streamlit as st
from pdf_to_csv import converter

st.set_page_config(page_title="PDF to CSV Converter", layout="centered")
st.title("📄➡️📊 PDF to CSV Converter")

uploaded_file = st.file_uploader("Upload your Excel macro file (.xlsm)", type=["xlsm"])

if uploaded_file:
    st.success("File uploaded successfully!")
    with open("uploaded.xlsm", "wb") as f:
        f.write(uploaded_file.read())

    output_path = "output.csv"
    success, message = converter.convert_excel_to_csv("uploaded.xlsm", output_path)

    if success:
        st.download_button("Download CSV", data=open(output_path, "rb"), file_name="output.csv", mime="text/csv")
    else:
        st.error(f"Conversion failed: {message}")