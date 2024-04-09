import streamlit as st
import pandas as pd


st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

st.header('Ingresa tus Datos')

with st.form(key='my_form', border=False):
	text_input = st.text_input(label='Ingresa tu email')
	event = st.selectbox('Seleccione el evento del dato a registrar', ('2024/Junio/23', '2024/Agosto/08', '2024/Julio/14'))
	number_input = st.number_input(label='Ingresa la precipitación registrada en [mm]')
	submit_button = st.form_submit_button(label='Registrar información')