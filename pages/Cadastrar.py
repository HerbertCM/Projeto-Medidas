import pandas as pd
import streamlit as st
import dataFrame
from datetime import datetime
from funcao import verificar
import time
import re

df_aluno = pd.read_csv("data/aluno.csv")
df_medida = pd.read_csv("data/medidas.csv")

st.set_page_config(layout="wide")
st.title("Cadastrar, editar e excluir")

tabs1, tabs2 = st.tabs(["Aluno", "Medida"])

with tabs1:
    abs1, abs2, abs3 = st.tabs(["Cadastrar Aluno", "Editar Aluno", "Excluir Aluno"])
    with abs1:
        st.markdown("<h3>Cadastrar Aluno:</h3>", unsafe_allow_html=True)
        id = len(df_aluno) + 1
        nome = st.text_input("Nome:")
        telefone = st.text_input("Telefone (ex: 27999999999):")

        if st.button("Salvar Aluno"):
            if nome in df_aluno["nome"].values:
                st.error("Aluno já Cadastrado!")
                time.sleep(3)
                st.rerun()

            if not re.fullmatch(r"\d{10,11}", str(telefone)):
                st.error("Telefone deve ter 10 ou 11 números (DDD + número)!")
            else:
                novo_aluno = {
                    "aluno_id": id,
                    "nome": nome,
                    "telefone": telefone
                }

                df_aluno = pd.concat([df_aluno, pd.DataFrame([novo_aluno])], ignore_index=True)
                df_aluno.to_csv("data/aluno.csv", index=False)

                st.success("Aluno salvo com Sucesso!")
                time.sleep(3)
                st.rerun()
    
    with abs2:
        if len(df_aluno) > 0:
            st.markdown("<h3>Editar Aluno:</h3>", unsafe_allow_html=True)
            nome_selecionado = st.selectbox("Selecione o Aluno:", df_aluno["nome"].to_list())
            df_selecionado = df_aluno[df_aluno["nome"] == nome_selecionado]
            st.dataframe(df_selecionado[["nome", "telefone"]], hide_index=True)

            novo_nome = st.text_input("Novo Nome:", value=nome_selecionado)
            novo_telefone = st.text_input("Novo Telefone:", value=df_selecionado["telefone"].iloc[0])

            if st.button("Salvar Edições"):
                if not re.fullmatch(r"\d{10,11}", str(novo_telefone)):
                    st.error("Telefone deve ter 10 ou 11 números (DDD + número)!")
                else:
                    index = df_selecionado.index[0]
                    df_aluno.loc[index, "nome"] = novo_nome
                    df_aluno.loc[index, "telefone"] = novo_telefone

                    df_aluno.to_csv("data/aluno.csv", index=False)
                    st.success("Dados alterados com Sucesso!")
                    time.sleep(3)
                    st.rerun()
        else:
            st.warning("Cadastre Alunos!")
    
    with abs3:
        if len(df_aluno) > 0:
            st.markdown("<h3>Excluir Aluno:</h3>", unsafe_allow_html=True)
            nome_selecionado = st.selectbox("Selecione o Aluno para Exlusão:", df_aluno["nome"].to_list())
            df_selecionado = df_aluno[df_aluno["nome"] == nome_selecionado]
            st.dataframe(df_selecionado[["nome", "telefone"]], hide_index=True)

            if "confirmar_exclusao" not in st.session_state:
                st.session_state.confirmar_exclusao = False

            if st.button(f"Excluir {nome_selecionado}"):
                st.session_state.confirmar_exclusao = True

            if st.session_state.confirmar_exclusao:
                st.warning(f"Todos os dados de {nome_selecionado} serão apagados! Deseja continuar?")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Sim"):
                        df_aluno_excluir = df_aluno[df_aluno["nome"] != nome_selecionado]
                        df_aluno_id = df_aluno[df_aluno["nome"] == nome_selecionado]
                        df_medida_excluir = df_medida[df_medida["aluno_id"] != df_aluno_id["aluno_id"].iloc[0]]

                        df_aluno_excluir.to_csv("data/aluno.csv", index=False)
                        df_medida_excluir.to_csv("data/medidas.csv", index=False)

                        st.success(f"Dados de {nome_selecionado} excluídos com Sucesso!")
                        st.session_state.confirmar_exclusao = False
                        time.sleep(3)
                        st.rerun()
                with col2:
                    if st.button("Não"):
                        st.session_state.confirmar_exclusao = False
                        st.rerun()
        else:
            st.warning("Cadastre Alunos!")

