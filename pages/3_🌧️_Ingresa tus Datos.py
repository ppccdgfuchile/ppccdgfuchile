from params import *
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
import sys
# import locale
sys.path.append('../.')

# Use Spanish Locale
# locale.setlocale(locale.LC_TIME, 'es_ES')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

events = sorted(os.listdir(f".{path_sep}eventos"))
events_names = [datetime.strptime(e.split(".")[0], "%Y-%m-%d").strftime("%Y/%B/%d")
                for e in events]


def check_valid_email(email):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    usuarios = pd.read_csv(
        f".{path_sep}usuarios{path_sep}usuarios.csv", index_col='index')
    lista_mails = usuarios.mail.to_list()
    if re.match(pat, email):
        if email in lista_mails:
            return True
        else:
            st.error("El correo no se encuentra registrado")
            return False
    else:
        st.error("El correo no es válido")
        return False


def check_valid_precipitation(precipitation):
    if precipitation < 0:
        st.error("El valor de precipitación no puede ser negativo")
        return False
    elif not (isinstance(precipitation, int) or isinstance(precipitation, float)):
        st.error("El valor de precipitación debe ser un número")
        return False
    return True


def submit_information(email, event, precipitation):
    if not check_valid_email(email):
        return None
    elif not check_valid_precipitation(precipitation):
        return None
    else:
        # Read event csv
        df = pd.read_csv(
            f".{path_sep}eventos{path_sep}{events[events_names.index(event)]}")

        df.loc[df.mail == email, 'pp'] = precipitation

        # Save data
        df.to_csv(
            f".{path_sep}eventos{path_sep}{events[events_names.index(event)]}", index=False)

        st.success(f"Información registrada exitosamente!")
        st.success(f"Email: {email}")
        st.success(f"Precipitación: {precipitation}")
        return None


st.header('Ingresa tus Datos')

with st.form(key='my_form', border=False):
    email = st.text_input(label='Ingresa tu correo')
    event = st.selectbox(
        'Seleccione el evento del dato a registrar', events_names)
    precipitation = st.number_input(
        label='Ingresa la precipitación registrada en [mm]', min_value=0., max_value=300., step=0.1)
    submit_button = st.form_submit_button(label='Registrar información')

if submit_button:
    submit_information(email, event, precipitation)
