from params import *
import streamlit as st
import pandas as pd
import sys
sys.path.append('../')


st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

df = pd.read_csv(f'.{path_sep}data_test.csv', sep=',')

st.header('Datos')
st.dataframe(df, height=600, hide_index=True)
