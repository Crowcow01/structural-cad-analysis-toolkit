import pandas as pd, sys
filename=sys.argv[1] if len(sys.argv)>1 else "240276_output.xlsx"
excel=pd.ExcelFile(filename)
for sheet in excel.sheet_names:
    print("\n"+"="*80); print(sheet); print("="*80)
    df=pd.read_excel(filename,sheet_name=sheet)
    print(df.head(10).to_string(index=False)); print("\nColumns:"); print(df.columns.tolist())
