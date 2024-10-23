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

# Criar um segundo DataFrame com informações adicionais para tooltips
df2 = pd.DataFrame(
    {
        "AGENCIA": agencias,
        "NOME_AGENCIA": [
            f"Agência {i}" for i in agencias
        ],  # Exemplo de nome de agência
        "VALOR": np.random.randint(1, 1000, len(agencias)),  # Exemplo de valor numérico
    }
)

# Mesclar o df_pivot com df2 para incluir as informações adicionais para os tooltips
df_pivot = df_pivot.merge(df2, on="AGENCIA")


# Função para formatar os scores com ícones e preparar os tooltips
def format_scores(val):
    try:
        if isinstance(val, (int, float)) and 0 <= val < 40:
            return f"❌ {val:.2f}"
        elif isinstance(val, (int, float)) and 40 <= val < 80:
            return f"⚠️ {val:.2f}"
        elif isinstance(val, (int, float)) and 80 <= val < 100:
            return f"✅ {val:.2f}"
        return f"{val:.2f}"
    except:
        return val


# Aplicar a formatação ao DataFrame
df_pivot[df_pivot.columns.difference(["AGENCIA", "NOME_AGENCIA", "VALOR"])] = df_pivot[
    df_pivot.columns.difference(["AGENCIA", "NOME_AGENCIA", "VALOR"])
].applymap(format_scores)

# Resetar o índice para preparar os dados para exibição
df_pivot.reset_index(drop=True, inplace=True)

# Definir as opções de grid, incluindo a coluna "AGENCIA" e *tooltips* para cada coluna
gridOptions = {
    "columnDefs": [
        {
            "headerName": "AGENCIA",
            "field": "AGENCIA",
            "pinned": "left",
            "tooltipField": "AGENCIA",
            "tooltipValueGetter": {
                "function": (
                    "function(params) {"
                    "    var nome = params.data.NOME_AGENCIA;"
                    "    var valor = params.data.VALOR;"
                    "    return 'Agência: ' + nome + ', Valor: ' + valor;"
                    "}"
                )
            },  # Tooltip personalizado com nome da agência e valor
        },
        {
            "headerName": "EFICIÊNCIA",
            "children": [
                {"field": "INFRA CIVIL", "tooltipField": "INFRA CIVIL"},
            ],  # Tooltip para INFRA CIVIL
        },
        {
            "headerName": "PERFORMANCE",
            "children": [
                {"field": "AA", "tooltipField": "AA"},
                {"field": "AB", "tooltipField": "AB"},
                {"field": "INFRA DE TI", "tooltipField": "INFRA DE TI"},
            ],
        },
        {
            "headerName": "RISCOS",
            "children": [
                {"field": "REGULATÓRIO", "tooltipField": "REGULATÓRIO"},
                {"field": "SEGURANÇA", "tooltipField": "SEGURANÇA"},
            ],
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
    allow_unsafe_jscode=True,  # Permitir JavaScript personalizado
)

# Se você quiser visualizar o resultado da interação
st.write("Tabela exibida com sucesso!")
