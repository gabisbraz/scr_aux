from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme
import pandas as pd
import numpy as np
import streamlit as st

# Definir os pilares e seus temas
pilares_temas = [
    ("EFICIÊNCIA", "INFRA CIVIL"),
    ("PERFORMANCE", "AA"),
    ("RISCOS", "REGULATÓRIO"),
    ("RISCOS", "SEGURANÇA"),
    ("PERFORMANCE", "AB"),
    ("PERFORMANCE", "INFRA DE TI"),
]

# Definir uma lista de 3500 agências (exemplo: de 1 a 3500)
agencias = list(range(1, 3501))  # Criar lista de agências de 1 até 3500

# Criar as combinações de agências com pilares e temas
linhas = []
for agencia in agencias:
    for pilar, tema in pilares_temas:
        linhas.append(
            {"AGENCIA": agencia, "PILAR": pilar, "TEMA": tema, "SCORE": np.nan}
        )  # Inicializar SCORE como NaN

# Criar o DataFrame
df = pd.DataFrame(linhas)

# Exemplo de preenchimento aleatório de SCORE
df["SCORE"] = (
    np.random.rand(len(df)) * 100
)  # Gera valores de score aleatórios de 0 a 100

# Criar a tabela dinâmica (pivot table) baseada nas agências e temas
df_pivot = df.pivot_table(
    index="AGENCIA",  # Agências como índice
    columns="TEMA",  # Pilar e Tema como níveis de colunas
    values="SCORE",  # Valores correspondem aos scores
    aggfunc="first",  # Usar o primeiro valor em caso de duplicidade
    fill_value="-",  # Preencher valores vazios com "-"
)

# Resetar o índice para preparar os dados para exibição
df_pivot.reset_index(inplace=True)

# Definir as opções de grid, incluindo a coluna "AGENCIA"
gridOptions = {
    "columnDefs": [
        {
            "headerName": "AGENCIA",
            "field": "AGENCIA",
        },
        {
            "headerName": "EFICIÊNCIA",
            "children": [{"field": "INFRA CIVIL"}],
        },
        {
            "headerName": "PERFORMANCE",
            "children": [{"field": "AA"}, {"field": "AB"}, {"field": "INFRA DE TI"}],
        },
        {
            "headerName": "RISCOS",
            "children": [{"field": "REGULATÓRIO"}, {"field": "SEGURANÇA"}],
        },
    ]
}

# Exibir a tabela no AgGrid
AgGrid(
    df_pivot,
    gridOptions=gridOptions,  # Usar as gridOptions configuradas
    update_mode=GridUpdateMode.NO_UPDATE,
    fit_columns_on_grid_load=False,  # Ajustar colunas ao carregar a grid
    theme=AgGridTheme.MATERIAL,  # Aplicar tema material
)

# Se você quiser visualizar o resultado da interação
st.write("Tabela exibida com sucesso!")
