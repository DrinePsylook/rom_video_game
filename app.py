import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import tempfile

from utils_txt import transform_xml, clean_dies, create_custom_xml

st.set_page_config(page_title="ROM video games",
                   page_icon="🎮",
                   layout="wide")

st.title("Transformation et Téléchargement de fichiers ROM")

col1, col2 = st.columns(2)

with col1:
    # uploade les fichiers de type xml, xls
    uploaded_tab = st.file_uploader("Choisissez un fichier xml ou xls",
                                    accept_multiple_files=False,
                                    type=['xlm', 'xls', 'xsls'])
    valid_xml = st.button("Télécharger au format txt")

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
            name0 = uploaded_txt.name.split(".")
            new_df_name = f"New_{name0[0]}.xml".replace(" ", "_")

            # utilisation du temp pour télécharger le fichier dans le dossier téléchargement
            temp_dir = tempfile.mkdtemp()
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

       