"""
  __author__ = Gabriella Silveira Braz
  __email__ = gabriella.braz@itau-unibanco.com.br
  __version__ = 0.0.1
  __pylintGrade__ = 9.88
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd
import streamlit as st
from loguru import logger

DIR_ROOT = str(Path(__file__).parent)
sys.path.append(DIR_ROOT)

from app.src.data_class.data_class_score import ScoreFarolMap


def rearranja_coluna_score_pilar(df):
    """
    REORGANIZA AS COLUNAS DE UM DATAFRAME DE ACORDO COM A PRIORIDADE
    DE COLUNAS GLOBAL E OUTRAS.

    ARGUMENTOS:
        df (pd.DataFrame): O DATAFRAME A SER REORGANIZADO. AS COLUNAS DEVEM
            SER MULTINÍVEL, ONDE O NÍVEL SUPERIOR REPRESENTA OS PILARES
            E O NÍVEL INFERIOR REPRESENTA OS TEMAS OU OUTROS ATRIBUTOS.

    RETORNA:
        pd.DataFrame: O DATAFRAME REINDEXADO COM AS COLUNAS REORDENADAS.
            AS COLUNAS DO TIPO "GLOBAL" SÃO MOVIDAS PARA O FIM DA LISTA
            DE COLUNAS, ENQUANTO AS OUTRAS COLUNAS PERMANECEM ANTES.
    """
    # LISTA PARA COLUNAS DO TIPO GLOBAL
    global_columns = []
    # LISTA PARA OUTRAS COLUNAS
    other_columns = []
    # ITERA SOBRE OS PILARES
    for pilar in df.columns.levels[0]:
        # OBTÉM AS COLUNAS DO PILAR
        pilar_columns = df[pilar].columns.tolist()
        # SE "SCORE PILAR" ESTIVER NAS COLUNAS
        if "SCORE PILAR" in pilar_columns:
            # REMOVE "SCORE PILAR" DAS COLUNAS
            pilar_columns.remove("SCORE PILAR")
            # REINSERE "SCORE PILAR" NO FINAL
            pilar_columns.append("SCORE PILAR")
        if pilar == "GLOBAL":
            # ADICIONA AS COLUNAS DO PILAR GLOBAL À LISTA global_columns
            global_columns.extend([(pilar, col) for col in pilar_columns])
        else:
            # ADICIONA AS COLUNAS DOS OUTROS PILARES À LISTA other_columns
            other_columns.extend([(pilar, col) for col in pilar_columns])
    # JUNTA AS LISTAS DE COLUNAS (OUTRAS ANTES E GLOBAL NO FINAL)
    all_columns = other_columns + global_columns
    # REINDEXA O DATAFRAME COM AS COLUNAS REORDENADAS
    df = df.reindex(columns=pd.MultiIndex.from_tuples(all_columns))

    return df


def get_class_info(id, value_wanted, arg_wanted, data_class_list):
    """
    RETORNA O VALOR DE UM ARGUMENTO ESPECÍFICO DE UM OBJETO NA LISTA DE CLASSES.

    ARGUMENTOS:
        id (str): O NOME DO ATRIBUTO A SER COMPARADO COM O VALOR DESEJADO.
        value_wanted (any): O VALOR QUE O ATRIBUTO DO OBJETO DEVE TER PARA SER SELECIONADO.
        arg_wanted (str): O NOME DO ATRIBUTO DO QUAL O VALOR SERÁ RETORNADO.
        data_class_list (List[Any]): A LISTA DE OBJETOS DE CLASSE ONDE A BUSCA SERÁ REALIZADA.

    RETORNA:
        any: O VALOR DO ARGUMENTO DESEJADO SE O ID DO OBJETO CORRESPONDER AO VALOR DESEJADO,
             OU None SE NENHUM OBJETO NA LISTA ATENDER A CONDIÇÃO.
    """
    # ITERA SOBRE A LISTA DE OBJETOS DE CLASSE
    for obj in data_class_list:
        # SE O ID DO OBJETO FOR IGUAL AO VALOR DESEJADO
        if getattr(obj, id) == value_wanted:
            # RETORNA O ARGUMENTO DESEJADO DO OBJETO
            return getattr(obj, arg_wanted)
    # RETORNA NONE SE NENHUM OBJETO FOR ENCONTRADO
    return None


dict_farol = {
    "VERMELHO": {"cor_icone": "red", "icones": "bi bi-x-circle-fill"},
    "AMARELO": {"cor_icone": "#B68105", "icones": "bi bi-dash-circle-fill"},
    "VERDE": {"cor_icone": "green", "icones": "bi bi-check-circle-fill"},
}


def ordenar_lista(lista, ordem_desejada):
    ordem_indices = {elemento: index for index, elemento in enumerate(ordem_desejada)}
    lista_ordenada = sorted(lista, key=lambda x: ordem_indices.get(x, float("inf")))
    return lista_ordenada


lista = ["a", "b", "c", "d"]

ordem_desejada = ["b", "d", "e", "a", "c"]
lista_ordenada = ordenar_lista(lista, ordem_desejada)
print(lista_ordenada)


def generate_html_table(
    dataframe: pd.DataFrame,
    df_combined: pd.DataFrame,
    score_farol_map: ScoreFarolMap,
    index_columns: List[str],
    score_pilar_selected: List[str],
    rows_per_page: int = 7,
) -> str:

    # LÊ O CONTEÚDO DO ARQUIVO CSS
    with open("app/src/style/style_farol_table_score_viewer.css", "r") as file:
        css_file = file.read()

    # ADICIONA O CSS DA TABELA HTML
    css = f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"><style>{css_file}</style>"""

    # INÍCIO DA HEADER
    html_string = """<div id="table-container"><table id="emp-table"><thead><tr>"""

    # INICIALIZA O ÍNDICE DAS COLUNAS
    col_index = len(index_columns)

    # REORGANIZA AS COLUNAS DO DATAFRAME PRINCIPAL --> SCORE PILAR COMO COLUNA MAIS A DIREITA DENTRO DE UM PIKLAR
    dataframe = rearranja_coluna_score_pilar(dataframe)

    # ITERA SOBRE AS COLUNAS SELECIONADAS COMO INDEX (MULTISELECT)
    for index_column in index_columns:
        # ADICIONA AS COLUNAS DE ÍNDICE AO CABEÇALHO
        html_string += f'<th class="index" rowspan="2">{index_column}</th>'

    # PILAR GLOBAL DEVE SEMPRE SER VISÍVEL
    ordem_pilares = score_pilar_selected + ["GLOBAL"]

    # ITERA SOBRE OS PILARES
    for pilar in ordem_pilares:
        if pilar in dataframe.columns.levels[0]:
            # OBTÉM A QUANTIDADE DE TEMAS NO PILAR
            qtd_temas_no_pilar = len(dataframe[pilar].columns)
            # ADICIONA UM CABEÇALHO DE COLUNA COM O NOME DO PILAR
            html_string += f'<th colspan="{qtd_temas_no_pilar}" style="border: 1px solid #D5D5DB; background-color: #EFF2F6">{pilar}</th>'

    # FECHA A LINHA DA HEADER E INICIA UMA NOVA LINHA
    html_string += "</tr><tr>"

    # ITERA SOBRE OS PILARES
    for pilar in ordem_pilares:
        if pilar in dataframe.columns.levels[0]:
            # ITERA SOBRE OS TEMAS DE CADA PILAR
            for tema in dataframe[pilar].columns:
                col_index += 1  # INCREMENTA O ÍNDICE DA COLUNA
                # ADICIONA UMA COLUNA DE HEADER COM O TEMA
                html_string += f"""<th class="sortable" data-column="{pilar}-{tema}" style="min-width: 100px; background-color: #F8F9FB;">{tema}</th>"""
    html_string += "</tr></thead><tbody id='table-body'>"

    # ITERA SOBRE AS LINHAS DO DATAFRAME
    for _, row_data in dataframe.iterrows():
        # INICIA UMA NOVA LINHA NA TABELA
        html_string += "<tr>"

        # PARA CASOS ONDE COLUNAS INDEX NÃO ESTEJAM SELECIONADAS
        index_values = (
            [row_data.name] if isinstance(row_data.name, int) else row_data.name
        )

        # ADICIONA ÍNDICE À LINHA
        for index_column in index_values:
            html_string += f"<td class='index'>{index_column}</td>"

        # FILTRA O DATAFRAME COMBINADO POR AGENCIA USANDO O PRIMEIRO ELEMENTO DA LISTA
        df_agencia = df_combined.loc[df_combined["AGENCIA"] == index_values[0]]

        # ITERA SOBRE OS PILARES
        for pilar in ordem_pilares:
            if pilar in dataframe.columns.levels[0]:
                # ITERA SOBRE OS TEMAS DE CADA PILAR
                for tema in dataframe[pilar].columns:
                    # OBTÉM O VALOR DA CÉLULA, OU 0 SE NÃO EXISTIR
                    valor = row_data.get((pilar, tema), 0)
                    icone_color = None
                    icone_score = None
                    df_agencia_pilar_tema = df_agencia.loc[
                        (df_agencia["PILAR"] == pilar) & (df_agencia["TEMA"] == tema)
                    ]
                    if valor != "-" and not df_agencia_pilar_tema.empty:
                        icone_color = get_class_info(
                            id="nome_etl",
                            value_wanted=df_agencia_pilar_tema["FAROL"].values[0],
                            arg_wanted="cor_icone",
                            data_class_list=score_farol_map.farol_list,
                        )
                        icone_score = get_class_info(
                            id="nome_etl",
                            value_wanted=df_agencia_pilar_tema["FAROL"].values[0],
                            arg_wanted="icones",
                            data_class_list=score_farol_map.farol_list,
                        )
                    # ADICIONA A CÉLULA COM O ÍCONE E O VALOR
                    html_string += f'<td data-column="{pilar}-{tema}" style="color: black; text-align: center; min-width: 50px;"><div style="display: flex;"><div style="width: 50%; display: flex; justify-content: flex-end;"><span class="{icone_score}" style="color: {icone_color}; padding-right: 5px;"></span></div><div style="width: 50%; display: flex; justify-content: flex-start;">{valor}</div></div></td>'
        # FECHA A LINHA DA TABELA
        html_string += "</tr>"

    # FECHA A TABELA E O DOCUMENTO HTML
    html_string += """</tbody></table><div class="pagination" id="pagination"></div></div></body></html>"""

    # ADICIONA O CSS AO FINAL DO HTML
    html_string += css

    with open(
        "app/src/style/sorting_and_pagination_table_score_viewer.js", "r"
    ) as file:
        # LÊ O CONTEÚDO DO ARQUIVO JS
        js_file = file.read()

    # SUBSTITUI O ESPAÇO RESERVADO PELO NÚMERO DE LINHAS POR PÁGINA
    js_file = js_file.replace("str(rows_per_page)", str(rows_per_page))

    # ADICIONA O CÓDIGO JS NO HTML
    js_script = f"<script>{js_file}</script>"

    html_string += js_script
    return html_string
