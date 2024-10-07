import streamlit as st
import streamlit_antd_components as sac
import streamlit as st
import plotly.graph_objs as go
import plotly.io as pio
import base64
import numpy as np


class CardsScores:

    def __init__(
        self,
        titulo: str = "-",
        qtd_valor: int = 0,
        porcentagem: float = 0,
        serie_historica: dict = {},
        color: str = "grey",
    ):
        self.titulo = titulo
        self.qtd_valor = qtd_valor
        self.porcentagem = porcentagem
        self.serie_historica = serie_historica
        self.color = color
        self.card = None

    def render_html_card(self):
        html = f"""
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
        <div style='box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); display: flex; border-radius: 10px; height: 100%;'>
            <div style='border-left: 1rem solid {self.color}; border-top-left-radius: 10px; border-bottom-left-radius: 10px;'>
            </div>
            <div style='width: 100%;'>
                <div style='display: flex; width: 100%;'>
                    <div style='margin-left: 10px; width: 100%; display: flex; flex-direction: column;'>
                        <div style='width: 100%; padding-top: 8px; padding-bottom: 12px; color: #4D4D4D; font-weight: 400;'>{self.titulo.title()}</div>
                        <div style='display: flex; padding-bottom: 15px;'>
                            <div style='font-size: 25px; font-weight: 400; display: flex; align-items: center;'>
                                {str(self.qtd_valor)}
                            </div>
                            <div style='width: 1px; background-color: black; margin-left: 20px; margin-right: 20px; display: flex; align-items: center;'>
                            </div>
                            <div style='font-size: 20px; font-weight: 300; display: flex; align-items: center;'>
                                {str(self.porcentagem).replace(".", ",")}%
                            </div>
                        </div>
                    </div>
                    <div style='padding-top: 5px; padding-right: 8px;'>
                        <i class='bi bi-x-circle-fill' style='font-size: 1.3rem; color: {self.color};'></i>
                    </div>
                </div>
                <div style='width: 100%; margin-left: 10px; padding-bottom: 10px;'>{self.render_data_series_chart()}</div>
            </div>
        </div>
        """
        st.button("dw", key=f"{self.titulo}")
        st.markdown(html, unsafe_allow_html=True)
        return html

    def render_data_series_chart(self):
        meses = list(self.serie_historica.keys())
        valores = list(self.serie_historica.values())
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(x=meses, y=valores, mode="lines", line=dict(color=self.color))
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="white",
            height=20,
            width=250,
        )
        svg_bytes = pio.to_image(fig, format="svg")
        return svg_bytes.decode()


with st.sidebar:
    st.write(230)
col = st.columns([1, 1, 1])


with col[0]:
    CardsScores(
        titulo="Agências Críticas",
        qtd_valor=500,
        porcentagem=50,
        serie_historica={
            "jan": 100,
            "fev": 50,
            "mar": 80,
            "abr": 68,
            "mai": 78,
            "jun": 83,
            "jul": 85,
            "ago": 60,
            "set": 56,
            "out": 79,
            "nov": 67,
            "dez": 20,
        },
        color="red",
    ).render_html_card()
with col[1]:
    CardsScores(
        titulo="Agências Medianas",
        qtd_valor=300,
        porcentagem=30,
        serie_historica={
            "jan": 100,
            "fev": 10,
            "mar": 80,
            "abr": 68,
            "mai": 38,
            "jun": 83,
            "jul": 35,
            "ago": 60,
            "set": 26,
            "out": 79,
            "nov": 67,
            "dez": 60,
        },
        color="orange",
    ).render_html_card()
with col[2]:
    CardsScores(
        titulo="Agências boas",
        qtd_valor=200,
        porcentagem=20,
        serie_historica={
            "jan": 100,
            "fev": 90,
            "mar": 80,
            "abr": 68,
            "mai": 78,
            "jun": 83,
            "jul": 85,
            "ago": 60,
            "set": 56,
            "out": 79,
            "nov": 67,
            "dez": 100,
        },
        color="green",
    ).render_html_card()
