import streamlit as st
from params import *

st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

col1, col2 = st.columns([0.8, 0.2], gap='large')

with col1:
    st.header('Pluviómetros Ciudadanos DGF')
    st.markdown("""
                El proyecto Pluviómetros Ciudadanos (PPCC) es una iniciativa de ciencia ciudadana desarrollada inicialmente en el [Departamento de Geofísica (DGF)](http://www.dgf.uchile.cl/) de la [Facultad de Ciencias Físicas y Matemáticas (FCFM) de la Universidad de Chile](https://ingenieria.uchile.cl/). Su objetivo es estudiar la relación entre la precipitación y la geografía nacional (cerros, valles, quebradas, etc) gracias a la colaboración de voluntarios/as independientes de su edad o actividad.
            
                En este repositorio se encuentra la información y mediciones recopiladas por los voluntarios, además de las herramientas desarrolladas para su despliegue público en la web.
                """, )

with col2:
    st.image(f'static{path_sep}logo_dgf.png')
    st.divider()
    st.image(f'static{path_sep}logo_ppcc.png')
