import streamlit as st
import pandas as pd
import os
import sys

from utils import recolectar_eventos

# ------ Pagina para descargar y visualizar datos de eventos registrados ----- #

sys.path.append('../.')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")
st.sidebar.image("static/logo_ppcc.png", use_container_width=True)


df_eventos, n_eventos = recolectar_eventos()
if n_eventos != 0:
    eventos = df_eventos['Evento'].tolist()
    nombres = df_eventos['Nombre'].tolist()
    st.header("Precipitación acumulada por evento")
    for i, (evento, nombre) in enumerate(zip(eventos, nombres)):
        with st.expander(f'Evento: {nombre}'):
            path = os.path.join('.', 'eventos', evento)
            df = pd.read_csv(path, index_col=0)
            df = df[['Alias', 'Grupo', 'Latitud', 'Longitud', 'Precipitacion']]
            df = df.rename({'Precipitacion': 'Precipitación (mm)'}, axis=1)
            st.dataframe(df)
    st.sidebar.markdown('---')
    data = [pd.read_csv(os.path.join('.', 'eventos', evento), index_col=0)
            for evento in eventos]
    data = pd.concat(data, keys=nombres).droplevel(1)
    data.index.name = 'Evento'
    data.to_csv('tmp/Eventos.csv')
    fbytes = open('tmp/Eventos.csv', 'rb')
    st.download_button('Descargar Base de Datos', fbytes,
                       on_click="rerun", use_container_width=True,
                       file_name='Eventos.csv', mime='text/csv')


else:
    st.warning('No hay eventos disponibles para mostrar.')
    st.stop()
