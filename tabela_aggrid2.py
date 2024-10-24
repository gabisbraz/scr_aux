from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme, JsCode
import pandas as pd
import streamlit as st

# Exemplo simplificado de df_tabela_farol_pivot
df_tabela_farol_pivot = pd.DataFrame(
    {
        "AGENCIA": [1, 2, 3],
        "TEMA": ["VERMELHO - 45", "AMARELO - 65", "VERDE - 85"],
    }
)

# Função JavaScript para aplicar estilo de célula com base no texto antes do '-'
cell_style_js = JsCode(
    """
function(params) {
    if (params.value.includes("VERMELHO")) {
        return {
            'color': 'red',
            'font-weight': 'bold',
        };
    } else if (params.value.includes("AMARELO")) {
        return {
            'color': 'orange',
            'font-weight': 'bold',
        };
    } else if (params.value.includes("VERDE")) {
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
    let val_splited = params.value.split(" - ");
    if (val_splited[0] === "VERMELHO") {
        return '❌ ' + val_splited[1];
    } else if (val_splited[0] === "AMARELO") {
        return '⚠️ ' + val_splited[1];
    } else if (val_splited[0] === "VERDE") {
        return '✅ ' + val_splited[1];
    }
    return val_splited[1];
}
"""
)

# Definir as opções de grid, incluindo o cellStyle e cellRenderer
gridOptions = {
    "columnDefs": [
        {
            "headerName": "AGENCIA",
            "field": "AGENCIA",
            "pinned": "left",
        },
        {
            "headerName": "TEMA",
            "field": "TEMA",
            "cellStyle": cell_style_js,
            "cellRenderer": cell_renderer_js,
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

# Se você quiser visualizar o resultado da interação
st.write("Tabela exibida com sucesso!")
