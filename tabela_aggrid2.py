from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme, JsCode
import pandas as pd
import streamlit as st

# Exemplo simplificado de df_tabela_farol_pivot com colunas numéricas
df_tabela_farol_pivot = pd.DataFrame(
    {
        "AGENCIA": [1, 2, 3],
        "TEMA": ["VERMELHO - 45", "AMARELO - 65", "VERDE - 85"],
    }
)

# Extrair o valor numérico da coluna "TEMA"
df_tabela_farol_pivot["SCORE"] = df_tabela_farol_pivot["TEMA"].apply(
    lambda x: float(x.split(" - ")[1])
)

# Função JavaScript para aplicar estilo de célula com base no texto antes do '-'
cell_style_js = JsCode(
    """
function(params) {
    if (params.data.TEMA.includes("VERMELHO")) {
        return {
            'color': 'red',
            'font-weight': 'bold',
        };
    } else if (params.data.TEMA.includes("AMARELO")) {
        return {
            'color': 'orange',
            'font-weight': 'bold',
        };
    } else if (params.data.TEMA.includes("VERDE")) {
        return {
            'color': 'green',
            'font-weight': 'bold',
        };
    }
    return null;
}
"""
)

# Função JavaScript para renderizar o conteúdo da célula com ícones
cell_renderer_js = JsCode(
    """
function(params) {
    let val_splited = params.data.TEMA.split(" - ");
    if (val_splited[0] === "VERMELHO") {
        return '❌ ' + params.value.toFixed(2);
    } else if (val_splited[0] === "AMARELO") {
        return '⚠️ ' + params.value.toFixed(2);
    } else if (val_splited[0] === "VERDE") {
        return '✅ ' + params.value.toFixed(2);
    }
    return params.value.toFixed(2);
}
"""
)

# Definir as opções de grid, garantindo que a coluna SCORE seja tratada como numérica
gridOptions = {
    "columnDefs": [
        {
            "headerName": "AGENCIA",
            "field": "AGENCIA",
            "pinned": "left",
        },
        {
            "headerName": "SCORE",
            "field": "SCORE",
            "type": "numericColumn",  # Definir a coluna como numérica
            "cellStyle": cell_style_js,
            "cellRenderer": cell_renderer_js,
            "sortable": True,  # Habilitar a ordenação numérica
        },
    ]
}

# Exibir a tabela no AgGrid
AgGrid(
    df_tabela_farol_pivot,
    gridOptions=gridOptions,  # Usar as gridOptions configuradas
    update_mode=GridUpdateMode.NO_UPDATE,
    fit_columns_on_grid_load=False,  # Ajustar colunas ao carregar a grid
    theme=AgGridTheme.MATERIAL,  # Aplicar tema material
    allow_unsafe_jscode=True,  # Permitir JavaScript personalizado
)

# Exibir mensagem de sucesso
st.write("Tabela exibida com sucesso!")
