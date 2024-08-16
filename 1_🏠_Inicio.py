import streamlit as st
from params import *
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

st.sidebar.image(f"static{path_sep}logo_ppcc.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_dgf.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_cr2.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_uoh.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_uvalpo.png", use_column_width=True)


# col1, col2 = st.columns([0.8, 0.2], gap='large')

st.image(f'static{path_sep}imagen_satelital1.png')
st.header('Red de Pluviómetros Ciudadanos')
st.markdown("""
El proyecto Pluviómetros Ciudadanos (PPCC) es una iniciativa de ciencia
ciudadana que se desarrolló en el [Departamento de Geofísica (DGF)](http://www.dgf.uchile.cl/)
de la [Facultad de Ciencias Físicas y Matemáticas (FCFM) de la Universidad de Chile](https://ingenieria.uchile.cl/)
con el objetivo es estudiar los efectos topográficos sobre la
distribución espacial de la precipitación en la Región Metropolitana, a
partir de mediciones realizadas por observadores(as) voluntarios(as) y de
estaciones meteorológicas automáticas (EMA) de la red nacional. El
proyecto comenzó en el 2021 ampliándose en el 2024 a las regiones V y VI,
a través de iniciativas similares coordinadas con el [Departamento de Meteorología de la Universidad de Valparaiso](https://meteo.uv.cl)
y el [Instituto de Ciencias de la Ingeniería de la Universidad de O ́Higgins](https://www.uoh.cl/instituto-de-ciencias-de-la-ingenieria/).

La información de precipitación que se obtiene a través de este proyecto
es de libre acceso y se publica en este sitio Web en forma de tablas
(botón Registros) y mapas (botón Mapas).  Los puntos de medición de
los(as) observadores que colaboran con el proyecto se identifican mediante
un alias.

Al hacer un click sobre un punto de medición en un mapa se despliega
información sobre el nombre de la estación meteorológica o el alias del
punto de medición, el valor de la precipitación acumulada en milímetros y
una caracterización (Grupo) con los códigos EMA si corresponde a una
estación meteorológica automática o RM, V-R, VI-R para identificar a que
filial del proyecto pertenece la persona que realiza la observación.

Los contactos para quienes deseen colaborar con este proyecto son los
siguientes, dependiendo de la región de residencia:

* Región Metropolitana:
Prof. Patricio Aceituno, Dpt. de Geofísica, FCFM - U. de Chile
Correo electrónico: aceituno@uchile.cl

* V Región
Prof. Ana María Córdoba, Dpt. de Meteorología, U. de Valparaíso
Correo electrónico: anamaria.cordova@uv.cl

* VI Región
Prof. Raúl Valenzuela, Instituto de Ciencias de la Ingeniería, U. de
O'Higgins
Correo electrónico: raul.valenzuela@uoh.cl
            """, )

# with col2:
# st.image(f'static{path_sep}logo_dgf.png')
# st.divider()
# st.image(f'static{path_sep}logo_ppcc.png')
# st.divider()
# st.image(f'static{path_sep}logo_cr2.jpg')
