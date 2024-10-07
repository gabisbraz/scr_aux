import pandas as pd
import folium
from folium.plugins import Draw, Fullscreen
from streamlit_folium import st_folium, folium_static
import geopandas
import json
import streamlit as st

import plotly.graph_objects as go
import os

from streamlit.components.v1 import html

gjj = None


# Função para gerar gráficos de barras para cada UF
@st.cache_resource
def gerar_grafico_uf(uf, esg, performance, riscos):
    fig = go.Figure(
        data=[
            go.Bar(name="ESG", x=["ESG"], y=[esg], marker_color="green"),
            go.Bar(
                name="PERFORMANCE",
                x=["PERFORMANCE"],
                y=[performance],
                marker_color="blue",
            ),
            go.Bar(name="RISCOS", x=["RISCOS"], y=[riscos], marker_color="red"),
        ]
    )

    # Layout
    fig.update_layout(
        title=f"Temas para {uf}",
        xaxis_title="Tema",
        yaxis_title="Score",
        barmode="group",
    )

    # Salvar gráfico como HTML
    gjj = fig.to_html(full_html=False)
    return gjj


@st.cache_resource
def dfa(opt):
    df_pivot = pd.read_excel("df.xlsx")

    if opt == "BR":
        # Caminho para o arquivo JSON
        file_path = "app/src/data/br_states.json"

        # Abrindo e lendo o arquivo JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        col = ["SIGLA", "Estado", "RISCOS", "PERFORMANCE", "ESG"]
        data = geopandas.GeoDataFrame.from_features(data, crs="EPSG:4326")
        data = pd.merge(data, df_pivot, left_on="SIGLA", right_on="UF")
        data = data[["geometry"] + col]
    else:
        # Caminho para o arquivo JSON
        file_path = "app/src/data/br_ba.json"

        # Abrindo e lendo o arquivo JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        col = ["name", "description"]
        data = geopandas.GeoDataFrame.from_features(data, crs="EPSG:4326")
        data = data[["geometry"] + col]

    return col, data


# INICIALIZA MAPA
opt = st.selectbox("Selecione o tipo", options=["BR", "Estados"])
col, data = dfa(opt)

map = folium.Map(location=[0, 0], zoom_start=2)

popup = folium.GeoJsonPopup(
    fields=col,
    aliases=col,
    localize=True,
    labels=True,
)

folium.GeoJson(
    data=data,  # ADICIONA GEOJSON AO MAPA - DEFINE ESTILO DE CADA REGIÃO
    zoom_on_click=True,  # MAPA DÁ ZOOM QUANDO REGIÃO É CLICADA
    name="Estados do Brasil",
    popup=popup,
).add_to(map)

# PLUGIN DE DESENHO NO MAPA
Draw().add_to(map)

# PLUGIN DE TELA CHEIA NO MAPA
Fullscreen(
    position="topright",
    title="Expandir",
    title_cancel="Fechar",
    force_separate_button=True,
).add_to(map)

# RENDERIZA O MAPA
x = st_folium(map, return_on_hover=False)

st.write(x)
