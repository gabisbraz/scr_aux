"""
  __author__ = Gabriella Silveira Braz
  __email__ = gabriella.braz@itau-unibanco.com.br
  __version__ = 0.0.1
  __pylintGrade__ = 9.27
"""

import sys
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

DIR_ROOT = Path(__file__).parent.parent.parent
sys.path.append(DIR_ROOT)


def create_pivot_table_with_multindex(
    dataframe: pd.DataFrame,
    index: str = None,
    columns: list = None,
    values: str = None,
    axis: int = 1,
) -> pd.DataFrame:
    """FUNÇÃO RESPONSÁVEL POR CRIAR UMA TABELA PIVOT COM MULTI-ÍNDICE

    Args:
      dataframe (pd.DataFrame): DATAFRAME INICIAL A SER TRANSFORMADO.
      index (str, optional): COLUNA QUE SERÁ UTILIZADA COMO ÍNDICE DA TABELA
        PIVOT. DEFAULTS TO None.
      columns (list, optional): LISTA DE COLUNAS QUE SERÃO UTILIZADAS COMO
        COLUNAS NA TABELA PIVOT. DEFAULTS TO None.
      values (str, optional): COLUNA CUJOS VALORES SERÃO PREENCHIDOS NA
        TABELA PIVOT. DEFAULTS TO None.
      axis (int, optional): EIXO DE ORDENAÇÃO DA TABELA PIVOT
        (0 PARA LINHAS, 1 PARA COLUNAS). DEFAULTS TO 1.

    Returns:
      pd.DataFrame: DATAFRAME RESULTANTE APÓS A CRIAÇÃO E ORDENAÇÃO
        DA TABELA PIVOT.
    """
    # CRIA A TABELA PIVOT COM BASE NO DATAFRAME, ÍNDICE, COLUNAS E VALORES FORNECIDOS
    df_pivot = dataframe.pivot_table(
        index=index, columns=columns, values=values, aggfunc="first", fill_value="-"
    )

    # ORDENA A TABELA PIVOT DE ACORDO COM OS NÍVEIS DAS COLUNAS ESPECIFICADAS
    return df_pivot.sort_index(axis=axis, level=list(range(len(columns))))


# Função para exportar DataFrames para Excel estilizado
def to_excel(
    df_base_unica: pd.DataFrame = pd.DataFrame(),
    df_score_pilar: pd.DataFrame = pd.DataFrame(),
    df_score_tema: pd.DataFrame = pd.DataFrame(),
):
    """FUNÇÃO QUE EXPORTA VÁRIOS DATAFRAMES PARA UM ARQUIVO EXCEL ESTILIZADO.

    Args:
      df_base_unica (pd.DataFrame): DATAFRAME CONTENDO OS DADOS DA BASE UNICA.
      df_score_pilar (pd.DataFrame): DATAFRAME CONTENDO OS DADOS DO RANKING.
      df_score_tema (pd.DataFrame): DATAFRAME CONTENDO OS DADOS DO TABELAO.

    Returns:
      bytes: ARQUIVO EXCEL EM FORMATO BINÁRIO.
    """

    # CRIA UM OBJETO BytesIO PARA ARMAZENAR O ARQUIVO EXCEL
    output = BytesIO()

    # UTILIZA O CONTEXT MANAGER PARA ESCREVER OS DATAFRAMES NO ARQUIVO EXCEL
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        # CRIA O WORKBOOK
        workbook = writer.book

        # ADICIONA FORMATAÇÃO
        format1 = workbook.add_format({"num_format": "0.00", "align": "center"})
        format2 = workbook.add_format({"align": "center"})
        header_format = workbook.add_format(
            {"bg_color": "#D3D3D3", "bold": True, "align": "center"}
        )

        if not df_base_unica.empty:
            # ADICIONA A SHEET 'BASE UNICA'
            df_base_unica.to_excel(writer, sheet_name="BASE ÚNICA", index=False)
            worksheet = writer.sheets["BASE ÚNICA"]

            # DEFINE O FORMATO DAS CÉLULAS PARA A BASE UNICA
            worksheet.set_column("A:Z", None, format1)
            for col_num, value in enumerate(df_base_unica.columns.values):
                worksheet.write(0, col_num, value, header_format)

            center_format = workbook.add_format({"align": "center"})
            worksheet.set_column("A:Z", None, center_format)
            worksheet.autofit()

        if not df_score_pilar.empty:
            df_score_pilar.to_excel(writer, sheet_name="SCORE PILAR")
            worksheet = writer.sheets["SCORE PILAR"]

            # DEFINE O FORMATO DAS CÉLULAS
            worksheet.set_column("A:Z", None, format1)

            # FORMATA MULTIINDEX
            header_format_bold = workbook.add_format({"bold": True, "align": "center"})
            header_format_bold_pilar = workbook.add_format(
                {"bold": True, "align": "center", "bg_color": "#8F8F8F"}
            )
            header_format_bold_tema = workbook.add_format(
                {"bold": True, "align": "center", "bg_color": "#A5A5A1"}
            )
            header_format_bold_coluna = workbook.add_format(
                {"bold": True, "align": "center", "bg_color": "#CDCFC9"}
            )
            for row_num, (pilar, tema) in enumerate(df_score_pilar.columns):
                worksheet.write(0, row_num + 2, pilar, header_format_bold_pilar)
                worksheet.write(1, row_num + 2, tema, header_format_bold_tema)

            # MESCLA CÉLULAS DESNECESSÁRIAS DO MULTIINDEX
            worksheet.merge_range("B1:B2", "", header_format_bold)

            # # EXCLUI LINHA 4
            worksheet.set_row(2, options={"hidden": True})

            center_format = workbook.add_format({"align": "center"})
            worksheet.set_column("A:Z", None, center_format)

            worksheet.autofit()

        if not df_score_tema.empty:
            # ADICIONA A SHEET 'SCORE TEMA'
            df_score_tema.to_excel(writer, sheet_name="SCORE TEMA")
            worksheet = writer.sheets["SCORE TEMA"]

            # DEFINE O FORMATO DAS CÉLULAS PARA O SCORE TEMA
            worksheet.set_column("A:Z", None, format2)

            # FORMATA MULTIINDEX
            header_format_bold = workbook.add_format({"bold": True, "align": "center"})
            header_format_bold_pilar = workbook.add_format(
                {"bold": True, "align": "center", "bg_color": "#8F8F8F"}
            )
            header_format_bold_tema = workbook.add_format(
                {"bold": True, "align": "center", "bg_color": "#A5A5A1"}
            )
            header_format_bold_coluna = workbook.add_format(
                {"bold": True, "align": "center", "bg_color": "#CDCFC9"}
            )
            for row_num, (pilar, tema, coluna) in enumerate(df_score_tema.columns):
                worksheet.write(0, row_num + 1, pilar, header_format_bold_pilar)
                worksheet.write(1, row_num + 1, tema, header_format_bold_tema)
                worksheet.write(2, row_num + 1, coluna, header_format_bold_coluna)

            # MESCLA CÉLULAS DESNECESSÁRIAS DO MULTIINDEX
            worksheet.merge_range("A1:A3", "", header_format_bold)

            # EXCLUI LINHA 4
            worksheet.set_row(3, options={"hidden": True})

            center_format = workbook.add_format({"align": "center"})
            worksheet.set_column("A:Z", None, center_format)

            worksheet.autofit()

    # RETORNA O ARQUIVO EXCEL EM FORMATO BINÁRIO
    return output.getvalue()
