import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import tempfile

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from utils_txt import transform_xml, clean_dies, create_custom_xml
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
            name_xml = uploaded_tab.name.split(".")
            new_xml_name = f"New_{name_xml[0]}.xml".replace(" ", "_")
            
            valid_xml= st.download_button(
                label="Télécharger au format txt",
                data="",
                file_name = new_xml_name,
                mime="application/xml"
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
    txt_upld = clean_txt(uploaded_txt)
    new_txt_upld = io.StringIO(txt_upld)
    df_txt = pd.read_csv(new_txt_upld, delimiter=";")
    df_txt = remove_whitespace(df_txt)

    new_file_xml_name = f"Fusion_{name_txt[0]}_{name_xml[0]}.xml".replace(" ", "_")

    valid_fusion = st.button("Fusionner les fichiers XML et txt")
    if valid_fusion:        
        st.subheader("Télécharger les fichiers fusionnés", divider=True)

        fusion = fusion_files(df_xml, df_txt)
        xml_content = create_custom_xml(fusion)

        col3, col4, col5 = st.columns([2, 2, 8])
        with col3 :
            valid_fusion_xml = st.download_button(
                label= "Télécharger la fusion au format XML",
                data = xml_content,
                file_name=new_file_xml_name,
                mime="application/xml"
            )
        with col4:
            valid_fusion_txt = st.download_button(
                label= "Télécharger la fusion au format txt",
                data ="",
                file_name="",
                mime="application/txt"
            )
