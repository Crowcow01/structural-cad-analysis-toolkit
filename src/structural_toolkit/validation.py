import pandas as pd

def compare_results(python_file,sap_file,id_column,python_column,sap_column):
    py=pd.read_csv(python_file); sap=pd.read_csv(sap_file)
    c=py.merge(sap,on=id_column,suffixes=("_python","_sap"))
    pycol=python_column if python_column in c.columns else f"{python_column}_python"
    sapcol=sap_column if sap_column in c.columns else f"{sap_column}_sap"
    c["absolute_error"]=(c[pycol]-c[sapcol]).abs()
    c["percentage_error"]=c["absolute_error"]/c[sapcol].abs().replace(0,float("nan"))*100
    return c