with tabs2:
    abs1, abs2, abs3 = st.tabs(["Cadastrar Medida", "Editar Medida", "Excluir Medida"])

    with abs1:
        if len(df_aluno) > 0:
            st.markdown("<h3>Cadastrar Medida:</h3>", unsafe_allow_html=True)
            aluno_selecionado = st.selectbox("Selecione o Aluno:", df_aluno["nome"].to_list(), key="medida")

            quadril = st.number_input("Quadril:", min_value=0, step=1)
            cintura = st.number_input("Cintura:", min_value=0, step=1)
            abdomen = st.number_input("Abdômen:", min_value=0, step=1)
            peitoral = st.number_input("Busto/ Peitoral:", min_value=0, step=1)
            coxa_esquerda = st.number_input("Coxa Esquerda:", min_value=0, step=1)
            coxa_direita = st.number_input("Coxa Direita:", min_value=0, step=1)
            braco_esquerdo = st.number_input("Braço Esquerdo:", min_value=0, step=1)
            braço_direito = st.number_input("Braço Direito:", min_value=0, step=1)

            if st.button("Salvar Medida"):
                df_selecionado = df_aluno[df_aluno["nome"] == aluno_selecionado]
                aluno_selecionado_id = df_selecionado["aluno_id"].iloc[0]

                data_atual  = datetime.now().strftime("%d/%m/%Y")

                numero_medidas = len(df_medida[df_medida["aluno_id"] == aluno_selecionado_id]) + 1

                nova_medida = {
                    "aluno_id": aluno_selecionado_id,
                    "data_medida": data_atual,
                    "numero_da_medida": numero_medidas,
                    "quadril": quadril,
                    "cintura": cintura,
                    "abdomen": abdomen,
                    "peitoral": peitoral,
                    "coxa_esquerda": coxa_esquerda,
                    "coxa_direita": coxa_direita,
                    "braco_esquerdo": braco_esquerdo,
                    "braco_direito": braço_direito
                }

                df_medida = pd.concat([df_medida, pd.DataFrame([nova_medida])], ignore_index=True)
                df_medida.to_csv("data/medidas.csv", index=False)

                st.success("Medidas salvas com Sucesso!")
                time.sleep(3)
                st.rerun()
        else:
            st.warning("Cadastre Alunos!")
    
    with abs2:
        if len(df_medida) > 0:
            st.markdown("<h3>Editar Medida:</h3>", unsafe_allow_html=True)
            aluno_selecionado = st.selectbox("Selecione o Aluno", verificar(df_aluno, df_medida), key="editar")
            df_selecionado = df_aluno[df_aluno["nome"] == aluno_selecionado]
            aluno_selecionado_id = df_selecionado["aluno_id"].iloc[0]
            df_medida_selecionada = df_medida[df_medida["aluno_id"] == aluno_selecionado_id]

            st.dataframe(df_medida_selecionada[["numero_da_medida", "data_medida", "quadril", "cintura","abdomen", "peitoral", "coxa_esquerda", "coxa_direita", "braco_esquerdo", "braco_direito"]], hide_index=True)

            index = 0
            if len(df_medida_selecionada) > 1:
                numero_medida = st.selectbox("Selecione o número da medida:", df_medida_selecionada["numero_da_medida"].to_list())
                medida_index = df_medida_selecionada[df_medida_selecionada["numero_da_medida"] == numero_medida]
                index = medida_index.index[0]
            else:
                index = df_medida_selecionada.index[0]
            
            data_convertida = datetime.strptime(df_medida.loc[index, "data_medida"], "%d/%m/%Y")

            nova_data = st.date_input("Selecione a Data:", value=data_convertida)
            novo_quadril = st.number_input("Nova medida de Quadril:", min_value=0, step=1, value=df_medida.loc[index, "quadril"])
            nova_cintura = st.number_input("Nova medida de Cintura:", min_value=0, step=1, value=df_medida.loc[index, "cintura"])
            novo_abdomen = st.number_input("Nova medida de Abdômen:", min_value=0, step=1, value=df_medida.loc[index, "abdomen"])
            novo_peitoral = st.number_input("Nova medida de Busto/ Peitoral:", min_value=0, step=1, value=df_medida.loc[index, "peitoral"])
            nova_coxa_esquerda = st.number_input("Nova medida de Coxa Esquerda:", min_value=0, step=1, value=df_medida.loc[index, "coxa_esquerda"])
            nova_coxa_direita = st.number_input("Nova medida de Coxa Direita:", min_value=0, step=1, value=df_medida.loc[index, "coxa_direita"])
            novo_braco_esquerdo = st.number_input("Nova medida de Braço Esquerdo:", min_value=0, step=1, value=df_medida.loc[index, "braco_esquerdo"])
            novo_braço_direito = st.number_input("Nova medida de Braço Direito:", min_value=0, step=1, value=df_medida.loc[index, "braco_direito"])

            if st.button("Salvar nova Medida"):
                data_formatada = nova_data.strftime("%d/%m/%Y")
                df_medida.loc[index, "data_medida"] = data_formatada
                df_medida.loc[index, "quadril"] = novo_quadril
                df_medida.loc[index, "cintura"]  = nova_cintura
                df_medida.loc[index, "abdomen"] = novo_abdomen
                df_medida.loc[index, "peitoral"] = novo_peitoral
                df_medida.loc[index, "coxa_esquerda"] = nova_coxa_esquerda
                df_medida.loc[index, "coxa_direita"] = nova_coxa_direita
                df_medida.loc[index, "braco_esquerdo"] = novo_braco_esquerdo
                df_medida.loc[index, "braco_direito"] = novo_braço_direito

                df_medida.to_csv("data/medidas.csv", index=False)
                st.success("Medidas editadas com Sucesso!")
                time.sleep(3)
                st.rerun()
        else:
            st.warning("Cadastre Medidas!")

    with abs3:
        if len(df_medida) > 0:
            st.markdown("<h3>Excluir Medida:</h3>", unsafe_allow_html=True)
            aluno_selecionado = st.selectbox("Selecione o Aluno:", verificar(df_aluno, df_medida), key="excluir1")
            df_selecionado = df_aluno[df_aluno["nome"] == aluno_selecionado]
            aluno_selecionado_id = df_selecionado["aluno_id"].iloc[0]
            df_medida_selecionada = df_medida[df_medida["aluno_id"] == aluno_selecionado_id]

            st.dataframe(df_medida_selecionada[["numero_da_medida", "data_medida", "quadril", "cintura","abdomen", "peitoral", "coxa_esquerda", "coxa_direita", "braco_esquerdo", "braco_direito"]], hide_index=True)

            index = 0
            numero_medida = 1
            if len(df_medida_selecionada) > 1:
                numero_medida = st.selectbox("Selecione o número da medida que deseja excluir:", df_medida_selecionada["numero_da_medida"].to_list(), key="excluir2")
                medida_index = df_medida_selecionada[df_medida_selecionada["numero_da_medida"] == numero_medida]
                index = medida_index.index[0]
            else:
                index = df_medida_selecionada.index[0]

            if "confirmar_exclusao" not in st.session_state:
                    st.session_state.confirmar_exclusao = False
            
            if st.button("Excluir medida"):
                st.session_state.confirmar_exclusao = True


            if st.session_state.confirmar_exclusao:
                st.warning(f"Confirmar a exclusão da medida {numero_medida}?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Sim", key="confirmar"):
                        df_medida.drop(index, inplace=True)
                        df_medida_selecionada = df_medida[df_medida["aluno_id"] == aluno_selecionado_id]
                        for n in range(len(df_medida_selecionada)):
                            index = df_medida_selecionada.index[n]
                            df_medida.loc[index, "numero_da_medida"] = n + 1
                        
                        df_medida.to_csv("data/medidas.csv", index=False)
                        
                        st.session_state.confirmar_exclusao = False

                        st.success("Medida excluída com Sucesso!")
                        time.sleep(3)
                        st.rerun()

                with col2:
                    if st.button("Não", key="cancelar"):
                        st.session_state.confirmar_exclusao = False
                        st.rerun()
        else:
            st.warning("Cadastre Medidas!")