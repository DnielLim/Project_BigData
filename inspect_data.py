import duckdb
import pandas as pd
import os

print("=== INSPECTING DATA FILES ===")
# 1. e-shop clothing 2008.csv
csv_path = 'Data/e-shop clothing 2008.csv'
if os.path.exists(csv_path):
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        line_count = sum(1 for _ in f)
    print(f"e-shop clothing lines: {line_count}")
    df_sample = pd.read_csv(csv_path, sep=None, engine='python', nrows=3)
    print("e-shop columns:", df_sample.columns.tolist())
    print("e-shop sample:\n", df_sample.iloc[0].to_dict())

# 2. Online Retail.xlsx
excel_path = 'Data/Online Retail.xlsx'
if os.path.exists(excel_path):
    print(f"\nChecking {excel_path} sheet names...")
    xl = pd.ExcelFile(excel_path)
    print("Sheets:", xl.sheet_names)
    df_xl = xl.parse(xl.sheet_names[0], nrows=5)
    print("Online Retail columns:", df_xl.columns.tolist())

# 3. online_retail_II.xlsx
excel2_path = 'Data/online_retail_II.xlsx'
if os.path.exists(excel2_path):
    print(f"\nChecking {excel2_path} sheet names...")
    xl2 = pd.ExcelFile(excel2_path)
    print("Sheets:", xl2.sheet_names)
