
import streamlit as st
from core.converter import process_pdf

st.set_page_config(page_title="Auto PDF to CSV", layout="centered")

st.title("📄 Auto PDF → Excel → CSV Export")
st.write("Upload your PDF, choose a set, and auto-export CSV using Excel macro logic.")

pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
export_set = st.selectbox("Select Export Set", ["5 Set1", "5 Set2", "5 Set3", "5 Set4"])
run = st.button("▶ Run & Export CSV")

if run and pdf_file:
    with st.spinner("Processing..."):
        result_paths = process_pdf(pdf_file, export_set)
    st.success("CSV export completed!")
    for path in result_paths:
        st.download_button(f"Download {Path(path).name}", open(path, "rb").read(), file_name=Path(path).name)
