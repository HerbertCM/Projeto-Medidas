import streamlit as st
import pandas as pd
from dataFrame import df_aluno, df_medida

st.set_page_config(layout="wide")
st.title("Visualizar")

abs1, abs2 = st.tabs(["Alunos", "Medidas"])

with abs1:
    st.dataframe(df_aluno)

with abs2:
    st.dataframe(df_medida)