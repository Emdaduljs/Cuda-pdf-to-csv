import streamlit as st
import tempfile
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import pandas as pd

st.set_page_config(page_title="PDF to CSV (Any Type)", layout="centered")

st.title("📄 PDF to CSV Converter (Universal)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    st.success("PDF uploaded successfully.")

    export_set = st.selectbox("Select Export Set", ["Set 1", "Set 2", "Set 3"])
    run = st.button("🔄 Run & Export CSV")

    if run:
        st.info("Processing PDF...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        doc = fitz.open(pdf_path)
        text_data = []

        for i, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                text_data.append({"Page": i + 1, "Text": text.strip()})
            else:
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_text = pytesseract.image_to_string(img)
                text_data.append({"Page": i + 1, "Text": ocr_text.strip()})

        df = pd.DataFrame(text_data)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "converted_data.csv", "text/csv")
