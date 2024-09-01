"""
  __author__ = Gabriella Silveira Braz
  __email__ = gabriella.braz@itau-unibanco.com.br
  __version__ = 0.0.1
  __pylintGrade__ = 10
"""

import sys
from pathlib import Path

import streamlit as st
from streamlit_echarts import st_echarts

DIR_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(DIR_ROOT)


def create_radar_chart(
    temas_unique: list,
    agencias_values: dict,
    color_map_layers: dict,
    layers_legend_values: dict,
):
    """FUNÇÃO RESPONSÁVEL POR CRIAR O RADAR CHART UTILIZANDO ECHARTS

    Args:
      temas_unique (list): LISTA DE TEMAS ÚNICOS DISPONÍVEIS NO MOMENTO DO SCORE
      agencias_values (dict): DICIONÁRIO COM OS VALORES DAS AGÊNCIAS
        ex.: "UF": {
            "INFRA": "7.7",
            "SEGURANCA": "5.8",
            "REGULATÓRIO": "3.9",
          },
      color_map_layers (dict): DICIONÁRIO COM O MAPA DE CORES PARA AS LAYERS
        ex.: "UF": {
            "cor_area": "rgba(17, 66, 228, 0.6)",
            "cor_borda": "rgba(17, 66, 228, 1)",
            "cor_legenda": "rgba(17, 66, 228, 0.5)",
          },
      layers_legend_values (dict): DICT DO NOME DA LAYER E SEU APELIDO.

    Returns:
      dict: CONFIGURAÇÕES DO GRÁFICO RADAR
    """

    # CRIA A LISTA DE INDICADORES PARA O GRÁFICO RADAR COM O NOME
    # E VALOR MÁXIMO PARA CADA TEMA
    indicator_value = [
        {"name": name.title(), "max": 11, "textStyle": {"fontSize": 14}}
        for name in temas_unique
    ]

    # CRIA A LISTA DE VALORES (DICTS) DA SÉRIE PARA CADA LAYER DO GRÁFICO
    series_values = []
    for layer, apelido_layer in layers_legend_values.items():  # PARA CADA LAYER...
        # OBTEM CORES PARA A LAYER ESPECIFICADA
        color_layer = color_map_layers.get(layer, {})

        # CRIA O DICT COM CONFIGURAÇÕES E VALORES DA LAYER
        dict_series = {
            "name": apelido_layer,  # NOME DA LAYER NA LEGENDA
            "type": "radar",  # TIPO DO GRÁFICO
            "symbolSize": 1,
            "label": {
                "color": "#696969",
                "fontWeight": "bold",
                "backgroundColor": "white",
                "borderRadius": 3,
                "padding": [3, 5],
                "fontSize": 15,
                "show": True,
            },
            "areaStyle": {  # DEFINE A COR DA ÁREA COLORIDA
                "color": color_layer.get("cor_area", "rgba(0, 0, 0, 0.5)")
            },
            "lineStyle": {  # DEFINE A COR DA BORDA DA ÁREA COLORIDA
                "color": color_layer.get("cor_borda", "rgba(0, 0, 0, 1)"),
                "type": "dashed",
                "width": 1,
                "opacity": 0.5,
            },
            "itemStyle": {
                "color": color_layer.get(
                    "cor_legenda", "rgba(0, 0, 0, 0.5)"
                )  # DEFINE A COR DA LEGENDA
            },
        }
        # INICIALIZAÇÃO DA LISTA QUE CONTERÁ OS VALORES (float) DO GRÁFICO
        data_values = []

        for tema in temas_unique:  # PARA CADA TEMA...
            # ADICIONA OS VALORES DE CADA TEMA EM UMA LISTA
            data_values.append(
                agencias_values.get(layer).get("SCORE_LAYER").get(tema, 0)
            )

        # UPDATE DO DICIONÁRIO DE CONFIGURAÇÕES PARA ADIÇÃO DOS VALORES
        dict_series.update({"data": [data_values]})

        # UPDATE DO DICIONRIO COMPLETO DA LAYER
        series_values.append(dict_series)

    # RETORNA O DICIONÁRIO DE CONFIGURAÇÃO DO GRÁFICO INTEIRO
    return {
        "legend": {
            "bottom": -5,  # LOCALIZAÇÃO DA LEGENDA
            "data": list(layers_legend_values.values()),  # ELEMENTOS DA LEGENDA
            "itemGap": 15,  # ESPAÇAMENTO ENTRE CATEGORIAS DA LEGENDA
            "textStyle": {
                "color": "#000D3C",  # QUANDO LEGENDA SELECIONADA, FICA DESTA COR
                "fontSize": 10,
            },
            "icon": "roundRect",
            "selected": {"UF": False, "MUNICÍPIO": False, "FAROL": False},
            "selectedMode": "single",
        },
        "tooltip": {
            "trigger": "item",
        },
        "radar": {
            "indicator": indicator_value,
            "shape": "circle",  # DEFINE O FORMATO DO GRÁFICO
            "startAngle": 90,  # DEFINE ÂNGULO DE INÍCIO
            "splitNumber": 4,  # DEFINE O NÚMERO DE "RODAS" NO GRÁFICO
            "axisName": {  # DEFINE LABEL DAS CATEGORIAS NO GRÁFICO
                "color": "#1B1B1B",
                "fontWeight": "bold",
                "fontSize": 14,
            },
            "splitArea": {  # DEFINE O STYLE DO FUNDO "RODAS" DO GRÁFICO
                "areaStyle": {
                    "color": ["white", "#d5d5db4f", "white", "#d5d5db4f"],
                    "shadowColor": "rgba(0, 0, 0, 0.0)",
                    "shadowBlur": 0,
                }
            },
            "axisLine": {  # DEFINE O STYLE DOS EIXOS DE CADA CATEGORIA
                "lineStyle": {"color": "grey"}
            },
            "axisLabel": {
                "show": False,
                "fontSize": 15,
                "position": "bottom",
            },
        },
        "center": ["50%", "50%"],
        "series": series_values,
        "avoidLabelOverlap": True,
        "label": {"show": True, "position": "bottom", "fontSize": 13},
        "labelLine": {"show": True},
        "emphasis": {
            "lineStyle": {
                "width": 1,
            },
            "label": {
                "show": True,
                "fontSize": 14,
            },
        },
    }


