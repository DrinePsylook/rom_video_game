import streamlit as st
import pandas as pd
import numpy as np
import tempfile

txt_col = ['#Name', 'Title', 'Emulator', 'CloneOf', 'Year', 'Manufacturer',
            'Category', 'Players', 'Rotation', 'Control', 'Status', 'DisplayCount', 'DisplayType', 'AltRomname', 'AltTitle', 'Extra', 'Buttons', 'Series', 'Language', 'Region', 'Rating']
df_txt = pd.DataFrame(columns=txt_col)

temp_dir = tempfile.mkdtemp()