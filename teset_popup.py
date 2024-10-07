import pandas as pd
import random

# Lista de UFs
ufs = ["SP", "RJ", "MG", "ES", "BA", "PE", "CE", "RS", "PR", "SC", "DF"]

# Lista de temas
temas = ["RISCOS", "PERFORMANCE", "ESG"]


# Função para gerar pontuação aleatória
def generate_score():
    return round(random.uniform(0, 100), 2)


# Gerar dados
data = []
for uf in ufs:
    for tema in temas:
        data.append([uf, tema, generate_score()])

# Criar DataFrame
df = pd.DataFrame(data, columns=["UF", "TEMA", "SCORE"])
# Criar um novo dataframe com os temas como colunas separadas
df_pivot = df.pivot(index="UF", columns="TEMA", values="SCORE").reset_index()

df_pivot.to_excel("df.xlsx", index=False)
