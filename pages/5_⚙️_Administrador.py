import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
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

with open(f'.{path_sep}admins.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

stauth.Hasher.hash_passwords(config['credentials'])
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

    with st.expander("Usuarios registrados", expanded=True):
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

    with st.expander("Ver datos de evento", expanded=False):
        events = sorted(os.listdir(f".{path_sep}eventos"))
        events_names = [datetime.strptime(e.split(".")[0], "%Y-%m-%d").strftime("%Y/%m/%d")
                        for e in events]
        event = st.selectbox(
            'Seleccione evento', events_names, key='verdatos')

        data = pd.read_csv(
            f".{path_sep}eventos{path_sep}{events[events_names.index(event)]}", index_col='index')

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
        d = st.date_input("Fecha del evento a añadir:")
        sheet = st.file_uploader('Cargar planilla de registros...')
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

            if st.button("Agregar a la base de datos"):
                try:
                    data.to_csv(f'eventos/{d.strftime('%Y-%m-%d')}.csv')
                    st.success(f"Evento del {d.strftime(
                        '%Y-%m-%d')} ha sido creado!")
                except Exception as e:
                    st.warning(f'No se pudo crear el evento {
                               d.strftime('%Y-%m-%d')}!')
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
        events_names = [datetime.strptime(e.split(".")[0], "%Y-%m-%d").strftime("%Y/%m/%d")
                        for e in events]
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
