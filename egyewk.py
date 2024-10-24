import streamlit as st
import pandas as pd

# Exemplo de DataFrame com diferentes tipos de conteúdo (HTML, LaTeX, texto)
data = {
    "Tema": ["Água"],
    "KPI": ["ICA"],
    "Descrição": [
        [
            "<p><b>Calculamos o ICA (Índice do Consumo de Água)</b></p>",
            r"\text{ICA} = \frac{\text{consumo de água}}{\text{consumo ideal de água}}",
            """<ul>
            <li>Se <b>ICA &lt; 1</b>: considera-se o consumo abaixo do ideal, estabeleceu-se que a nota é 10</li>
            <li>Se <b>ICA = 1</b>: considera-se o consumo igual ao ideal, estabeleceu-se que a nota é 9. Ponto (9, 1)</li>
            <li>Se <b>ICA = 1.3</b>: significa que o consumo é até 30% acima do ideal. Estabeleceu-se que a nota é 7. Ponto (7, 1.3)</li>
            <li>Se <b>ICA &gt; 1</b>: significa que a agência está gastando mais do que o ideal, logo será penalizada com notas piores.</li>
            </ul>""",
            "Score Final = -6.67 * ICA + 15.67",
            "<p>Se o ICA for igual a 1, basta substituir na equação acima para calcular o Score Final da agência.</p>",
        ]
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
                # Iterar por cada parte da descrição
                for descricao in row["Descrição"]:
                    # Verificando o tipo de conteúdo
                    if descricao.startswith("<p>") or descricao.startswith(
                        "<ul>"
                    ):  # HTML
                        st.markdown(descricao, unsafe_allow_html=True)
                    elif descricao.startswith(r"\text"):  # LaTeX
                        st.latex(descricao)
                    else:  # Texto simples ou fórmulas como strings
                        st.write(descricao)
