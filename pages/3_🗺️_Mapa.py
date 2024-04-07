import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")

df = pd.read_csv('data_test.csv', sep=';')
df_map = df[['lat', 'lon', 'pp']].astype('float64')

df_map.drop(77, inplace=True)
df_map.drop(118, inplace=True)

df_map.dropna(inplace=True)
df_map['pp'] = df_map['pp']*100

st.header('Mapa')
st.map(df_map, latitude='lat', longitude='lon', size='pp')
