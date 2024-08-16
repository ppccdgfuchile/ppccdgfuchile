import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import yaml
from yaml.loader import SafeLoader
from params import *
import sys
import os
# import locale
from datetime import datetime
import time
sys.path.append('../.')

st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")
st.sidebar.image(f"static{path_sep}logo_ppcc.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_dgf.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_cr2.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_uoh.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_uvalpo.png", use_column_width=True)


with open(f'.{path_sep}admins.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

Hasher.hash_passwords(config['credentials'])
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

name, authentication_status, user = authenticator.login()

if authentication_status == False:
    st.error("Usuario o contraseña incorrectos!")

if authentication_status:
    st.header("Página de Administración")
    st.divider()

    with st.expander("Usuarios registrados", expanded=False):
        data = pd.read_csv(
            f".{path_sep}usuarios{path_sep}usuarios.csv",
            index_col='index')

        def update_data():
            st.success('Actualización exitosa!')
            data_edited.reset_index(inplace=True, drop=True)
            data_edited.index.name = 'index'
            data_edited.to_csv(
                f".{path_sep}usuarios{path_sep}usuarios.csv")

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
                # st.success(f"{fname} ha sido creado!")
            elif fname.split('.')[-1] in ['xls', 'xlsx']:
                data = pd.read_excel(sheet)
                # st.success(f"{fname} ha sido creado!")
            else:
                st.error(f'{fname} debe ser una planilla excel o csv!')

            if st.button("Actualizar registro de usuarios"):
                try:
                    data['lat'] = data['lat'].map(
                        lambda s: float(str(s).replace(',', '.')))
                    data['lon'] = data['lon'].map(
                        lambda s: float(str(s).replace(',', '.')))
                    data.to_csv(f'usuarios{path_sep}usuarios.csv')
                    st.success(f'Archivo {path_sep}usuarios.csv creado !')
                    st.rerun()
                except Exception as e:
                    st.warning(f'No se pudo crear el archivo !')
                    st.error(f'Error: {e}')
    with st.expander("Configurar visualizacion", expanded=False):
        visparams = pd.read_csv(
            f'visparams{path_sep}visparams.csv', index_col=0)

        def update_visparams():
            # index = visparams_edited.index
            # visparams_edited.reset_index(inplace=True, drop=True)
            # visparams_edited.index.name = 'eventos'
            visparams_edited.to_csv(
                f".{path_sep}visparams{path_sep}visparams.csv")

        update_visparams = st.button(
            "Actualizar", on_click=update_visparams, key='visparams_update')
        visparams_edited = st.data_editor(
            visparams, use_container_width=True, num_rows='dynamic',
            key='visparams_edit')

    with st.expander("Ver datos de evento", expanded=False):
        events = sorted(os.listdir(f".{path_sep}eventos"))
        events_names = sorted([e.split('.')[0].replace(
            '-', '/').replace('_', ' - ') for e in events], reverse=True)
        event = st.selectbox(
            'Seleccione evento', events_names, key='verdatos')

        data = pd.read_csv(
            f".{path_sep}eventos{path_sep}{events[events_names.index(event)]}",
            index_col=0)

        def update_data():
            data_edited.reset_index(inplace=True, drop=True)
            data_edited.index.name = 'index'
            data_edited.to_csv(
                f".{path_sep}eventos{path_sep}{events[events_names.index(event)]}")

        update_data = st.button(
            "Actualizar", on_click=update_data, key='data_update_event')
        data_edited = st.data_editor(
            data, use_container_width=True, num_rows='dynamic',
            key='data_edit_event')

    with st.expander("Añadir nuevo evento", expanded=False):
        d = st.date_input("Fecha del evento a añadir:",
                          (datetime.today(), datetime.today()))
        event_name = '_'.join([dd.strftime('%F') for dd in d])
        sheet = st.file_uploader('Cargar planilla de registros...')
        if sheet is not None:
            loaded_fname = sheet.name
            if loaded_fname.split('.')[-1] == 'csv':
                data = pd.read_csv(sheet)
                # st.success(f"{loaded_fname} ha sido creado!")
            elif loaded_fname.split('.')[-1] in ['xls', 'xlsx']:
                data = pd.read_excel(sheet)
                # st.success(f"{loaded_fname} ha sido creado!")
            else:
                st.error(f'{loaded_fname} debe ser una planilla excel o csv!')

            if st.button("Agregar a la base de datos"):
                try:
                    data['lat'] = data['lat'].map(
                        lambda s: float(str(s).replace(',', '.')))
                    data['lon'] = data['lon'].map(
                        lambda s: float(str(s).replace(',', '.')))

                    data.to_csv(f'eventos/{event_name}.csv')

                    visparams = pd.read_csv('visparams/visparams.csv',
                                            index_col=0)
                    visparams.loc[event_name] = np.nan
                    visparams.to_csv('visparams/visparams.csv')

                    st.success(f"Evento del {event_name.replace(
                        '-', '/').replace('_', ' - ')} ha sido creado!")
                except Exception as e:
                    st.warning(f'No se pudo crear el evento {
                               event_name}!')
                    st.error(f'Error: {e}')

                # st.rerun()
                #
                # if st.button('Añadir'):
                #     df = pd.read_csv(f".{path_sep}usuarios{path_sep}usuarios.csv")
                #     df['pp'] = np.nan
                #     df.to_csv(
                #         f".{path_sep}eventos{path_sep}{d.strftime('%Y-%m-%d')}.csv", index=False)
                #     st.success(f"{d.strftime('%Y-%m-%d')}.csv ha sido creado!")
                #     st.rerun()

    with st.expander("Eliminar evento", expanded=False):
        events = sorted(os.listdir(f".{path_sep}eventos"))
        events_names = sorted([e.split('.')[0].replace(
            '-', '/').replace('_', ' - ') for e in events], reverse=True)
        target_event = st.selectbox(
            'Seleccione el evento a eliminar', events_names, key='eliminarevento')
        if st.button("Eliminar"):
            os.remove(
                f".{path_sep}eventos{path_sep}{events[events_names.index(target_event)]}")
            st.warning(
                f"{events[events_names.index(target_event)]} ha sido eliminado de la base de datos")
            with st.spinner('Actualizando...'):
                time.sleep(3)
            st.rerun()

    authenticator.logout('Logout')

    # with st.expander("Administrar usuarios"):
    #     usuarios = pd.read_csv(
    #         f".{path_sep}usuarios{path_sep}usuarios.csv", index_col='index')

    #     def update_df():
    #         usuarios_edited.reset_index(inplace=True, drop=True)
    #         usuarios_edited.index.name = 'index'
    #         usuarios_edited.to_csv(
    #             f".{path_sep}usuarios{path_sep}usuarios.csv")

    #     update_button = st.button(
    #         "Update", on_click=update_df, key='usuarios_edited')
    #     usuarios_edited = st.data_editor(
    #         usuarios, use_container_width=True, num_rows="dynamic")
