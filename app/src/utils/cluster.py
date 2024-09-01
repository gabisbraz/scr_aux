"""
  __author__ = Gabriella Silveira Braz
  __email__ = gabriella.braz@itau-unibanco.com.br
  __version__ = 0.0.1
  __pylintGrade__ = 10
"""

import pandas as pd
from loguru import logger


def get_clusters_list(df_base: pd.DataFrame, df_scatter: pd.DataFrame) -> list:
    """
    RETORNA UMA LISTA DE OPÇÕES DE CLUSTERS/QUADRANTES COM BASE NOS
    DATAFRAMES FORNECIDOS.

    SE O DATAFRAME DO SCATTER PLOT CONTIVER A COLUNA "CLUSTER",
    CRIA UMA LISTA ORDENADA DE CLUSTERS ÚNICOS COMBINADOS COM OS QUADRANTES.
    CASO CONTRÁRIO, RETORNA APENAS OS QUADRANTES ÚNICOS DO DATAFRAME BASE.

    Args:
      df_base (pd.DataFrame): DATAFRAME BASE CONTENDO AS INFORMAÇÕES GERAIS.
      df_scatter (pd.DataFrame): DATAFRAME RESULTANTE DO SCATTER PLOT COM
        INFORMAÇÕES DE CLUSTERIZAÇÃO.

    Returns:
      list: LISTA DE OPÇÕES DE CLUSTERS/QUADRANTES DISPONÍVEIS.
    """

    # VERIFICA SE A COLUNA CLUSTER ESTÁ PRESENTE NO DATAFRAME DO SCATTER CHART
    if "CLUSTER" in df_scatter.columns:
        # CRIA UMA COLUNA FORMATADA COM O NOME DO CLUSTER E O QUADRANTE CORRESPONDENTE
        df_scatter_unique_cluster = df_scatter.drop_duplicates(["CLUSTER"])

        coluna_cluster = (
            "CLUSTER "
            + df_scatter_unique_cluster["CLUSTER"].astype(str).str.zfill(2)
            + " - "
            + df_scatter_unique_cluster["QUADRANTE_INTERVALO"]
        ).sort_values(ascending=True)

        # COMBINA QUADRANTES ÚNICOS COM CLUSTERS E ADICIONA A OPÇÃO "TODAS OPÇÕES"
        list_clusters = (
            ["TODAS OPÇÕES"]
            + list(df_base["FAROL"].unique())
            + list(coluna_cluster.unique())
        )
        logger.debug(
            "RADAR CHART SELECTBOX CONTÉM VALORES DE QUADRANTES E CLUSTERS SELECIONADOS"
        )
    else:
        # SE NÃO HOUVER A COLUNA CLUSTER, RETORNA APENAS OS QUADRANTES ÚNICOS DO DATAFRAME BASE
        list_clusters = ["TODAS OPÇÕES"] + list(df_base["FAROL"].unique())
        logger.debug("RADAR CHART SELECTBOX CONTÉM APENAS VALORES DE QUADRANTES")

    return list_clusters


def filter_dataframe(
    df_base: pd.DataFrame, df_scatter: pd.DataFrame, selection: str
) -> pd.DataFrame:
    """
    FUNÇÃO RESPONSÁVEL POR FILTRAR O DATAFRAME COM BASE NA SELEÇÃO FORNECIDA.

    Args:
      df_base (pd.DataFrame): DATAFRAME CONTENDO OS DADOS GERAIS.
      df_scatter (pd.DataFrame): DATAFRAME RESULTANTE DO SCATTER PLOT COM
        DADOS DE CLUSTERIZAÇÃO.
      selection (str): SELEÇÃO PARA FILTRAGEM (FAROL OU TODAS AGÊNCIAS)

    Returns:
      pd.DataFrame: DATAFRAME FILTRADO DE ACORDO COM A SELEÇÃO.
    """

    # VERIFICA SE A SELEÇÃO É "TODAS OPÇÕES" E RETORNA O DF COMPLETO
    if selection == "TODAS OPÇÕES":
        logger.debug("RADAR CHART SELECTBOX DE AGÊNCIAS CONTÉM TODOS OS PONTOS")
        return df_base

    logger.debug(
        f"RADAR CHART SELECTBOX DE AGÊNCIAS CONTÉM APENAS PONTOS DO QUADRANTE {selection}"
    )

    # FILTRA O DATAFRAME PELO QUADRANTE SELECIONADO
    return df_base[df_base["FAROL"] == selection]