def render_radar_chart(
    cd_ponto: int,
    score_geral_css: str,
    valores_radar_chart: dict,
    radar_chart_column: int,
    temas_visiveis: list,
    score_farol_map,
) -> None:
    """
    FUNÇÃO RESPONSÁVEL POR RENDERIZAR O RADAR CHART COM STYLED CSS

    Args:
      cd_ponto (int): NÚMERO DA AGÊNCIA QUE SERÁ RENDERIZADA
      score_geral_css (str): STRING DE CSS PARA ESTILO GERAL DO RADAR CHART
      valores_radar_chart (dict): DICIONÁRIO CONTENDO OS VALORES PARA O RADAR CHART
      radar_chart_column (int): COLUNA ONDE O RADAR CHART SERÁ RENDERIZADO
      temas_visiveis (list): LISTA DOS TEMAS QUE SERÃO RENDERIZADOS NO RADAR CHART
    """

    # RENDERIZA O CSS DO RADAR CHART
    st.markdown(
        f"""<style>{score_geral_css} \
      </style>\n<div class="agencia-name">AGÊNCIA \
      {cd_ponto}</div>""",
        unsafe_allow_html=True,
    )

    cores_radar_chart_layers = dict(
        settings.get("PAGE_SCORE_GERAL.CORES_RADAR_CHART_LAYERS")
    )

    # CRIA O RADAR CHART UTILIZANDO DICT DE VALORES
    radar_chart = create_radar_chart(
        temas_unique=temas_visiveis,
        agencias_values=valores_radar_chart[f"AGENCIA_{cd_ponto}"],
        color_map_layers=settings.get("PAGE_SCORE_GERAL.CORES_RADAR_CHART_LAYERS"),
        layers_legend_values={
            "CD_PONTO": f"AGÊNCIA {cd_ponto}",
            "UF": "UF",
            "MUNICIPIO": "MUNICÍPIO",
            "FAROL": "FAROL",
        },
    )

    # RENDERIZA O RADAR CHART
    st_echarts(radar_chart, key=f"radar_chart_{cd_ponto}_{radar_chart_column}")
