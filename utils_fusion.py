import streamlit as st
import pandas as pd
import numpy as np
import io

from utils_txt import clean_dies, adjust_columns, clean_xml_string, transform_xml

def fusion_files(df_xml, df_txt):
    df_txt = df_txt.rename(columns={"#Name":"name"})
    df_txt.columns = df_txt.columns.str.lower()
    df_combined = pd.merge(df_xml, df_txt, on="name", how="outer")
    df_combined = df_combined.applymap(lambda x: np.nan if x is None else x)

    # Récupération des noms de colonnes de base
    combined_columns =[]
    for col in df_combined.columns:
        if col.endswith("_y") or col.endswith("_x"):
            base_col = col.replace("_y", "").replace("_x", "")
            if base_col not in combined_columns:
                combined_columns.append(base_col)
                        
    # fusion des colonnes _y(xml) et _x (txt)
    for col in combined_columns:
        col_xml = f"{col}_y"
        col_txt = f"{col}_x"
        if col_xml in df_combined.columns and col_txt in df_combined.columns:
            df_combined[col] = df_combined[col_xml].combine_first(df_combined[col_txt])

    # drop des colonnes _y et _x devenues inutiles 
    df_combined = df_combined.drop(columns=[f"{col}_y" for col in combined_columns if f"{col}_y" in df_combined.columns] + [f"{col}_x" for col in combined_columns if f"{col}_x" in df_combined.columns])
        
    return df_combined


def clean_txt(file):
    txt_upld = clean_dies(file.getvalue())
    txt_upld_str = "\n".join(txt_upld)

    header = txt_upld_str.strip().split(';') 
    data_lines = txt_upld[1:] 
    if len(data_lines) > 0 and len(data_lines[0].split(';')) > len(header):         
        adjusted_data = adjust_columns(header, data_lines) 
    else: 
        adjusted_data = data_lines 
    
    header_str = ";".join(header)
    adjusted_data_str = "\n".join(["".join(row) for row in adjusted_data])
    new_txt_upld_str = f"{header_str}\n{adjusted_data_str}"
    # print(new_txt_upld_str)
    
    return new_txt_upld_str

def remove_whitespace(df): 
    for col in df.columns: 
        # Enlève les espaces pour chaque cellule 
        df[col] = df[col].str.strip() 
        return df

def clean_dataframe_for_xml(df): 
    for col in df.columns: 
        df[col] = df[col].apply(clean_xml_string) 
    return df