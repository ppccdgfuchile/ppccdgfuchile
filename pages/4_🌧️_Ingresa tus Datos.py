import streamlit as st
import pandas as pd
import locale
from datetime import datetime
import os

# Use Spanish Locale
locale.setlocale(locale.LC_TIME, 'es_ES')
st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

events = sorted(os.listdir(".\eventos"))
events_names = [datetime.strptime(e.split(".")[0], "%Y-%m-%d").strftime("%Y/%B/%d") for e in events]

def check_valid_email(email):
	return

def check_valid_precipitation(precipitation):
	return

def submit_information(email, event, precipitation):
	if not check_valid_email(email):
		return st.error("E-mail no válido")
	if not check_valid_precipitation(precipitation):
		return st.error("Valor de precipitación no válida")
	
	return st.success(f"Información registrada exitosamente!")

st.header('Ingresa tus Datos')

with st.form(key='my_form', border=False):
	email = st.text_input(label='Ingresa tu email')
	event = st.selectbox('Seleccione el evento del dato a registrar', events_names)
	precipitation = st.number_input(label='Ingresa la precipitación registrada en [mm]')
	submit_button = st.form_submit_button(label='Registrar información')

	if submit_button:
		submit_information(email, event, precipitation)
		