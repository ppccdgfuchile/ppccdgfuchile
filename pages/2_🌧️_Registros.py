from params import *
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
import sys

# ----------------- Pagina para descargar eventos registrados ---------------- #

sys.path.append('../.')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")
st.sidebar.image(f"static{path_sep}logo_ppcc.png", use_column_width=True)

events = sorted(os.listdir('eventos'), reverse=True)
events_names = [e.split('.')[0].replace('-', '/').replace('_', ' - ')
                for e in events]
st.header("Precipitación acumulada por evento")
for i, event, name in zip(range(len(events)), events, events_names):
    with st.expander(f'Evento: {name}'):
        path = os.path.join('.', 'eventos', event)
        df = pd.read_csv(path, index_col=0)
        df = df[['alias', 'grupo', 'lat', 'lon', 'pp']]
        df.columns = ['Alias', 'Grupo', 'Latitud',
                      'Longitud', 'Precipitacion (mm)']
        st.dataframe(df)
