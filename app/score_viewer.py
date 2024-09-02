"""
  __author__ = Gabriella Silveira Braz
  __email__ = gabriella.braz@itau-unibanco.com.br
  __version__ = 0.0.1
  __pylintGrade__ = 9.70
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit_antd_components as sac
import streamlit_echarts as st_echarts
from loguru import logger
from streamlit.components.v1 import html
from streamlit_profiler import Profiler
from streamlit_extras.dataframe_explorer import dataframe_explorer


DIR_ROOT = str(Path(__file__).parent.parent)
sys.path.append(DIR_ROOT)

from app.src.utils.download_to_excel import create_pivot_table_with_multindex
from app.src.utils.merge_de_2_ou_3 import (
    merge_de_2_ou_3_bases_removendo_colunas_desnecessarias,
)
from app.src.utils.generate_html_table import generate_html_table
from app.src.data_class.data_class_score import (
    ScoreFarolMap,
    ScorePilarMap,
    ScoreTemaMap,
    Farol,
    Tema,
    Pilar,
)

# p = Profiler()
score_tema_map = ScoreTemaMap(
    tema_list=[
        Tema(
            nome_front="INFRA CIVIL",
            nome_etl="INFRA CIVIL",
            cor_background="#F8F9FB",
        ),
        Tema(
            nome_front="REGULATÓRIO",
            nome_etl="REGULATÓRIO",
            cor_background="#F8F9FB",
        ),
        Tema(
            nome_front="SEGURANÇA",
            nome_etl="SEGURANÇA",
            cor_background="#F8F9FB",
        ),
        Tema(
            nome_front="ESG",
            nome_etl="ESG",
            cor_background="#F8F9FB",
        ),
    ]
)

score_pilar_map = ScorePilarMap(
    pilar_list=[
        Pilar(
            nome_etl="EFICIÊNCIA",
            nome_front="EFICIÊNCIA",
            cor_background="#EFF2F6",
        ),
        Pilar(
            nome_etl="PERFORMANCE",
            nome_front="PERFORMANCE",
            cor_background="#EFF2F6",
        ),
        Pilar(
            nome_etl="RISCO",
            nome_front="RISCO",
            cor_background="#EFF2F6",
        ),
        Pilar(
            nome_etl="ESG",
            nome_front="ESG",
            cor_background="#EFF2F6",
        ),
    ]
)

score_farol_map = ScoreFarolMap(
    farol_list=[
        Farol(
            nome_etl="VERMELHO",
            nome_front="Agências críticas",
            cor_icone="red",
            icones="bi bi-x-circle-fill",
        ),
        Farol(
            nome_etl="AMARELO",
            nome_front="Agências medianas",
            cor_icone="#B68105",
            icones="bi bi-dash-circle-fill",
        ),
        Farol(
            nome_etl="VERDE",
            nome_front="Agências ótimas",
            cor_icone="green",
            icones="bi bi-check-circle-fill",
        ),
    ]
)


@st.experimental_dialog("SCORE FAROL", width="large")
def criar_grafico_echarts(
    df: pd.DataFrame,
    data_column: str,
    line_name_column: str,
    value_column: str,
    score_farol_map: ScoreFarolMap,
):

    # CONVERTE A COLUNA PARA DATETIME
    df[data_column] = pd.to_datetime(df[data_column])

    # FORMATA A DATA NO FORMATO "MÊS/ANO"
    df["DATA_FORMATTED"] = df[data_column].dt.strftime("%b/%y")

    # EXTRAI AS DATAS FORMATADAS COMO UMA LISTA --> EIXO X
    x_axis_data = df["DATA_FORMATTED"].unique().tolist()
    x_axis_data.sort(key=lambda date: datetime.strptime(date, "%b/%y"))

    # INICIALIZA LISTA PARA CONFIGS. DAS SÉRIES
    series = []

    # ITERA SOBRE OS FARÓIS DO SCOREFAROLMAP DATACLASS.
    for farol in score_farol_map.farol_list:
        # FILTRA OS DADOS DO DATAFRAME PARA OBTER OS VALORES ASSOCIADOS AO FAROL ATUAL.
        serie_data = df[df[line_name_column] == farol.nome_etl][value_column].tolist()

        # CRIA NOVA SÉRIE DO GRÁFICO
        series.append(
            {
                "name": farol.nome_front,  # DEFINE O NOME DA SÉRIE PARA EXIBIÇÃO NA LEGENDA
                "type": "line",  # ESPECIFICA QUE A SÉRIE SERÁ UMA LINHA
                "data": serie_data,  # ATRIBUI OS DADOS DA SÉRIE (VALORES DO FAROL)
                "itemStyle": {"color": farol.cor_icone},  # DEFINE A COR DA LINHA
                "lineStyle": {
                    "width": 2,
                    "color": farol.cor_icone,
                },  # FORMATA A LARGURA E A COR DA LINHA
                "label": {
                    # "show": True,
                    "position": "top",
                    "color": farol.cor_fonte,
                },  # ADICIONA LABEL
                "smooth": False,  # DEFINE SE A LINHA DEVE SER CURVAS OU LINEAR.
            }
        )

    # CONFIGURAÇÕES GERAIS DO GRÁFICO
    option = {
        "tooltip": {"trigger": "axis"},  # CONFIGURA O TOOLTIP --> MOUSE SOBRE O EIXO
        "legend": {
            "data": [farol.nome_front for farol in score_farol_map.farol_list]
        },  # DEFINE OS NOMES DAS SÉRIES NA LEGENDA
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True,
        },  # AJUSTA AS MARGENS DO GRÁFICO
        "toolbox": {"feature": {"saveAsImage": {}}},
        "xAxis": {
            "type": "category",  # TIPO DO EIXO X == CATEGÓRICO (DATAS)
            "data": x_axis_data,  # VALORES DO EIXO X
        },
        "yAxis": {"type": "value"},  # TIPO DO EIXO Y == VALORES NUMÉRICO
        "series": series,  # ADICIONA AS SÉRIES AO GRÁFICO
        "dataZoom": [
            {
                "start": 100
                * (
                    (len(x_axis_data) - 12) / len(x_axis_data)
                ),  # ADICIONA A BARRA DE ZOOM NA PARTE INFERIOR DO GRÁFICO.
                "end": 100,  # CALCULA O FIM DO ZOOM PARA A BARRA.
            },
        ],
    }

    st_echarts.st_echarts(options=option)


def get_columns_agencia_info_selected(
    multiselect_label: str,
    multiselect_options: list,
    multiselect_default: list,
    columns_to_drop: list,
    index_name: str,
):
    """
    FILTRA E RETORNA AS COLUNAS SELECIONADAS PELO USUÁRIO EM UM MULTISELECT,
    EXCLUINDO COLUNAS ESPECIFICADAS E GARANTINDO QUE O ÍNDICE SEMPRE SEJA INCLUÍDO.

    ARGUMENTOS:
        multiselect_label (str): O RÓTULO A SER EXIBIDO NO MULTISELECT.
        multiselect_options (list): A LISTA DE OPÇÕES DISPONÍVEIS NO MULTISELECT.
        multiselect_default (list): A LISTA DE OPÇÕES PRESELECIONADAS NO MULTISELECT.
        columns_to_drop (list): A LISTA DE COLUNAS QUE DEVEM SER EXCLUÍDAS DAS OPÇÕES.
        index_name (str): O NOME DA COLUNA DE ÍNDICE QUE DEVE SER SEMPRE INCLUÍDA NA SELEÇÃO FINAL.

    RETORNA:
        list: A LISTA DE COLUNAS SELECIONADAS PELO USUÁRIO, SEM AS COLUNAS EXCLUÍDAS E
        GARANTINDO QUE O ÍNDICE SEJA INCLUÍDO. SE NENHUMA COLUNA FOR SELECIONADA, RETORNA APENAS O ÍNDICE.
    """
    # FILTRA AS OPÇÕES DO MULTISELECT, EXCLUINDO AS COLUNAS A SEREM REMOVIDAS E O ÍNDICE
    filtered_multiselect_options = [
        col for col in multiselect_options if col not in [index_name] + columns_to_drop
    ]
    # FILTRA AS OPÇÕES PRESELECIONADAS, MANTENDO APENAS AQUELAS QUE ESTÃO NAS OPÇÕES FILTRADAS
    filtered_multiselect_default = [
        col for col in multiselect_default if col in filtered_multiselect_options
    ]
    # CRIA O MULTISELECT COM AS OPÇÕES FILTRADAS E AS OPÇÕES PRESELECIONADAS
    colunas_info_agencia_table_selected = st.multiselect(
        label=multiselect_label,
        options=filtered_multiselect_options,
        default=filtered_multiselect_default,
    )
    # RETORNA O ÍNDICE MAIS AS COLUNAS SELECIONADAS PELO USUÁRIO,
    # OU SOMENTE O ÍNDICE SE NENHUMA COLUNA FOR SELECIONADA
    if not colunas_info_agencia_table_selected:
        return [index_name]
    return [index_name] + colunas_info_agencia_table_selected


@st.experimental_fragment
def container_tabela_farois(
    df_explorer_output,
    df_score_pilar,
    df_score_tema,
    df_score_global,
    score_farol_map,
    columns_to_drop,
):

    # MULTISELECT DAS COLUNAS INFO VISÍVEIS
    colunas_table_selected = get_columns_agencia_info_selected(
        multiselect_label="Selecione as colunas desejadas",
        multiselect_options=df_explorer_output.columns,
        multiselect_default=["UF", "MUNICIPIO"],
        columns_to_drop=columns_to_drop,
        index_name="CD_PONTO",
    )

    # MULTISELEC DOS PILARES VISÍVEIS
    score_pilar_selected = st.multiselect(
        "Selecione o pilar desejado", options=columns_to_drop, default=columns_to_drop
    )

    df_score_pilar["TEMA_PILAR"] = "SCORE PILAR"
    df_score_pilar = df_score_pilar.rename(
        columns={
            "AGENCIA_PILAR": "AGENCIA",
            "PILAR_PILAR": "PILAR",
            "TEMA_PILAR": "TEMA",
            "SCORE_PILAR": "SCORE",
            "FAROL_PILAR": "FAROL",
        }
    )
    df_score_tema = df_score_tema.rename(
        columns={
            "AGENCIA_TEMA": "AGENCIA",
            "TEMA_TEMA": "TEMA",
            "PILAR_TEMA": "PILAR",
            "SCORE_TEMA": "SCORE",
            "FAROL_TEMA": "FAROL",
        }
    )
    df_score_global["PILAR_GLOBAL"] = "GLOBAL"
    df_score_global["TEMA_GLOBAL"] = "GLOBAL"
    df_score_global = df_score_global.rename(
        columns={
            "AGENCIA_GLOBAL": "AGENCIA",
            "PILAR_GLOBAL": "PILAR",
            "TEMA_GLOBAL": "TEMA",
            "SCORE_GLOBAL": "SCORE",
            "FAROL_GLOBAL": "FAROL",
        }
    )

    # CONCATENA OS DFS DE SCORE PILAR, TEMA E GLOBAL
    df_concat_pilar_tema_global = pd.concat(
        [df_score_pilar, df_score_tema, df_score_global], axis=0
    )

    # ORDENA O DF CONCATENADO PELA COLUNA "AGENCIA"
    df_concat_pilar_tema_global.sort_values("AGENCIA", inplace=True)

    # MERGE ENTRE O DF CONCATENADO (PILAR, TEMA E GLOBAL) E O df_explorer_output PARA
    # OBTENÇÃO DE COLUNAS DE INFORMAÇÃO (MULTISELECT)
    df_tabela_farol_pivot = df_concat_pilar_tema_global.merge(
        df_explorer_output, right_on="CD_PONTO", left_on="AGENCIA", how="inner"
    )

    # PIVOT DO DF PARA CONSTRUÇÃO DA TABELA HTML
    df_tabela_farol = create_pivot_table_with_multindex(
        dataframe=df_tabela_farol_pivot,
        index=colunas_table_selected,
        columns=["PILAR", "TEMA"],
        values="SCORE",
    )

    with st.spinner("Carregando base..."):
        # GERA A TABELA HTML DOS FARÓIS SCORE
        html(
            generate_html_table(
                dataframe=df_tabela_farol,
                df_combined=df_concat_pilar_tema_global,
                score_farol_map=score_farol_map,
                index_columns=colunas_table_selected,
                score_pilar_selected=score_pilar_selected,
                rows_per_page=2,
            ),
            height=460,
            scrolling=True,
        )

    # CALCULA A QTD. DAS AGÊNCIAS SELECIONADAS
    qtd_agencias_selected = df_explorer_output["CD_PONTO"].nunique()

    # ESCREVE NA TELA A QUANTIDADE DE AGÊNCIA SELECIONADAS
    st.write(
        f"Quantidade de agências selecionadas: \
      {qtd_agencias_selected}"
    )


def plot_dataframe(data):
    filtered_df = dataframe_explorer(data, case=False)
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    return filtered_df, None


def main_page_score(user_configs):

    df_base_unica = pd.read_excel("app/src/data/df_base_unica.xlsx")
    df_score_tema = pd.read_csv("app/src/data/df_base_score_tema.csv")
    df_score_pilar = pd.read_csv("app/src/data/df_base_score_pilar.csv")
    df_score_global = pd.read_csv("app/src/data/df_base_score_global.csv")
    df_score_farol_intervalo = pd.read_excel(
        "app/src/data/df_intervalo_score_farol.xlsx"
    )

    with st.container(border=True):

        df_score_pilar_dataframe_explorer = create_pivot_table_with_multindex(
            dataframe=df_score_pilar,
            index=[
                "AGENCIA_PILAR",
            ],
            columns=["PILAR_PILAR"],
            values="SCORE_PILAR",
        )

        # FAZ O MERGE ENTRE AS BASES DO SCORE PILARES E TEMAS E BASE ÚNICA
        df_base_unica_score = merge_de_2_ou_3_bases_removendo_colunas_desnecessarias(
            dataframe_1=df_base_unica,
            dataframe_2=df_score_pilar_dataframe_explorer,
            dataframe_3=df_score_global,
            merge_column_dataframe_1="CD_PONTO",
            merge_column_dataframe_2="AGENCIA_PILAR",
            merge_column_dataframe_3="AGENCIA_GLOBAL",
            list_columns_to_drop=["AGENCIA_GLOBAL"],
        )

        # PLOTANDO O DATAFRAME
        selected_df, _ = plot_dataframe(data=df_base_unica_score)

        # CÓPIA DO DATAFRAME RESULTANTE DO DATAFRAME EXPLORER
        df_explorer_output = selected_df.copy()

        # CRIAÇÃO DE COLUNAS STREAMLIT PARA GRID DA PÁGINA
        col_download_base = st.columns([3, 3, 3], vertical_alignment="center")

        with col_download_base[0]:
            # DISPONDO A QUANTIDADE DE DADOS SELECIONADOS
            tamanho_selected_df = len(df_explorer_output)
            gramatica_qtd_pontos = "ponto" if len(df_explorer_output) == 1 else "pontos"
            st.text(f"{tamanho_selected_df} {gramatica_qtd_pontos} selecionados")

    if not df_explorer_output.empty:

        # CRIAÇÃO DE TABS PARA SEÇÃO 2
        tabs_secao_2 = sac.tabs(
            [
                sac.TabsItem(
                    label="Tabela",
                    icon="table",
                ),
                sac.TabsItem(
                    label="Gráfico",
                    icon="chart",
                    disabled=True,
                ),
            ],
            align="center",
            variant="outline",
            color="orange",
            use_container_width=True,
        )

        with st.container(border=True):

            # VISGRÁFICO E TABELA RANKING
            if tabs_secao_2 == "Gráfico":
                pass

            else:
                container_tabela_farois(
                    df_explorer_output=df_explorer_output,
                    df_score_pilar=df_score_pilar,
                    df_score_tema=df_score_tema,
                    df_score_global=df_score_global,
                    score_farol_map=score_farol_map,
                    columns_to_drop=list(
                        df_score_pilar_dataframe_explorer.columns.values
                    ),
                )

    else:
        st.info("Selecione filtros da tabela para a visualização completa da página")


main_page_score({})
