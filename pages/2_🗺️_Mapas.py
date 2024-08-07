from params import *
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd

import numpy as np
import plotly.express as px

from streamlit_folium import st_folium
import folium  # for interactive maps
# to select the maptype we want to use
from folium import Circle, Marker, CircleMarker

import branca.colormap as cm
from datetime import datetime
# import json
# import geojson
import sys
# import locale
sys.path.append('../.')

# locale.setlocale(locale.LC_TIME, 'es_ES')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

st.sidebar.image(f"static{path_sep}logo_ppcc.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_dgf.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_cr2.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_uoh.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_uvalpo.png", use_column_width=True)


events = sorted(os.listdir(f".{path_sep}eventos"))
events_names = sorted([datetime.strptime(e.split(".")[0], "%Y-%m-%d")
                       for e in events], reverse=True)
events_names = [e.strftime("%Y/%m/%d") for e in events_names]

target_event = st.selectbox(
    'Seleccione el evento a visualizar', events_names)

target_event2 = target_event.replace('/', '-')
df = pd.read_csv(
    f'.{path_sep}eventos{path_sep}{target_event2}.csv')
df_map = df[['lat', 'lon', 'pp']].astype('float64')
df_map['nombre'] = df['nombre']
df_map['alias'] = df['alias']
df_map['grupo'] = df['grupo']
df_map.dropna(inplace=True)
st.header(f'Precipitaciones acumuladas: Evento {target_event}')

# regiones = geojson.load(open('static/REGIONES.geojson', 'r+'))

# ---------------------------------------------------------------------------- #
# BASEMAPS

# google_maps_tile = folium.TileLayer(
#     tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
#     attr='Google Maps',
#     name='Mapa',
#     overlay=False,
#     control=True
# )

google_terrain_tile = folium.TileLayer(
    tiles='http://www.google.cn/maps/vt?lyrs=p@189&gl=cn&x={x}&y={y}&z={z}',
    attr='Google Relief',
    name='Relieve',
    overlay=False,
    control=True
)

google_satellite_tile = folium.TileLayer(
    tiles='http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}',
    attr='Google Satellite',
    name='Satelite',
    overlay=False,
    control=True
)

# ---------------------------------------------------------------------------- #
folium_map = folium.Map(location=[-33.5, -70.8], zoom_start=9,
                        tiles=google_terrain_tile)

google_satellite_tile.add_to(folium_map)

group1 = folium.FeatureGroup('Pluviómetros Ciudadanos')
group2 = folium.FeatureGroup('Pluviómetros Red Nacional')
colormap = cm.linear.YlGnBu_09.scale(df.pp.min(), df.pp.max())
for idx, row in df_map[df_map.grupo != 'EMA'].iterrows():
    # color = colormap.scale(row.pp)
    popup = folium.Popup(
        f"<b>Alias:</b> {row.alias} <br> <b>Precipitación:</b> {row.pp} [mm] <br> <b>Grupo:</b> {row.grupo} <br>", max_width=1000)
    # Circle(location=[row.lat, row.lon], radius=1, color='darkblue',
    #        fill_color='darkblue', fill=True, fill_opacity=1).add_to(folium_map)
    CircleMarker(location=[row.lat, row.lon],
                 radius=row.pp,
                 stroke=True,
                 weight=0.75,
                 color='black',
                 fill_color=colormap(row.pp), fill=True,
                 fill_opacity=0.8,
                 popup=popup).add_to(group1)

for idx, row in df_map[df_map.grupo == 'EMA'].iterrows():
    # color = colormap.scale(row.pp)
    popup = folium.Popup(
        f"<b>Alias:</b> {row.alias} <br> <b>Precipitación:</b> {row.pp} [mm] <br> <b>Grupo:</b> {row.grupo} <br>", max_width=1000)
    # Circle(location=[row.lat, row.lon], radius=1, color='darkblue',
    #        fill_color='darkblue', fill=True, fill_opacity=1).add_to(folium_map)
    CircleMarker(location=[row.lat, row.lon],
                 radius=row.pp,
                 stroke=True,
                 weight=0.75,
                 color='red',
                 fill_color=colormap(row.pp), fill=True,
                 fill_opacity=0.8,
                 popup=popup).add_to(group2)

folium_map.add_child(group1)
folium_map.add_child(group2)
folium_map.add_child(folium.map.LayerControl(position='bottomleft'))


st_map = st_folium(folium_map,
                   width=streamlit_js_eval(
                       js_expressions='window.innerWidth', key='lwidth'),
                   height=600)
