import pandas as pd
from loguru import logger


def merge_de_2_ou_3_bases_removendo_colunas_desnecessarias(
    dataframe_1: pd.DataFrame,
    dataframe_2: pd.DataFrame,
    merge_column_dataframe_1: str,
    merge_column_dataframe_2: str,
    list_columns_to_drop: list = None,
    list_columns_to_select: list = None,
    list_drop_duplicates_columns: list = None,
    dataframe_3: pd.DataFrame = pd.DataFrame(),
    merge_column_dataframe_3: str = None,
    how_merge_1: str = "inner",
    how_merge_2: str = "inner",
) -> pd.DataFrame:
    """FUNÇÃO RESPONSÁVEL POR REALIZAR O MERGE ENTRE 2 ou 3 BASES E
    REMOVER COLUNAS DESNECESSÁRIAS.

    Args:
      dataframe_1 (pd.DataFrame): DATAFRAME BASE COM OS DADOS FILTRADOS DE SCORE.
      dataframe_2 (pd.DataFrame): DATAFRAME COM O SCORE POR PILAR.
      dataframe_3 (pd.DataFrame, Optional): DATAFRAME COM O SCORE GLOBAL. DEFAULT TO pd.DataFrame()
      list_columns_to_drop (list): LISTA DE COLUNAS A SEREM REMOVIDAS APÓS O MERGE.
      merge_column_dataframe_1 (str): NOME DA COLUNA DE ID DA AGÊNCIA NA BASE ÚNICA.
      merge_column_dataframe_2 (str): NOME DA COLUNA DE ID DA AGÊNCIA NA BASE DE SCORE POR PILAR.
      merge_column_dataframe_3 (str, Optional): NOME DA COLUNA DE ID DA AGÊNCIA NA BASE DE SCORE GLOBAL. DEFAULT TO None
      how_merge_1 (str, Optional): COMO O PRIMEIRO MERGE DEVE SER FEITO: inner, outer, left, right
      how_merge_2 (str, Optional): COMO O SEGUNDO MERGE DEVE SER FEITO: inner, outer, left, right

    Returns:
      pd.DataFrame: DATAFRAME RESULTANTE APÓS O MERGE E DROP DAS COLUNAS ESPECIFICADAS.
    """

    # MERGE ENTRE A BASE ÚNICA E BASE SCORE POR PILAR (RISCO, PERFORMANCE...)
    df_base_unica_pilar = pd.merge(
        dataframe_1,
        dataframe_2,
        left_on=merge_column_dataframe_1,
        right_on=merge_column_dataframe_2,
        how=how_merge_1,
    )

    if not dataframe_3.empty and merge_column_dataframe_3:
        # MERGE ENTRE A BASE RESULTANTE E BASE SCORE GLOBAL (NOTA GERAL DA AGÊNCIA)
        dataframe_final = pd.merge(
            df_base_unica_pilar,
            dataframe_3,
            left_on=merge_column_dataframe_1,
            right_on=merge_column_dataframe_3,
            how=how_merge_2,
        )
    else:
        dataframe_final = df_base_unica_pilar

    if list_columns_to_drop:
        # DROP DE COLUNAS APÓS O MERGE --> COLUNAS NÃO NECESSÁRIAS NA VISUALIZAÇÃO DO DATAFRAME EXPLORER
        dataframe_final.drop(
            list_columns_to_drop, axis=1, inplace=True, errors="ignore"
        )

        logger.debug(f"COLUNAS {list_columns_to_drop} REMOVIDAS DO DATAFRAME")
    if list_columns_to_select:
        colunas_selected = [
            col for col in list_columns_to_select if col in dataframe_final.columns
        ]
        dataframe_final = dataframe_final[colunas_selected]
        logger.debug(f"COLUNAS {colunas_selected} SELECIONADAS NO DATAFRAME")
    if list_drop_duplicates_columns:
        dataframe_final.drop_duplicates(list_drop_duplicates_columns, inplace=True)
        logger.debug(
            f"REMOÇÃO DE DUPLICADAS A PARTIR DAS COLUNAS: {list_drop_duplicates_columns}"
        )

    return dataframe_final
