from params import *
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
import sys
import time
# import locale
sys.path.append('../.')

# Use Spanish Locale
# locale.setlocale(locale.LC_TIME, 'es_ES')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

st.sidebar.image(f"static{path_sep}logo_ppcc.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_dgf.png", use_column_width=True)
st.sidebar.image(f"static{path_sep}logo_cr2.png", use_column_width=True)


def check_valid_email(email):
    usuarios = pd.read_csv(
        f".{path_sep}usuarios{path_sep}usuarios.csv", index_col='index')
    lista_mails = usuarios.mail.to_list()
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pat, email):
        if email in lista_mails:
            st.error("El correo ya se encuentra registrado")
            return False
        else:
            return True
    else:
        st.error("El correo no es válido")
        return False


def check_nombre(nombre):
    pat = r'[a-zA-Zñáéíóú\s]+$'
    if re.match(pat, nombre):
        return True
    else:
        st.error("El nombre no es válido (Ej: Juan Ramírez)")
        return False


def check_comuna(comuna):
    pat = r'[a-zA-Zñáéíóú\s]+$'
    if re.match(pat, comuna):
        return True
    else:
        st.error("El nombre de la comuna no es válido (Ej: San Miguel)")
        return False


def check_alias(alias):
    pat = r'^[a-zA-Z0-9]+$'
    if re.match(pat, alias):
        return True
    else:
        st.error(
            "El alias no es válido (Debe ser una palabra solo con letras y números, sin tildes)")
        return False


def register_user(nombre, mail, comuna, alias, latitud, longitud):
    if not check_valid_email(mail):
        return None
    elif not check_nombre(nombre):
        return None
    elif not check_comuna(comuna):
        return None
    elif not check_alias(alias):
        return None
    else:
        usuarios = pd.read_csv(
            f".{path_sep}usuarios{path_sep}usuarios.csv", index_col='index')
        usuarios.loc[len(usuarios.index)] = [nombre, mail,
                                             comuna, latitud, longitud, alias, '']
        usuarios.to_csv(f".{path_sep}usuarios{path_sep}usuarios.csv")
        st.success("Usuario registrado!")


with st.form(key='my_form', border=False):
    nombre = st.text_input(label='Nombre').rstrip()
    mail = st.text_input(label='Correo').rstrip()
    comuna = st.text_input(label='Comuna').rstrip()
    alias = st.text_input(label='Alias').rstrip()
    # grupo = st.text_input(label='Grupo')

    st.divider()

    with st.expander("¿Cómo obtener la latitud y longitud de tu ubicación?"):
        # st.write('Video')
        st.video(f'static{path_sep}googlemaps_ubicacion.mp4')

    latitud = st.number_input(
        label='Ingresa tu latitud en grados', min_value=-90., max_value=90., step=0.00001)
    longitud = st.number_input(
        label='Ingresa tu longitud en grados', min_value=-90., max_value=90., step=0.00001)
    submit_button = st.form_submit_button(label='Registrar información')

if submit_button:
    register_user(nombre, mail, comuna, alias, latitud, longitud)
