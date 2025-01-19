import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import tempfile

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from utils_txt import transform_xml, clean_dies, create_custom_xml, return_df_txt
from utils_fusion import fusion_files, clean_txt, remove_whitespace, clean_dataframe_for_xml

txt_col = ['#Name', 'Title', 'Emulator', 'CloneOf', 'Year', 'Manufacturer',
            'Category', 'Players', 'Rotation', 'Control', 'Status', 'DisplayCount',
            'DisplayType', 'AltRomname', 'AltTitle', 'Extra', 'Buttons', 'Series',
            'Language', 'Region', 'Rating']
df_txt = pd.DataFrame(columns=txt_col)

st.set_page_config(page_title="ROM video games",
                   page_icon="🎮",
                   layout="wide")

st.title("Transformation et Téléchargement de fichiers ROM")

col1, col2 = st.columns(2)
temp_dir = tempfile.mkdtemp()

with col1:
    # uploade les fichiers de type xml, xls
    uploaded_tab = st.file_uploader("Choisissez un fichier xml ou xls",
                                    accept_multiple_files=False,
                                    type=['xml', 'xls', 'xsls'])
    
    if uploaded_tab is not None:
        with st.spinner('Chargement du fichier en cours...'):
            xml_uploaded = io.StringIO(uploaded_tab.getvalue().decode('utf-8'))
            df_xml = pd.read_xml(xml_uploaded, parser='etree')
            print("df_xml.columns : ", df_xml.columns)
            name_xml = uploaded_tab.name.split(".")
            new_xml_name = f"New_{name_xml[0]}.txt".replace(" ", "_")

            fusion_for_txt = fusion_files(df_xml, df_txt)
            new_df_fusion_txt = return_df_txt(fusion_for_txt)
            csv_buffer1 = io.StringIO() 
            new_df_fusion_txt.to_csv(csv_buffer1, sep=";", index=False) 
            csv_content1 = csv_buffer1.getvalue()
            
            valid_xml= st.download_button(
                label="Télécharger au format txt",
                data=csv_content1,
                file_name = new_xml_name,
                mime="application/txt"
                )

with col2:
    #uploade fichier txt
    uploaded_txt = st.file_uploader("Choisissez un fichier txt",
                                    accept_multiple_files=False,
                                    type=['txt', 'dat'])

    if uploaded_txt is not None :
        with st.spinner('Chargement du fichier en cours...'):
            # st.write(uploaded_txt.getvalue())
            file_uploaded = clean_dies(uploaded_txt.getvalue())

            # transformation du fichier txt uploadé
            df_cleaned = transform_xml(file_uploaded)
            xml_content = create_custom_xml(df_cleaned)
            
            # récupération du nom initial du txt pour renommer le nouveau fichier downloadé
            name_txt = uploaded_txt.name.split(".")
            new_df_name = f"New_{name_txt[0]}.xml".replace(" ", "_")

            # utilisation du temp pour télécharger le fichier dans le dossier téléchargement
            path = os.path.join(temp_dir, new_df_name)

            # affichage du bouton de téléchargement du fichier
            valid_txt= st.download_button(
                label="Télécharger au format xml",
                data=xml_content,
                file_name = new_df_name,
                mime="application/xml"
                )
            
            if valid_txt: 
                st.rerun()


if uploaded_tab is not None and uploaded_txt is not None:
    st.subheader("Fusion", divider = True)

    #fichier xml
    xml_uploaded = io.StringIO(uploaded_tab.getvalue().decode('utf-8'))
    df_xml = pd.read_xml(xml_uploaded, parser='etree')

    # fichier txt
    new_txt_upld = clean_txt(uploaded_txt)
    df_txt = remove_whitespace(new_txt_upld)

    new_file_xml_name = f"Fusion_{name_txt[0]}_{name_xml[0]}.xml".replace(" ", "_")
    with st.spinner('Chargement du fichier en cours...'):
        valid_fusion = st.button("Fusionner les fichiers XML et txt")
    if valid_fusion:        
        st.subheader("Télécharger les fichiers fusionnés", divider=True)

        fusion = fusion_files(df_xml, df_txt)
        xml_content = create_custom_xml(fusion)

        col3, col4, col5 = st.columns([2, 2, 8])
        with col3 :
            with st.spinner('Chargement du fichier en cours...'):
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
            with st.spinner('Chargement du fichier en cours...'):
                valid_fusion_txt = st.download_button(
                    label= "Télécharger la fusion au format txt",
                    data = csv_content,
                    file_name=new_file_txt_name,
                    mime="application/txt"
                )
