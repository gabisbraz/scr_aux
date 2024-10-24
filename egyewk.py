import streamlit as st
import pandas as pd

# Exemplo de DataFrame
data = {
    "Tema": ["Água", "Água", "Energia", "Energia"],
    "KPI": ["ICA", "Consumo", "Eficiência", "Custo"],
    "Descrição": [
        """<p><b>Calculamos o ICA (Índice do Consumo de Água)</b></p>

<p><i>ICA = consumo de água / consumo ideal de água</i></p>

<ul>
    <li>Se <b>ICA &lt; 1</b>: considera-se o consumo abaixo do ideal, estabeleceu-se que a nota é 10</li>
    <li>Se <b>ICA = 1</b>: considera-se o consumo igual ao ideal, estabeleceu-se que a nota é 9. Ponto (9, 1)</li>
    <li>Se <b>ICA = 1.3</b>: significa que o consumo é até 30% acima do ideal. Estabeleceu-se que a nota é 7. Ponto (7, 1.3)</li>
    <li>Se <b>ICA &gt; 1</b>: significa que a agência está gastando mais do que o ideal, logo será penalizada com notas piores.</li>
</ul>

<p>Sabemos que o consumo e as suas respectivas notas têm uma relação linear, logo, pegamos os dois pontos conhecidos <b>(9, 1)</b> e <b>(7, 1.3)</b> e encontramos a equação que generaliza essa relação:</p>

<p><b>Score Final = -6.67 * ICA + 15.67</b></p>

<p>Se o ICA for igual a 1, basta substituir na equação acima para calcular o Score Final da agência.</p>
""",
        "O consumo de água mensal foi analisado em relação ao benchmark.",
        "Eficiência energética medida pelo uso de renováveis.",
        "Cálculo de custos de energia com base nas tarifas.",
    ],
}

df = pd.DataFrame(data)

# Criando as Tabs baseadas em cada Tema
temas = list(df["Tema"].unique())
tb = st.tabs(temas)
for i, tema in enumerate(temas):

    with tb[i]:
        # Filtrando os KPIs do tema atual
        df_tema = df[df["Tema"] == tema]

        for _, row in df_tema.iterrows():
            with st.expander(row["KPI"]):
                st.latex(
                    r"""
\text{ICA} = \frac{\text{consumo de água}}{\text{consumo ideal de água}}
"""
                )
                st.markdown(row["Descrição"], unsafe_allow_html=True)
