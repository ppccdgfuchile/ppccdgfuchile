import os
import sys

import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader


import numpy as np
import pandas as pd

from datetime import datetime
import time
sys.path.append('../.')

st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")
st.sidebar.image(os.path.join("static", "logo_ppcc.png"),
                 use_container_width=True)

with open(os.path.join('.', 'admins.yaml')) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

try:
    login = authenticator.login()
except Exception as e:
    st.error(e)
    st.stop()

if st.session_state['authentication_status']:
    st.header("Página de Administración")
    st.divider()

    with st.expander("Usuarios registrados", expanded=False):
        df_path = os.path.join('.', 'usuarios', 'usuarios.csv')
        data = pd.read_csv(df_path, index_col='index')

        def update_data():
            st.success('Actualización exitosa!')
            data_edited.reset_index(inplace=True, drop=True)
            data_edited.index.name = 'index'
            data_edited.to_csv(df_path)

        update_data = st.button(
            "Actualizar", on_click=update_data, key='data_update_users')
        data_edited = st.data_editor(data, use_container_width=True,
                                     num_rows='dynamic', key='data_edit_users')

        sheet = st.file_uploader('Cargar planilla de usuarios...',
                                 key='users_update')
        if sheet is not None:
            fname = sheet.name
            if fname.split('.')[-1] == 'csv':
                data = pd.read_csv(sheet)
            elif fname.split('.')[-1] in ['xls', 'xlsx']:
                data = pd.read_excel(sheet)
            else:
                st.error(f'{fname} debe ser una planilla excel o csv!')

            if st.button("Actualizar registro de usuarios"):
                try:
                    data['lat'] = data['lat'].map(
                        lambda s: float(str(s).replace(',', '.')))
                    data['lon'] = data['lon'].map(
                        lambda s: float(str(s).replace(',', '.')))
                    data.to_csv(df_path)
                    st.success('Archivo usuarios.csv creado !')
                    st.rerun()
                except Exception as e:
                    st.warning('No se pudo crear el archivo !')
                    st.error(f'Error: {e}')
    with st.expander("Configurar visualizacion", expanded=False):
        visparams_path = os.path.join('visparams', 'visparams.csv')
        visparams = pd.read_csv(visparams_path, index_col=0)

        def update_visparams():
            visparams_edited.to_csv(visparams_path)

        update_visparams = st.button(
            "Actualizar", on_click=update_visparams, key='visparams_update')
        visparams_edited = st.data_editor(
            visparams, use_container_width=True,
            num_rows='dynamic',
            key='visparams_edit')

    with st.expander("Ver datos de evento", expanded=False):
        events = sorted(os.listdir('eventos'), reverse=True)
        events_names = [e.split('.')[0].replace('-', '/').replace('_', ' - ')
                        for e in events]
        event = st.selectbox('Seleccione evento', events_names, key='verdatos')
        event_df_path = os.path.join('.', 'eventos',
                                     f'{events[events_names.index(event)]}')
        data = pd.read_csv(event_df_path, index_col=0)

        def update_data():
            data_edited.reset_index(inplace=True, drop=True)
            data_edited.index.name = 'index'
            data_edited.to_csv(event_df_path)

        update_data = st.button("Actualizar", on_click=update_data,
                                key='data_update_event')
        data_edited = st.data_editor(data, use_container_width=True,
                                     num_rows='dynamic', key='data_edit_event')

    with st.expander("Añadir nuevo evento", expanded=False):
        d = st.date_input("Fecha del evento a añadir:",
                          (datetime.today(), datetime.today()))
        event_name = '_'.join([dd.strftime('%F') for dd in d])
        sheet = st.file_uploader('Cargar planilla de registros...')
        if sheet is not None:
            loaded_fname = sheet.name
            if loaded_fname.split('.')[-1] == 'csv':
                data = pd.read_csv(sheet)
            elif loaded_fname.split('.')[-1] in ['xls', 'xlsx']:
                data = pd.read_excel(sheet)
            else:
                st.error(f'{loaded_fname} debe ser una planilla excel o csv!')

            if st.button("Agregar a la base de datos"):
                try:
                    data['lat'] = data['lat'].map(
                        lambda s: float(str(s).replace(',', '.')))
                    data['lon'] = data['lon'].map(
                        lambda s: float(str(s).replace(',', '.')))

                    data.to_csv(os.path.join('eventos', f'{event_name}.csv'))
                    visparams_path = os.path.join('visparams', 'visparams.csv')
                    visparams = pd.read_csv(visparams_path, index_col=0)
                    visparams.loc[event_name] = np.nan
                    visparams.to_csv(visparams_path)

                    st.success(f"Evento del {event_name.replace(
                        '-', '/').replace('_', ' - ')} ha sido creado!")
                except Exception as e:
                    st.warning(f'No se pudo crear el evento {event_name}!')
                    st.error(f'Error: {e}')

    with st.expander("Eliminar evento", expanded=False):

        events = sorted(os.listdir('eventos'), reverse=True)
        events_names = [e.split('.')[0].replace('-', '/').replace('_', ' - ')
                        for e in events]
        target_event = st.selectbox('Seleccione el evento a eliminar',
                                    events_names, key='eliminarevento')
        if st.button("Eliminar"):
            os.remove(os.path.join('.', 'eventos',
                                   f'{events[events_names.index(target_event)]}'))
            st.warning(
                f"{events[events_names.index(target_event)]} ha sido eliminado de la base de datos")
            with st.spinner('Actualizando...'):
                time.sleep(3)
            st.rerun()

    authenticator.logout('Logout')
