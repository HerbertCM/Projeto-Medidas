import os
import pandas as pd

caminho = "data/"

if not os.path.exists(caminho):
    os.makedirs(caminho)

if not os.path.exists(caminho + "aluno.csv"):
    aluno = {
        "aluno_id": [],
        "nome": [],
        "telefone": []
    }

    df_aluno = pd.DataFrame(aluno)
    df_aluno.to_csv(caminho + "aluno.csv", index=False)
    print("DataFrame aluno criado com Sucesso!")
else:
    df_aluno = pd.read_csv(caminho + "aluno.csv")
    print("DataFrame aluno carregado com Sucesso!")

if not os.path.exists(caminho + "medidas.csv"):
    medida = {
        "aluno_id": [],
        "data_medida": [],
        "numero_da_medida": [],
        "quadril": [],
        "cintura": [],
        "abdomen": [],
        "peitoral": [],
        "coxa_esquerda": [],
        "coxa_direita": [],
        "braco_esquerdo": [],
        "braco_direito": []
    }
    df_medida = pd.DataFrame(medida)
    df_medida.to_csv(caminho + "medidas.csv", index=False)
    print("DataFrame medida criado com Sucesso!")
else:
    df_medida = pd.read_csv(caminho + "medidas.csv")
    print("DataFrame medida carregado com Sucesso!")