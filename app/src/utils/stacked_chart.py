import pandas as pd
from streamlit_echarts import st_echarts


def create_bar_plot_stacked(df, agencia):
    df_agencia = df[df["AGENCIA_TEMA"] == agencia]

    pilares = df_agencia["PILAR_TEMA"].unique()
    temas = df_agencia["TEMA_TEMA"].unique()

    series_data = []
    for tema in temas:
        data = []
        for pilar in pilares:
            score = df_agencia[
                (df_agencia["TEMA_TEMA"] == tema) & (df_agencia["PILAR_TEMA"] == pilar)
            ]["SCORE_TEMA"]
            score_value = score.values[0] if not score.empty else 0
            score_value = float(score_value)
            label_show = bool(score_value != 0)
            data.append(
                {
                    "value": score_value,
                    "label": {
                        "show": label_show,
                        "position": "inside",
                        "formatter": f"{score_value:.2f}",
                    },
                }
            )

        series_data.append(
            {
                "name": tema,
                "type": "bar",
                "stack": "total",
                "emphasis": {"focus": "series"},
                "data": data,
            }
        )

    option = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow",
            },
        },
        "legend": {},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {"type": "category", "data": list(pilares)},
        "series": series_data,
    }

    st_echarts(options=option, height="500px")


df_score_tema = pd.read_csv("app/src/data/df_base_score_tema.csv")

create_bar_plot_stacked(df_score_tema, 1)
