import pandas as pd
import numpy as np

# Definir o tamanho X (número de linhas)
X = 5


# Função para gerar valores aleatórios para as colunas
def generate_random_values(column_name, num_rows):
    if "AGENCIA" in column_name:
        return [i for i in range(0, num_rows)]
    elif "TEMA" in column_name:
        return np.random.choice(["INFRA CIVIL", "REGULATÓRIO", "SEGURANÇA"], num_rows)
    elif "PILAR" in column_name:
        return np.random.choice(
            ["EFICIÊNCIA", "PERFORMACE", "ESG", "RISCO", "SATISFAÇÃO INTERNA"], num_rows
        )
    elif "SCORE" in column_name:
        return np.random.uniform(0, 10, num_rows).round(2)
    elif "FAROL" in column_name:
        return np.random.choice(["VERDE", "AMARELO", "VERMELHO"], num_rows)
    elif "KPI" in column_name:
        return np.random.choice(["KPI 1", "KPI 2", "KPI 3"], num_rows)
    elif "INTERVALO_MIN" in column_name:
        return np.random.randint(0, 11, num_rows)
    elif "INTERVALO_MAX" in column_name:
        return np.random.randint(0, 11, num_rows)
    else:
        return np.random.choice(["Valor A", "Valor B", "Valor C"], num_rows)


# Criar DataFrames
df_base_score_tema = pd.DataFrame(
    {
        "AGENCIA_TEMA": generate_random_values("AGENCIA", X),
        "TEMA_TEMA": generate_random_values("TEMA", X),
        "PILAR_TEMA": generate_random_values("PILAR", X),
        "SCORE_TEMA": generate_random_values("SCORE", X),
        "FAROL_TEMA": generate_random_values("FAROL", X),
    }
)

df_base_score_pilar = pd.DataFrame(
    {
        "AGENCIA_PILAR": generate_random_values("AGENCIA", X),
        "PILAR_PILAR": generate_random_values("PILAR", X),
        "SCORE_PILAR": generate_random_values("SCORE", X),
        "FAROL_PILAR": generate_random_values("FAROL", X),
    }
)

df_base_score_global = pd.DataFrame(
    {
        "AGENCIA_GLOBAL": generate_random_values("AGENCIA", X),
        "SCORE_GLOBAL": generate_random_values("SCORE", X),
        "FAROL_GLOBAL": generate_random_values("FAROL", X),
    }
)

df_intervalo_score_farol = pd.DataFrame(
    {
        "KPI_INTERVALO": generate_random_values("KPI", X),
        "TEMA_INTERVALO": generate_random_values("TEMA", X),
        "PILAR_INTERVALO": generate_random_values("PILAR", X),
        "INTERVALO_MIN": generate_random_values("INTERVALO_MIN", X),
        "INTERVALO_MAX": generate_random_values("INTERVALO_MAX", X),
        "FAROL_INTERVALO": generate_random_values("FAROL", X),
    }
)

# Ajustar INTERVALO_MAX para ser sempre maior ou igual ao INTERVALO_MIN
df_intervalo_score_farol["INTERVALO_MAX"] = np.maximum(
    df_intervalo_score_farol["INTERVALO_MIN"], df_intervalo_score_farol["INTERVALO_MAX"]
)

# Exibir os DataFrames gerados
print("df_base_score_tema:\n", df_base_score_tema)
print("\ndf_base_score_pilar:\n", df_base_score_pilar)
print("\ndf_base_score_global:\n", df_base_score_global)
print("\ndf_intervalo_score_farol:\n", df_intervalo_score_farol)

df_base_score_tema.to_csv("app/src/data/df_base_score_tema.csv", index=False)
df_base_score_pilar.to_csv("app/src/data/df_base_score_pilar.csv", index=False)
df_base_score_global.to_csv("app/src/data/df_base_score_global.csv", index=False)
df_intervalo_score_farol.to_csv(
    "app/src/data/df_intervalo_score_farol.csv", index=False
)


# Função para gerar valores aleatórios para as colunas
def generate_random_values_base_unica(column_name, num_rows):
    if "CD_PONTO" in column_name:
        return [i for i in range(0, num_rows)]
    elif "UF" in column_name:
        return np.random.choice(
            ["SP", "RJ", "MG", "ES", "BA", "PR", "RS", "SC", "PE", "CE"], num_rows
        )
    elif "MUNICIPIO" in column_name:
        return np.random.choice(
            [
                "São Paulo",
                "Rio de Janeiro",
                "Belo Horizonte",
                "Curitiba",
                "Porto Alegre",
                "Salvador",
            ],
            num_rows,
        )
    elif "FOOTPRINT" in column_name:
        return np.random.choice(["Pequeno", "Médio", "Grande"], num_rows)
    else:
        return np.random.choice(["Valor A", "Valor B", "Valor C"], num_rows)


# Criar DataFrame df_base_unica
df_base_unica = pd.DataFrame(
    {
        "CD_PONTO": generate_random_values_base_unica("CD_PONTO", X),
        "UF": generate_random_values_base_unica("UF", X),
        "MUNICIPIO": generate_random_values_base_unica("MUNICIPIO", X),
        "FOOTPRINT": generate_random_values_base_unica("FOOTPRINT", X),
    }
)

# Exibir o DataFrame gerado
print("df_base_unica:\n", df_base_unica)
df_base_unica.to_excel("app/src/data/df_base_unica.xlsx", index=False)
