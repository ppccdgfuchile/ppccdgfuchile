from params import *
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
import sys
# import locale
sys.path.append('../.')

# Use Spanish Locale
# locale.setlocale(locale.LC_TIME, 'es_ES')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

st.sidebar.image(f"static{path_sep}logo_ppcc.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_dgf.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_cr2.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_uoh.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_uvalpo.png", use_column_width=True)


events = sorted(os.listdir(f".{path_sep}eventos"))
events_names = sorted([e.split('.')[0].replace(
    '-', '/').replace('_', ' - ') for e in events], reverse=True)

st.header("Precipitación acumulada por evento")
for i, event, name in zip(range(len(events)), events, events_names):
    with st.expander(f'Evento: {name}'):
        df = pd.read_csv(f'.{path_sep}eventos{path_sep}{event}', index_col=0)
        df = df[['alias', 'grupo', 'lat', 'lon', 'pp']]
        df.columns = ['Alias', 'Grupo', 'Latitud',
                      'Longitud', 'Precipitacion (mm)']
        st.dataframe(df)
