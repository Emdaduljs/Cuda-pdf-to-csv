import tabula
import pdfplumber
import pandas as pd
import tempfile

def extract_tables_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        tmp_path = tmp.name

    # Try Tabula (lattice mode)
    try:
        dfs_lattice = tabula.read_pdf(tmp_path, pages="all", multiple_tables=True, lattice=True)
        if dfs_lattice and any(len(df) > 0 for df in dfs_lattice):
            return dfs_lattice
    except Exception as e:
        print(f"Tabula lattice error: {e}")

    # Try Tabula (stream mode)
    try:
        dfs_stream = tabula.read_pdf(tmp_path, pages="all", multiple_tables=True, stream=True)
        if dfs_stream and any(len(df) > 0 for df in dfs_stream):
            return dfs_stream
    except Exception as e:
        print(f"Tabula stream error: {e}")

    # Fallback to pdfplumber
    try:
        tables = []
        with pdfplumber.open(tmp_path) as pdf:
            for i, page in enumerate(pdf.pages):
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    tables.append(df)
        return tables
    except Exception as e:
        print(f"PDFPlumber error: {e}")

    return []
