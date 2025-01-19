import streamlit as st
import pandas as pd
import numpy as np
import os
import io


import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from utils import df_txt, temp_dir
from utils_txt import transform_xml, clean_dies, create_custom_xml, return_df_txt
from utils_fusion import fusion_files, clean_txt, remove_whitespace, dl_fusion_xml
from utils_dl import dl_txt_from_xml, dl_xml_from_txt



st.set_page_config(page_title="ROM video games",
                   page_icon="🎮",
                   layout="wide")

st.title("Transformation et Téléchargement de fichiers ROM")

col1, col_a, col2, col_b = st.columns([10, 2, 10, 2])


with col1:
    # uploade les fichiers de type xml, xls
    uploaded_tab = st.file_uploader("Choisissez un fichier xml ou xls",
                                    accept_multiple_files=False,
                                    type=['xml', 'xls', 'xsls'])
    

# with col_a:
    # ajout_xml_file = st.button("Ajout XML")

# second_uploaded_xml = None

# if ajout_xml_file:
#     with col1:
#         second_uploaded_xml = st.file_uploader("Choisissez un second fichier xml ou xls",
#                                         accept_multiple_files=False,
#                                         type=['xml', 'xls', 'xsls'])

if uploaded_tab is not None:
    with st.spinner('Chargement du fichier en cours...'):
        dl_txt_from_xml(uploaded_tab, df_txt)

# if uploaded_tab is not None and second_uploaded_xml is not None:
#     dl_fusion_xml(uploaded_tab, second_uploaded_xml)

with col2:
    #uploade fichier txt
    uploaded_txt = st.file_uploader("Choisissez un fichier txt",
                                    accept_multiple_files=False,
                                    type=['txt', 'dat'])

    if uploaded_txt is not None :
        with st.spinner('Chargement du fichier en cours...'):
            dl_xml_from_txt(uploaded_txt)

with col_b:
    ajout_txt_file = st.button("Ajout txt")
    

                

if uploaded_tab is not None and uploaded_txt is not None:
    st.subheader("Fusion", divider = True)

    #fichier xml
    xml_uploaded = io.StringIO(uploaded_tab.getvalue().decode('utf-8'))
    df_xml = pd.read_xml(xml_uploaded, parser='etree')

    # fichier txt
    new_txt_upld = clean_txt(uploaded_txt)
    df_txt = remove_whitespace(new_txt_upld)

    name_txt = uploaded_txt.name.split(".")
    name_xml = uploaded_tab.name.split(".")
    new_file_xml_name = f"Fusion_{name_txt[0]}_{name_xml[0]}.xml".replace(" ", "_")
    with st.spinner('Fusion du fichier en cours...'):
        valid_fusion = st.button("Fusionner les fichiers XML et txt")
    if valid_fusion:        
        st.subheader("Télécharger les fichiers fusionnés", divider=True)

        fusion = fusion_files(df_xml, df_txt)
        xml_content = create_custom_xml(fusion)

        col3, col4, col5 = st.columns([2, 2, 8])
        with col3 :
            with st.spinner('Téléchargement du fichier en cours...'):
                valid_fusion_xml = st.download_button(
                    label= "Télécharger la fusion au format XML",
                    data = xml_content,
                    file_name=new_file_xml_name,
                    mime="application/xml"
                )

        new_file_txt_name = f"Fusion_{name_txt[0]}_{name_xml[0]}.txt".replace(" ", "_")
        new_df_txt = return_df_txt(fusion)
        csv_buffer = io.StringIO() 
        new_df_txt.to_csv(csv_buffer, sep=";", index=False) 
        csv_content = csv_buffer.getvalue()

        with col4:
            with st.spinner('Téléchargement du fichier en cours...'):
                valid_fusion_txt = st.download_button(
                    label= "Télécharger la fusion au format txt",
                    data = csv_content,
                    file_name=new_file_txt_name,
                    mime="application/txt"
                )
