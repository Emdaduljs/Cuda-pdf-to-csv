import pandas as pd

def convert_excel_to_csv(input_path, output_path):
    try:
        df = pd.read_excel(input_path, sheet_name=0, engine="openpyxl")
        df.to_csv(output_path, index=False)
        return True, "Success"
    except Exception as e:
        return False, str(e)