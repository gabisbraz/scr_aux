import pandas as pd
import streamlit as st
from streamlit.components.v1 import html

dataframe = pd.read_excel("base_tema_novo.xlsx")

list_pilares = dataframe["PILAR"].unique()
dataframe["SCORE"] = dataframe["SCORE"].astype(str) + " - " + dataframe["FAROL"]
dataframe["TEMA"] = dataframe["PILAR"].astype(str) + " - " + dataframe["TEMA"]
dataframe.drop(columns=["FAROL", "PILAR"], inplace=True)

df_pivot = dataframe.pivot_table(
    index="CD_PONTO",
    columns="TEMA",
    values="SCORE",
    aggfunc="first",
    fill_value="-",
)
df_pivot.sort_index(axis=1, level=list(range(len(["PILAR", "TEMA"])))).reset_index()


print(df_pivot)

str_js = ""

for index_col in ["CD_PONTO"]:
    str_js += f""""
        {{{{ field: "{index_col}", headerName: "{index_col}", pinned: "left", minWidth: 100 }}}},
    """
for pilar in list(list_pilares):
    str_tema = ""
    for tema in list(df_pivot.columns.values):
        pilar_splited, tema_splited = tema.split(" - ")
        if pilar == pilar_splited:
            str_tema += f"""
                {{{{
                    field: "{tema}",
                    headerName: "{tema_splited}",
                    minWidth: 150,
                }}}},
            """
    str_js += f"""
        {{{{
            headerName: "{pilar}",
            children: [{str_tema}]
        }}}},
    """

print(str_js)

# Adaptar o HTML e o JavaScript para usar o renderer
ag_grid_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Ag-Grid Table with Icons</title>
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
        .icon {{
          margin-right: 5px;
        }}
      </style>
    </head>
    <body>
      <div id="myGrid" class="ag-theme-alpine"></div>

      <script>
        const farolDict = {{
          "VERMELHO": {{ icon: "bi bi-stoplights-fill", color: "red" }},
          "AMARELO": {{ icon: "bi bi-stoplights-fill", color: "yellow" }},
          "VERDE": {{ icon: "bi bi-stoplights-fill", color: "green" }},
        }};

        function farolCellRenderer(params) {{
          if (params.value) {{
            const [score, farol] = params.value.split(' - ');
            const farolInfo = farolDict[farol] || {{}};
            return `
              <span>
                <i class="${{farolInfo.icon}}" style="color:${{farolInfo.color}}"></i> 
                ${{score}}
              </span>
            `;
          }}
          return params.value;
        }}

        const gridOptions = {{
          rowData: {df_pivot.to_json(orient='records')},
          columnDefs: [
            {{ field: "CD_PONTO", headerName: "CD_PONTO", pinned: "left", minWidth: 100 }},
            {{
                headerName: "EFICIÊNCIA",
                children: [
                {{
                    field: "EFICIÊNCIA - INFRA CIVIL",
                    headerName: "INFRA CIVIL",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
                {{
                    field: "EFICIÊNCIA - SCORE PILAR",
                    headerName: "SCORE PILAR",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
            ]
        }},
        {{
            headerName: "PERFORMANCE",
            children: [
                {{
                    field: "PERFORMANCE - AA",
                    headerName: "AA",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
                {{
                    field: "PERFORMANCE - AB",
                    headerName: "AB",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
                {{
                    field: "PERFORMANCE - INFRA DE TI",
                    headerName: "INFRA DE TI",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
                {{
                    field: "PERFORMANCE - SCORE PILAR",
                    headerName: "SCORE PILAR",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
            ]
        }},
        {{
            headerName: "RISCOS",
            children: [
                {{
                    field: "RISCOS - REGULATÓRIO",
                    headerName: "REGULATÓRIO",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
                {{
                    field: "RISCOS - SCORE PILAR",
                    headerName: "SCORE PILAR",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
                {{
                    field: "RISCOS - SEGURANÇA",
                    headerName: "SEGURANÇA",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
            ]
        }},
        {{
            headerName: "ESG",
            children: [
                {{
                    field: "ESG - ESG",
                    headerName: "ESG",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
                {{
                    field: "ESG - SCORE PILAR",
                    headerName: "SCORE PILAR",
                    minWidth: 150,
                    cellRenderer: farolCellRenderer
                }},
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

html(ag_grid_html, height=550, scrolling=True)


st.dataframe(df_pivot)
