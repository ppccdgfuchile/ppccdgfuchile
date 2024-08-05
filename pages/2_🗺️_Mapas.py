from params import *
import streamlit as st
import pandas as pd

import plotly.express as px

from streamlit_folium import st_folium
import folium  # for interactive maps
# to select the maptype we want to use
from folium import Circle, Marker, CircleMarker
from folium.plugins import HeatMap, MarkerCluster  # for plugins
import branca.colormap as cm
from datetime import datetime
import sys
# import locale
sys.path.append('../.')

# locale.setlocale(locale.LC_TIME, 'es_ES')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

events = sorted(os.listdir(f".{path_sep}eventos"))
events_names = [datetime.strptime(e.split(".")[0], "%Y-%m-%d").strftime("%d/%m/%Y")
                for e in events]

target_event = st.selectbox(
    'Seleccione el evento a visualizar', events_names)


df = pd.read_csv(
    f'.{path_sep}eventos{path_sep}{events[events_names.index(target_event)]}')
df_map = df[['lat', 'lon', 'pp']].astype('float64')
df_map['nombre'] = df['nombre']
df_map['alias'] = df['alias']
df_map.dropna(inplace=True)
st.header(f'Precipitaciones acumuladas: Evento {target_event}')

# ---------------------------------------------------------------------------- #
# BASEMAPS

# google_maps_tile = folium.TileLayer(
#     tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
#     attr='Esri',
#     name='Esri Satellite',
#     overlay=False,
#     control=True
# )


# google_hybrid_tile = folium.TileLayer(
#     tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
#     attr='Esri',
#     name='Esri Satellite',
#     overlay=False,
#     control=True
# )

google_satellite_tile = folium.TileLayer(
    tiles='http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}',
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True
)

# ---------------------------------------------------------------------------- #
folium_map = folium.Map(location=[-33.4489, -70.6693],
                        tiles=google_satellite_tile, zoom_start=11)

colormap = cm.linear.YlGnBu_09.scale(df.pp.min(), df.pp.max())
for idx, row in df_map.iterrows():
    # color = colormap.scale(row.pp)
    popup = folium.Popup(
        f"<b>Alias:</b> {row.alias} <br> <b>Precipitación:</b> {row.pp} [mm] <br>", max_width=1000)
    # Circle(location=[row.lat, row.lon], radius=1, color='darkblue',
    #        fill_color='darkblue', fill=True, fill_opacity=1).add_to(folium_map)
    CircleMarker(location=[row.lat, row.lon],
                 radius=row.pp/2,
                 stroke=True,
                 weight=0.75,
                 color='black',
                 fill_color=colormap(row.pp), fill=True,
                 fill_opacity=0.8,
                 popup=popup).add_to(folium_map)

st_map = st_folium(folium_map, width=1300, height=700)

# st.divider()

# st.header('Mapa evento YYYY/MM/dd - Heatmap')
# # Create a base map
# folium_map2 = folium.Map(location=[-33.4489, -70.6693],
#                          tiles='cartodbpositron', zoom_start=9)
# HeatMap(df_map[['lat', 'lon']], radius=25, blur=25).add_to(folium_map2)
# st_map2 = st_folium(folium_map2, width=1300, height=700)
