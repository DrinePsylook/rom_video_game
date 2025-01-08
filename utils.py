import streamlit as st
import pandas as pd
import numpy as np
import os
import io

def adjust_columns(header, lines): 
    # fonction qui ajuste et redimensionne le tableau s'il y a une différence entre la taille des colonnes et des données par ligne -> malheureusement, perte de données
    adjusted_data = [] 
    for line in lines: 
        columns = line.strip().split(';') 
        if len(columns) > len(header): 
            diff = len(header) - len(columns)
            columns = columns[:diff] 
            # Retire la/les dernière(s) colonne en trop 
        adjusted_data.append(columns) 
    return adjusted_data

def clean_dies(file_verif): 
    # Conversion des bytes en string
    file_verif_str = file_verif.decode('utf-8')
    lines = file_verif_str.splitlines()
    cleaned_lines = [lines[0]] + [line for line in lines[1:] if not line.startswith("#")]
    return cleaned_lines

def transform_xml(cleaned_lines):
    header = cleaned_lines[0].split(';')
    data_lines = cleaned_lines[1:]
    data = [line.split(";") for line in data_lines]
    adjusted_data = adjust_columns(header, data_lines) 

    df_file = pd.DataFrame(adjusted_data, columns=header)

    file_xml = df_file.reset_index(drop=True)
    print("file xml colonnes = ",file_xml.columns)
    file_xml.columns = file_xml.columns.str.lower()
    if '#name' in file_xml.columns:
        file_xml = file_xml.rename(columns={"#name":"name"})

    return file_xml
