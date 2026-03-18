import webbrowser
import streamlit as st
import pandas as pd
from funcao import verificar
import urllib.parse

st.set_page_config(layout="wide")
st.title("Enviar Medida")

df_aluno = pd.read_csv("data/aluno.csv")
df_medidas = pd.read_csv("data/medidas.csv")

if len(df_medidas) > 0:
    aluno_selecionado = st.selectbox("Selecione o Aluno:", verificar(df_aluno, df_medidas))
    df_aluno_selecionado = df_aluno[df_aluno["nome"] == aluno_selecionado]
    aluno_selecionado_id = df_aluno_selecionado["aluno_id"].iloc[0]
    df_medida_selecionada = df_medidas[df_medidas["aluno_id"] == aluno_selecionado_id]

    st.dataframe(df_medida_selecionada[["numero_da_medida", "data_medida", "quadril", "cintura","abdomen", "peitoral", "coxa_esquerda", "coxa_direita", "braco_esquerdo", "braco_direito"]], hide_index=True)

    index = 0
    if len(df_medida_selecionada) > 1:
        medida_numero = st.selectbox("Selecione o número da medida:", df_medida_selecionada["numero_da_medida"].to_list())
        df_medida_selecionada = df_medida_selecionada[df_medida_selecionada["numero_da_medida"] == medida_numero]
        index = df_medida_selecionada.index[0]
    else:
        index = df_medida_selecionada.index[0]

    numero = "55" + str(df_aluno_selecionado['telefone'].iloc[0])
    mensagem = f"""Medida {df_aluno_selecionado['nome'].iloc[0]}
    
    Data da Medida: {df_medidas.loc[index, 'data_medida']}
    Número da Medida: {df_medidas.loc[index, 'numero_da_medida']}
    
    Quadril: {df_medidas.loc[index, 'quadril']} cm
    Cintura: {df_medidas.loc[index, 'cintura']} cm
    Abdômen: {df_medidas.loc[index, 'abdomen']} cm
    Busto/ Peitoral: {df_medidas.loc[index, 'peitoral']} cm
    Coxa Esquerda: {df_medidas.loc[index, 'coxa_esquerda']} cm
    Coxa Direita: {df_medidas.loc[index, 'coxa_direita']} cm
    Braço Esquerdo: {df_medidas.loc[index, 'braco_esquerdo']} cm
    Braço Direito: {df_medidas.loc[index, 'braco_direito']} cm"""

    mensagem = urllib.parse.quote(mensagem)

    link = f"https://wa.me/{numero}?text={mensagem}"

    if st.button(f"Enviar Medidas para {aluno_selecionado}"):
        st.markdown(
        f'<a href="{link}" target="_blank">👉 Enviar pelo WhatsApp</a>',
        unsafe_allow_html=True
    )
        
else:
    st.warning("Cadastre Medidas!")