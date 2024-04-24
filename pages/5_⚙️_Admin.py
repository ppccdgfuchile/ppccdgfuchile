import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from params import *
import sys
import os
import locale
from datetime import datetime
import time
sys.path.append('../.')

st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

with open(f'.{path_sep}admins.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

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
    authenticator.logout("Logout", "sidebar")
    st.header("Página de Administración")

    st.divider()

    with st.expander("Añadir nuevo evento"):
        d = st.date_input("Fecha del evento")
        if st.button('Añadir'):
            df = pd.read_csv(f".{path_sep}usuarios{path_sep}usuarios.csv")
            df['pp'] = np.nan
            df.to_csv(f".{path_sep}eventos{path_sep}{d.strftime('%Y-%m-%d')}.csv", index=False)
            st.success(f"{d.strftime('%Y-%m-%d')}.csv ha sido creado!")

    with st.expander("Eliminar evento"):
        events = sorted(os.listdir(f".{path_sep}eventos"))
        events_names = [datetime.strptime(e.split(".")[0], "%Y-%m-%d").strftime("%Y/%B/%d")
                        for e in events]
        target_event = st.selectbox(
            'Seleccione el evento a eliminar', events_names)
        if st.button("Eliminar"):
            os.remove(f".{path_sep}eventos{path_sep}{events[events_names.index(target_event)]}")
            st.warning(f"{events[events_names.index(target_event)]} ha sido eliminado de la base de datos")
            with st.spinner('Actualizando...'):
                time.sleep(3)
            st.rerun()

    with st.expander("Administrar usuarios"):
        usuarios = pd.read_csv(f".{path_sep}usuarios{path_sep}usuarios.csv", index_col='index')

        def update_df():
            usuarios_edited.reset_index(inplace=True)
            usuarios_edited.to_csv(f".{path_sep}usuarios{path_sep}usuarios.csv")

        update_button = st.button("Update", on_click=update_df)
        usuarios_edited = st.data_editor(usuarios, use_container_width=True, num_rows="dynamic")

