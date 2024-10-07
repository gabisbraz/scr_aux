import streamlit as st
import pandas as pd
from streamlit.components.v1 import html


# Função para carregar dados do CSV
def load_data(file):
    # Lê o arquivo CSV usando pandas
    df = pd.read_csv(file, sep=";", header=1)  # O cabeçalho é na segunda linha
    return df


# File uploader para o usuário enviar o CSV
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    # Carregar os dados do CSV
    df = load_data(uploaded_file)

    # Exibir os dados carregados (opcional)
    st.write("Dados Carregados:")
    st.dataframe(df)

    # Renomear colunas para que sejam únicas
    df.columns = [
        "Agencia",
        "Performance",
        "AA",
        "AB",
        "Global",
        "Regulatório",
        "Segurança",
        "Global_2",
    ]

    # Definindo o HTML para Ag-Grid
    ag_grid_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Ag-Grid Table with CSV Data</title>
      <script src="https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.noStyle.js"></script>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-grid.css">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-theme-alpine.css">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
      <style>
        #myGrid {{
          width: 100%;
          height: 500px;
          overflow: auto;
        }}
        .ag-header-group-cell {{
          font-weight: bold;
          text-align: center;
        }}
        .ag-header-group-cell[data-col-id="FIRST"] {{
          background-color: #007bff !important;
          color: white !important;
          border-right: 2px solid white;
        }}
        .ag-header-group-cell[data-col-id="SECOND"] {{
          background-color: #28a745 !important;
          color: white !important;
          border-right: 2px solid white;
        }}
        .ag-header-cell {{
          border-bottom: 2px solid #ccc;
        }}
      </style>
    </head>
    <body>
      <div id="myGrid" class="ag-theme-alpine"></div>

      <script>
        const gridOptions = {{
          rowData: {df.to_json(orient='records')},
          columnDefs: [
            {{ field: "Agencia", headerName: "Agência", pinned: "left", minWidth: 100 }},
            {{
              headerName: "Performance",
              children: [
                {{
                  field: "AA", 
                  headerName: "AA", 
                  minWidth: 150,
                  cellRenderer: function(params) {{
                    const value = params.value;
                    let color = 'transparent';
                    if (value === 5.77) {{
                      color = 'red';
                    }} else if (value === 5.78) {{
                      color = 'yellow';
                    }} else if (value === 5.79) {{
                      color = 'green';
                    }}
                    return `<span title='${{value}}'><i class='bi bi-0-square-fill' style='color: ${{color}};'></i> ${{value}}</span>`;
                  }}
                }},
                {{
                  field: "AB", 
                  headerName: "AB", 
                  minWidth: 150,
                  cellRenderer: function(params) {{
                    const value = params.value;
                    let color = 'transparent';
                    if (value === 5.77) {{
                      color = 'red';
                    }} else if (value === 5.78) {{
                      color = 'yellow';
                    }} else if (value === 5.79) {{
                      color = 'green';
                    }}
                    return `<span title='${{value}}'><i class='bi bi-0-square-fill' style='color: ${{color}};'></i> ${{value}}</span>`;
                  }}
                }},
                {{
                  field: "Global", 
                  headerName: "Global", 
                  minWidth: 150,
                  cellRenderer: function(params) {{
                    const value = params.value;
                    let color = 'transparent';
                    if (value === 5.77) {{
                      color = 'red';
                    }} else if (value === 5.78) {{
                      color = 'yellow';
                    }} else if (value === 5.79) {{
                      color = 'green';
                    }}
                    return `<span title='${{value}}'><i class='bi bi-0-square-fill' style='color: ${{color}};'></i> ${{value}}</span>`;
                  }}
                }},
              ]
            }},
            {{
              headerName: "Riscos",
              children: [
                {{ field: "Regulatório", headerName: "Regulatório", minWidth: 150, cellRenderer: function(params) {{ return `<span title='${{params.value}}'>${{params.value}}</span>`; }} }},
                {{ field: "Segurança", headerName: "Segurança", minWidth: 150, cellRenderer: function(params) {{ return `<span title='${{params.value}}'>${{params.value}}</span>`; }} }},
                {{ field: "Global_2", headerName: "Global (Duplicado)", minWidth: 150, cellRenderer: function(params) {{ return `<span title='${{params.value}}'>${{params.value}}</span>`; }} }}  // Para exemplo
              ]
            }}
          ],
          defaultColDef: {{
            sortable: true,
            filter: true,
            resizable: true,
            minWidth: 100
          }},
        }};

        const eGridDiv = document.querySelector('#myGrid');
        new agGrid.Grid(eGridDiv, gridOptions);
        gridOptions.api.sizeColumnsToFit();
      </script>
    </body>
    </html>
    """

    # Renderizar o HTML do Ag-Grid no Streamlit
    html(ag_grid_html, height=550, scrolling=True)
else:
    st.write("Por favor, faça o upload de um arquivo CSV.")
