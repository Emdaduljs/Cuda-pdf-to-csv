import pdfplumber
import pandas as pd

def extract_tables(pdf_file):
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            for tbl in page.extract_tables():
                df = pd.DataFrame(tbl[1:], columns=tbl[0])
                tables.append(df)
    return tables
