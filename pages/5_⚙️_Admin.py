import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

with open('.\\admins.yaml') as file:
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

    st.subheader("Añadir nuevo evento")
    d = st.date_input("Fecha del evento")
    if st.button('Añadir'):
        st.success(f"{d.strftime('%Y-%m-%d')}.csv ha sido creado!")
