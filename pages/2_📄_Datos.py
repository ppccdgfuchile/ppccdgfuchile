import streamlit as st
import pandas as pd


st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

df = pd.read_csv('.\eventos\data_test.csv', sep=';')

st.header('Datos')
st.dataframe(df, height=600, hide_index=True)
