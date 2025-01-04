import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Transformation et Téléchargement de fichiers ROM",
                   page_icon="🎮",
                   layout="wide")

st.title("Choisissez votre fichier à télécharger")

col1, col2 = st.columns(2)

with col1:
    option_tab = st.selectbox(
        "Choississez votre type de tableur :",
        ("xmml", "xlsx"),
        placeholder="Sélectionnez le fichier"
    )
    uploaded_tab = st.file_uploader("Choisissez un fichier")
    valid_tab = st.button("Validation tableur")

with col2:
    valid_txt= 