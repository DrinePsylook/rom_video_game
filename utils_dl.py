import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import tempfile

from utils import temp_dir
from utils_fusion import fusion_files
from utils_txt import return_df_txt, transform_xml, create_custom_xml, clean_dies

def dl_txt_from_xml(uploaded_tab, df_txt):
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
    
def dl_xml_from_txt(uploaded_txt):
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

