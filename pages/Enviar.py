import webbrowser
import streamlit as st
import pandas as pd
from funcao import verificar

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

    numero = "55" + str(df_aluno_selecionado["telefone"].iloc[0])
    mensagem = f"Medida {df_aluno_selecionado["nome"].iloc[0]}%0aData da Medida: {df_medidas.loc[index, "data_medida"]}%0aNúmero da Medida: {df_medidas.loc[index, "numero_da_medida"]}%0a%0aQuadril: {df_medidas.loc[index, "quadril"]} cm%0aCintura: {df_medidas.loc[index, "cintura"]} cm%0aAbdômen: {df_medidas.loc[index, "abdomen"]} cm%0aBusto/ Peitoral: {df_medidas.loc[index, "peitoral"]} cm%0aCoxa Esquerda: {df_medidas.loc[index, "coxa_esquerda"]} cm%0aCoxa Direita: {df_medidas.loc[index, "coxa_direita"]} cm%0aBraço Esquerdo: {df_medidas.loc[index, "braco_esquerdo"]} cm%0aBraço Direito: {df_medidas.loc[index, "braco_direito"]} cm%0a"

    link = f"https://wa.me/{numero}?text={mensagem}"

    if st.button(f"Enviar Medidas para {aluno_selecionado}"):
        st.markdown(
        f'<script>window.open("{link}", "_blank");</script>',
        unsafe_allow_html=True
    )
else:
    st.warning("Cadastre Medidas!")