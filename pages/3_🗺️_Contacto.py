import os
import streamlit as st
# ------------------------------- PAGINA INICIO ------------------------------ #
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")


st.image(os.path.join('static', 'imagen_satelital1.png'))
st.header('Red de Pluviómetros Ciudadanos')
st.markdown("""
El proyecto Pluviómetros Ciudadanos (PPCC) es una iniciativa de ciencia
ciudadana que se desarrolló en el 
[Departamento de Geofísica (DGF)](http://www.dgf.uchile.cl/) de la 
[Facultad de Ciencias Físicas y Matemáticas (FCFM) de la Universidad de 
Chile](https://ingenieria.uchile.cl/) con el objetivo de estudiar los 
efectos topográficos sobre la distribución espacial de la precipitación 
en la Región Metropolitana, a partir de mediciones realizadas por 
observadores(as) voluntarios(as) e información de estaciones meteorológicas automáticas 
(EMA) pertenecientes o coordinadas por varios organismos, entre ellos la Dirección
Meteorológica de Chile (DMC) y la Dirección General de Aguas (DGA).
El proyecto comenzó en el 2021.

La información de precipitación que se obtiene a través de este proyecto es
de libre acceso y se publica en este sitio Web en forma de tablas (viñeta Registros)
y mapas (viñeta Mapas). Los puntos de medición de los(as) observadores que colaboran con
el proyecto se identifican mediante un alias.

Al hacer un click sobre un punto de medición en el mapa se despliega 
información sobre el nombre de la estación meteorológica o el alias del 
punto de medición, el valor de la precipitación acumulada en milímetros y 
una caracterización (Grupo) con los códigos EMA si corresponde a una 
estación meteorológica automática o RM, V-R, VI-R para identificar a qué 
filial del proyecto pertenece la persona que realiza la observación.

El contacto para quienes deseen colaborar con este proyecto es el siguiente:

Prof. Patricio Aceituno, Dpt. de Geofísica, FCFM - U. de Chile.
Correo: aceituno@uchile.cl
""")

path1, path2 = [os.path.join('static', f) for f in ['logo_ppcc.png', 'logo_dgf.png']]
st.sidebar.image(path1, use_container_width=True)


cols = st.columns(4)
with cols[0]:
    st.image(path1, use_container_width=True)
with cols[2]:
    st.image(path2, use_container_width=True)
# with cols[4]:
#     st.image(path3, use_container_width=True)
# with cols[6]:
#     st.image(path4, use_container_width=True)
# with cols[8]:
#     st.image(path5, use_container_width=True)
