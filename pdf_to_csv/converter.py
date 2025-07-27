import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_file):
    all_tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append((f"Page {i+1} Table", df))
    return all_tables