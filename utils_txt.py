import streamlit as st
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import os
import io

def clean_dies(file_verif): 
    # Conversion des bytes en string
    file_verif_str = file_verif.decode('utf-8')
    lines = file_verif_str.splitlines()
    cleaned_lines = [lines[0]] + [line for line in lines[1:] if not line.startswith("#")]
    return cleaned_lines

def clean_xml_string(text):
    if text is None or pd.isna(text):
        return ""
    
    text = str(text)
    if text == "":
        return None

    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    
    return text

def adjust_columns(header, lines): 
    # fonction qui ajuste et redimensionne le tableau s'il y a une différence entre la taille des colonnes et des données par ligne -> malheureusement, perte de données
    adjusted_data = [] 
    for line in lines: 
        columns = line.strip().split(';') 
        if len(columns) > len(header): 
            diff = len(columns) - len(header)
            columns = columns[:-diff] 
            # Retire la/les dernière(s) colonne en trop 
        adjusted_data.append(columns) 
    return adjusted_data

def transform_xml(cleaned_lines):
    header = cleaned_lines[0].replace("#", "").strip().split(';')
    data_lines = cleaned_lines[1:]
    data = [line.split(";") for line in data_lines]
    if len(data_lines) > len(header):
        adjusted_data = adjust_columns(header, data_lines) 

    df_file = pd.DataFrame(adjusted_data, columns=header)
    df_file = df_file.applymap(lambda x: np.nan if x is None else x)
    for col in df_file.columns:
        df_file[col] = df_file[col].astype(object).replace("", np.nan)

    file_xml = df_file.reset_index(drop=True)
    file_xml.columns = file_xml.columns.str.lower()
    # print("file xml colonnes = ",file_xml.columns)
    
    for col in df_file.columns :
        df_file[col] = df_file[col].apply(clean_xml_string)

    return file_xml

def create_custom_xml(df):
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str += '<data>\n'

    for _, row in df.iterrows():
        xml_str += '    <row>\n'
        for col in df.columns:
            value = clean_xml_string(row[col])
            if value is not None: 
                xml_str += f'   <{col}>{value}</{col}>\n'
                # print("valeur = ",value)
            else:
                xml_str +=f'   <{col}>{np.nan}</{col}>\n'
        xml_str += '    </row>\n'
    xml_str += '</data>'
    return xml_str