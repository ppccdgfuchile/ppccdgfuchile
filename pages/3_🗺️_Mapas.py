import os
import sys

import pandas as pd
import numpy as np

import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_folium import st_folium

import folium
import branca.colormap as cm
from folium import CircleMarker
from folium.plugins import StripePattern

from utils import recolectar_eventos, cargar_parametros_visualizacion


sys.path.append('../.')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")
st.sidebar.image("static/logo_ppcc.png", use_container_width=True)

df_eventos, n_eventos = recolectar_eventos()
if n_eventos != 0:
    eventos = df_eventos['Evento'].tolist()
    nombres = df_eventos['Nombre'].tolist()
else:
    st.warning('No hay eventos disponibles para mostrar.')
    st.stop()

target_event = st.selectbox('Seleccione el evento a visualizar', nombres)
target_event_name = target_event.replace(' - ', '_').replace('/', '-')

df = pd.read_csv(os.path.join('.', 'eventos', f'{target_event_name}.csv'),
                 index_col=0)
df_map = df[['Latitud', 'Longitud', 'Precipitacion']].astype('float64')
df_map['Alias'] = df['Alias']
df_map['Grupo'] = df['Grupo']
df_map.dropna(inplace=True)
st.header(f'Precipitaciones acumuladas: Evento {target_event}')


# ---------------------------------------------------------------------------- #
# Crear un mapa de Folium centrado en la ubicación de Santiago, Chile
# Establecer tiles en None para evitar sobrescribir capas personalizadas
folium_map = folium.Map(location=[-33.5, -70.8],
                        zoom_start=9,
                        tiles=None)


# Cargar parámetros de visualización
dvisparams = cargar_parametros_visualizacion('default')
visparams = cargar_parametros_visualizacion(target_event_name)
for key in visparams.keys():
    if isinstance(visparams.get(key), (float, int)):
        if np.isnan(visparams[key]):
            visparams[key] = dvisparams[key]
    elif isinstance(visparams.get(key), str) and visparams[key].lower() == 'nan':
        visparams[key] = dvisparams[key]

vmin = visparams['vmin']
vmax = visparams['vmax']
vstep = visparams['vstep']
escala_puntos = visparams['escala_puntos']
paletacolores = visparams['PaletaColores']
basemap = visparams['MapaFondo']
cmapticks = np.arange(vmin, vmax+vstep, vstep)

# Configurar mapa de colores
mapa_colores = eval(f"cm.linear.{paletacolores}").scale(vmin, vmax)
mapa_colores.caption = 'Precipitación acumulada (mm)'
mapa_colores.tick_labels = cmapticks.tolist()

# --------------------------------- BASEMAPS --------------------------------- #

google_maps_tile = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
    attr='Google Maps',
    name='Mapa',
    overlay=False,
    control=True
)

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

# Agregar capas base
tiles = [google_maps_tile, google_terrain_tile, google_satellite_tile]
if basemap == 'Satelite':
    google_maps_tile.add_to(folium_map)
    google_terrain_tile.add_to(folium_map)
    google_satellite_tile.add_to(folium_map)
elif basemap == 'Relieve':
    google_maps_tile.add_to(folium_map)
    google_satellite_tile.add_to(folium_map)
    google_terrain_tile.add_to(folium_map)
elif basemap == 'Mapa':
    google_terrain_tile.add_to(folium_map)
    google_satellite_tile.add_to(folium_map)
    google_maps_tile.add_to(folium_map)
else:
    text = [
        f'{basemap} no es un mapa base válido. Opciones válidas: ',
        'Mapa, Satelite, Relieve.'
    ]
    st.warning(''.join(text))

# ---------------------------------------------------------------------------- #
# Crear grupos de características
grupo1 = folium.FeatureGroup('Pluviómetros Ciudadanos')
grupo2 = folium.FeatureGroup('Pluviómetros Red Nacional')


# Plotear puntos

for idx, row in df_map[df_map.Grupo != 'EMA'].iterrows():
    text = [
        f"<b>Alias:</b> {row['Alias']} <br> "
        f"<b>Precipitación:</b> {row['Precipitacion']} [mm] <br> "
        f"<b>Grupo:</b> {row['Grupo']} <br>"
    ]
    popup = folium.Popup(' '.join(text), max_width=1000)
    CircleMarker(location=[row.Latitud, row.Longitud],
                 radius=row.Precipitacion/escala_puntos,
                 stroke=True,
                 weight=0.75,
                 color='black',
                 fill_color=mapa_colores(row.Precipitacion), fill=True,
                 fill_opacity=0.8,
                 popup=popup).add_to(grupo1)


for idx, row in df_map[df_map['Grupo'] == 'EMA'].iterrows():
    text = [
        f"<b>Alias:</b> {row['Alias']} <br> "
        f"<b>Precipitación:</b> {row['Precipitacion']} [mm] <br> "
        f"<b>Grupo:</b> {row['Grupo']} <br>"
    ]
    popup = folium.Popup(' '.join(text), max_width=1000)
    CircleMarker(location=[row['Latitud'], row['Longitud']],
                 radius=row.Precipitacion/escala_puntos,
                 stroke=True,
                 weight=0.75,
                 color='red',
                 fill_color=mapa_colores(row['Precipitacion']), fill=True,
                 fill_opacity=0.8,
                 popup=popup).add_to(grupo2)

folium_map.add_child(grupo1)
folium_map.add_child(grupo2)
folium_map.add_child(folium.map.LayerControl(position='bottomleft'))
mapa_colores.add_to(folium_map)
# CSS = "font-size: 16px; color: white; text-align: center;"  # add more props if needed
# folium_map.get_root().header.add_child(
#     folium.Element(f"<style>#legend > g > text.caption {{{CSS}}}</style>")
# )
map_width = streamlit_js_eval(js_expressions='window.innerWidth', key='lwidth')
st_map = st_folium(folium_map, width=map_width, height=600)
