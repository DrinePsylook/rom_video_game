import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import tempfile

from utils import transform_xml, clean_dies

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
        # st.write(uploaded_txt.getvalue())
        # st.write(message_loading)
        file_uploaded = clean_dies(uploaded_txt.getvalue())
        # print("file_uploaded = " , file_uploaded[:10])
    
        # transforme le fichier uploadé en string
        # file_uploaded = io.StringIO(uploaded_txt.getvalue().decode('utf-8'))

        # transformation du fichier txt uploadé
        df_cleaned = transform_xml(file_uploaded)
        st.write("Aperçu des données nettoyées :")
        st.write(df_cleaned.head())
        # récupération du nom initial du txt pour renommer le nouveau fichier downloadé
        name0 = uploaded_txt.name.split(".")
        new_df_name = f"New_{name0[0]}.xml".replace(" ", "_")

        # utilisation du temp pour télécharger le fichier dans le dossier téléchargement
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, new_df_name)
        df_cleaned.to_xml(path, index=False, parser='etree')
        
        with open(path, 'r', encoding='utf-8') as file: 
            xml_content = file.read()

        # affichage du bouton de téléchargement du fichier
        valid_txt= st.download_button(
            label="Télécharger au format xml",
            data=xml_content,
            file_name = new_df_name,
            mime="application/xml"
            )
        
        if valid_txt:
            message_loading = ""

        

