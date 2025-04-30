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
observadores(as) voluntarios(as) y de estaciones meteorológicas automáticas 
(EMA) de la red nacional. El proyecto comenzó en el 2021 ampliándose en el 
2024 a las regiones de Valparaíso (V) y O'higgins (VI), a través de 
iniciativas similares coordinadas con el 
[Departamento de Meteorología de la Universidad de Valparaiso](https://meteo.uv.cl) 
y el 
[Instituto de Ciencias de la Ingeniería de la Universidad de O'Higgins]
(https://www.uoh.cl/instituto-de-ciencias-de-la-ingenieria/).

La información de precipitación que se obtiene a través de este proyecto 
es de libre acceso y se publica en este sitio Web en forma de tablas 
(viñeta Registros) y mapas (viñeta Mapas). Los puntos de medición de los(as) 
observadores que colaboran con el proyecto se identifican mediante un alias.

Al hacer un click sobre un punto de medición en el mapa se despliega 
información sobre el nombre de la estación meteorológica o el alias del 
punto de medición, el valor de la precipitación acumulada en milímetros y 
una caracterización (Grupo) con los códigos EMA si corresponde a una 
estación meteorológica automática o RM, V-R, VI-R para identificar a qué 
filial del proyecto pertenece la persona que realiza la observación.

Los contactos para quienes deseen colaborar con este proyecto son los 
siguientes, dependiendo de la región de residencia:

* Región Metropolitana:
    Prof. Patricio Aceituno, Dpt. de Geofísica, FCFM - U. de Chile.
    Correo electrónico: aceituno@uchile.cl

* V Región:
    Prof. Ana María Córdoba, Dpt. de Meteorología, U. de Valparaíso.
    Correo electrónico: anamaria.cordova@uv.cl

* VI Región:
    Prof. Raúl Valenzuela, Instituto de Ciencias de la Ingeniería, U. de 
    O'Higgins.
    Correo electrónico: raul.valenzuela@uoh.cl
""")

path1, path2, path3, path4, path5 = [os.path.join('static', f) for f in
                                     ['logo_ppcc.png', 'logo_dgf.png',
                                      'logo_uvalpo.png', 'logo_uoh.png',
                                      'logo_cr2.png']]
st.sidebar.image(path1, use_container_width=True)


cols = st.columns(9)
with cols[0]:
    st.image(path1, use_container_width=True)
with cols[2]:
    st.image(path2, use_container_width=True)
with cols[4]:
    st.image(path3, use_container_width=True)
with cols[6]:
    st.image(path4, use_container_width=True)
with cols[8]:
    st.image(path5, use_container_width=True)
