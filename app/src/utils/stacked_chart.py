import pandas as pd
from streamlit_echarts import st_echarts


def create_bar_plot_stacked(df, df_pilar, agencia):
    df_agencia = df[df["AGENCIA_TEMA"] == agencia]
    df_agencia_pilar = df_pilar[df_pilar["AGENCIA_PILAR"] == agencia]

    pilares = df_agencia["PILAR_TEMA"].unique()
    temas = df_agencia["TEMA_TEMA"].unique()

    series_data = []
    dict_tooltip = {}
    for tema in temas:
        data = []
        for pilar in pilares:
            # Filtra os dados do tema e pilar específicos
            pilar_data = df_agencia[df_agencia["PILAR_TEMA"] == pilar]
            pilar_data_pilar = df_agencia_pilar[
                df_agencia_pilar["PILAR_PILAR"] == pilar
            ]
            if not pilar_data_pilar.empty:
                total = pilar_data_pilar["SCORE_PILAR"].values[0]
            else:
                total = 10
            total_pilar_score = pilar_data["SCORE_TEMA"].sum()

            score_df = pilar_data[pilar_data["TEMA_TEMA"] == tema]
            farol = score_df["FAROL_TEMA"]
            score = score_df["SCORE_TEMA"]
            score_value = score.values[0] if not score.empty else 0
            score_farol = farol.values[0] if not farol.empty else None
            score_value = round(float(score_value), 2)

            # Calcula a porcentagem do tema em relação ao pilar
            if total_pilar_score != 0:
                percentage = round((score_value / total_pilar_score) * total, 2)
            else:
                percentage = 0

            label_show = bool(score_value != 0)

            if pilar in dict_tooltip.keys():
                dict_tooltip[pilar][tema] = f"{score_value:.2f}"
            else:
                dict_tooltip[pilar] = {
                    tema: {"VALOR": f"{score_value:.2f}", "FAROL": score_farol}
                }

            data.append(
                {
                    "value": percentage,
                    "label": {
                        "show": label_show,
                        "position": "inside",
                        "formatter": f"{score_value:.2f}",
                    },
                    "itemStyle": {
                        "borderRadius": [0, 0, 0, 0],
                    },
                }
            )

        series_data.append(
            {
                "name": tema,
                "type": "bar",
                # "stack": "total",
                "data": data,
            }
        )

    option = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow",
            },
            "formatter": """
                            <div style="font-size: 15px; font-weight: bold; margin-bottom: 5px;">{b0}</div>
                            <div style="display: flex; align-items: center; margin-bottom: -18px;">
                                <div style="display: flex; align-items: center; padding-right: 5px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="red" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                                    </svg>
                                </div>
                                <div style="font-size: 13px;">
                                    {a0}: <b style="color">{c0}</b>
                                </div>
                            </div>
                            <br/>
                            <div style="display: flex; align-items: center; margin-bottom: -18px;">
                                <div style="display: flex; align-items: center; padding-right: 5px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="red" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                                    </svg>
                                </div>
                                <div style="font-size: 13px;">
                                    {a1}: <b style="color">{c1}</b>
                                </div>
                            </div>
                            <br/>
                            <div style="display: flex; align-items: center; margin-bottom: -18px;">
                                <div style="display: flex; align-items: center; padding-right: 5px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="red" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                                    </svg>
                                </div>
                                <div style="font-size: 13px;">
                                    {a2}: <b style="color">{c2}</b>
                                </div>
                            </div>
                            <br/>
                            <div style="display: flex; align-items: center;">
                                <div style="display: flex; align-items: center; padding-right: 5px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="red" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                                    </svg>
                                </div>
                                <div style="font-size: 13px;">
                                    {a3}: <b style="color">{c3}</b>
                                </div>
                            </div>
                            """,
        },
        "legend": {
            "bottom": 0,  # Define a legenda na parte inferior
            "orient": "horizontal",  # Define a orientação da legenda como horizontal
            "itemWidth": 10,  # Tamanho do ícone da legenda
            "itemHeight": 10,  # Altura do ícone da legenda
            "textStyle": {"fontSize": 12},  # Tamanho da fonte da legenda
        },
        "grid": {
            "left": "0%",
            "right": "0%",
            "bottom": "5%",  # Ajusta o fundo para dar espaço à legenda
            "containLabel": True,
            "backgroundColor": "#FFFFFF",  # Define o fundo do gráfico como branco
            "borderColor": "transparent",  # Remove as bordas ao redor da grade
        },
        "xAxis": {
            "type": "value",
            "max": 10,
            "axisLabel": {
                "fontSize": 10,
                "show": False,  # Reduz o tamanho da fonte dos rótulos do eixo Y
            },
            "splitLine": {"show": False},  # Remove as linhas de grade verticais
            "axisLine": {"show": False},
            "axisTick": {"show": False},
        },
        "yAxis": {
            "type": "category",
            "data": list(pilares),
            "axisLabel": {
                "fontSize": 10,
                "show": True,  # Reduz o tamanho da fonte dos rótulos do eixo Y
            },
            "axisLine": {"show": False},
            "axisTick": {"show": False},
        },
        "series": series_data,
    }

    st_echarts(options=option, height="500px")


df_score_tema = pd.read_csv("app/src/data/df_base_score_tema.csv")
df_score_pilar = pd.read_csv("app/src/data/df_base_score_pilar.csv")

create_bar_plot_stacked(df_score_tema, df_score_pilar, 1)