def calcula_medias(
    dataframe: pd.DataFrame,
    colunas: list,
    agencias: list,
) -> dict:
    """FUNÇÃO RESPONSÁVEL POR CALCULAR A MÉDIA GLOBAL DO SCORE POR UF,
    MUNICÍPIO E CLUSTER E VALORES AGRUPADOS PR TEMA, FILTRADOS A
    PARTIR DAS COLUNAS ESPECIFICADAS

    Args:
      dataframe (pd.DataFrame): DATAFRAME INPUT DO DATAFRAME_EXPLORER,
        PARA CÁLCULO GERAL DOS CAMPOS A SER AGRUPADO. AS COLUNAS ESPERADAS DO DF SÃO:
        ['CD_PONTO', 'NOME DO PONTO', 'UF', 'MUNICIPIO', 'SCORE EFICIENCIA',
        'SCORE RISCO', 'SCORE PERFORMANCE', 'SCORE GLOBAL',
        'QUADRANTE_INTERVALO']
      colunas (list): LISTA DE NOMES DAS COLUNAS A SEREM AGRUPADAS.
      agencias (list): LISTA COM O NÚMERO DE 2 CD_PONTOS

    Returns:
      dict_values: DICIONÁRIO COM AS MÉDIAS DOS VALORES POR TEMA
        (EX.: {'AGENCIA 1': {'CD_PONTO': {...}, 'UF': {...},
        'MUNICIPIO': {...}, 'QUADRANTE': {...}}})
    """

    dict_values = {}

    for agencia in agencias:
        dict_agencia = {}

        for coluna in colunas:
            dict_grouped_values_return = {}

            # GET VALOR QUE AGRUPARÁ A TABELA (EX.: SP, OSASCO, ↑ EFICIÊNCIA ↓ PERFORMANCE)
            groupby_value = dataframe.loc[
                dataframe["CD_PONTO"] == int(agencia), coluna
            ].values[0]

            # FILTRA A TABELA PELO VALOR groupby_value DE UMA COLUNA ESPECIFICADA
            df_filtered_by_value = dataframe.loc[dataframe[coluna] == groupby_value]

            # CALCULA AS MÉDIAS POR TEMA, AGRUPADA PELA COLUNA ESPECIFICADA
            dict_grouped_values = (
                df_filtered_by_value.groupby(["TEMA"])["SCORE_TEMA"].mean().to_dict()
            )

            dict_grouped_values_return[coluna] = {
                key: round(value, 2) for key, value in dict_grouped_values.items()
            }

            # DICIONÁRIO COM CHAVE IGUAL AO groupby_value E VALOR IGUAL A MÉDIA DO
            # SCORE GLOBAL DO groupby_value
            dict_score_global_value_grouped = (
                df_filtered_by_value.groupby([coluna])["SCORE GLOBAL"].mean().to_dict()
            )

            # ARREDONDA O VALOR DA MÉDIA DO AGRUPAMENTO DO SCORE GLOBAL POR groupby_value
            dict_score_global_value_grouped[groupby_value] = round(
                dict_score_global_value_grouped[groupby_value], 2
            )

            dict_agencia[coluna] = {
                "SCORE_LAYER": dict_grouped_values_return[coluna],
                "NOME": groupby_value,
                "SCORE_GERAL": dict_score_global_value_grouped.get(groupby_value),
            }

        dict_values[f"AGENCIA_{agencia}"] = dict_agencia

        logger.debug(
            f"MÉDIAS POR TEMAS DO SCORE CALCULADAS: {dict_values[f'AGENCIA_{agencia}']}"
        )

    return dict_values
