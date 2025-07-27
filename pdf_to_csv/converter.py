import tabula
import pdfplumber
import pandas as pd
import tempfile
from pdf2image import convert_from_bytes
import pytesseract

def extract_tables_from_pdf(pdf_bytes):
    # Write PDF to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes.read())
        tmp_path = tmp.name

    # Try Tabula lattice
    try:
        dfs = tabula.read_pdf(tmp_path, pages="all", multiple_tables=True, lattice=True)
        if dfs and any(len(df) > 0 for df in dfs):
            return dfs
    except Exception:
        pass

    # Try Tabula stream
    try:
        dfs = tabula.read_pdf(tmp_path, pages="all", multiple_tables=True, stream=True)
        if dfs and any(len(df) > 0 for df in dfs):
            return dfs
    except Exception:
        pass

    # Try pdfplumber fallback
    try:
        tables = []
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                tbl = page.extract_table()
                if tbl:
                    df = pd.DataFrame(tbl[1:], columns=tbl[0])
                    tables.append(df)
        if tables:
            return tables
    except Exception:
        pass

    # Final fallback: OCR
    try:
        images = convert_from_bytes(pdf_bytes.read(), dpi=300)
        text_lines = []
        for img in images:
            txt = pytesseract.image_to_string(img)
            text_lines.extend([l for l in txt.splitlines() if l.strip()])
        # crude split into columns by whitespace
        df = pd.DataFrame([line.split() for line in text_lines])
        return [df]
    except Exception:
        return []
