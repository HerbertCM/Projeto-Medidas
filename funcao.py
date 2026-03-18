import pandas as pd
from dataFrame import df_aluno, df_medida

def verificar(df1, df2):
    lista_ids = df1["aluno_id"].to_list()
    lista_contem = []

    for aluno_id in lista_ids:
        if aluno_id in df2["aluno_id"].values:
            df_aluno_nome = df1[df1["aluno_id"] == aluno_id]
            nome = df_aluno_nome["nome"].iloc[0]
            lista_contem.append(nome)
    
    return lista_contem