import tabula
import pandas as pd
import tempfile

def extract_tables_tabula(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        tmp_path = tmp.name

    try:
        dfs = tabula.read_pdf(tmp_path, pages="all", multiple_tables=True, lattice=True)
        return dfs
    except Exception as e:
        print(f"Extraction error: {e}")
        return []
