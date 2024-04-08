import streamlit as st
import pandas as pd

import plotly.express as px

from streamlit_folium import st_folium
import folium #for interactive maps
from folium import Circle, Marker #to select the maptype we want to use
from folium.plugins import HeatMap, MarkerCluster #for plugins
import branca.colormap as cm


st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

df = pd.read_csv('data_test.csv', sep=';')
df_map = df[['lat', 'lon', 'pp']].astype('float64')
df_map['nombre'] = df['nombre']

df_map.drop(77, inplace=True)
df_map.drop(118, inplace=True)

df_map.dropna(inplace=True)

# st.header('Mapa creado con Streamlit')
# st.map(df_map, latitude='lat', longitude='lon', size='pp')
# st.divider()

st.header('Mapa evento YYYY/MM/dd - Scatter')
# Create a base map
folium_map = folium.Map(location=[-33.4489, -70.6693],
                        tiles='cartodbpositron', zoom_start=9)

for idx, row in df_map.iterrows():
    popup = folium.Popup(f"<b>Nombre:</b> {row.nombre} <br> <b>Precipitación:</b> {row.pp} [mm] <br> <b>Lat, Lon:</b> ({round(row.lat,3)}°, {round(row.lon,3)})°", max_width=1000)
    Circle(location=[row.lat, row.lon], radius=1, color='darkblue', fill_color='darkblue', fill=True, fill_opacity=1).add_to(folium_map)
    Circle(location=[row.lat, row.lon], radius=row.pp*25, color='royalblue', fill_color='royalblue', fill=True, fill_opacity=0.4, popup=popup).add_to(folium_map)

st_map = st_folium(folium_map, width=1300, height=700)

st.divider()

st.header('Mapa evento YYYY/MM/dd - Heatmap')
# Create a base map
folium_map2 = folium.Map(location=[-33.4489, -70.6693],
                         tiles='cartodbpositron', zoom_start=9)

cbar = cm.linear.BuPu_05.scale(min(df_map.pp), max(df_map.pp))
HeatMap(df_map[['lat', 'lon']], radius=25, blur=25).add_to(folium_map2)

st_map2 = st_folium(folium_map2, width=1300, height=700)
