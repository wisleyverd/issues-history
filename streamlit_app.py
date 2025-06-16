import streamlit as st
import pandas as pd

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Consulta de Emissores e Emissões", layout="centered")

# --- TÍTULO ---
st.title("🔍 Consulta")

# --- CAMPO DE BUSCA ---
nome_pesquisado = st.text_input("Digite o nome da empresa para buscar:")

# --- CARREGAR BASE (Parquet ou CSV) ---
@st.cache_data
def carregar_dados():
    return pd.read_parquet("202506-Emissoes-Consolidado.parquet")

df = carregar_dados()

# --- CONSULTA ---
if nome_pesquisado:
    # Filtro que ignora maiúsculas/minúsculas
    resultado = df[df['NOME-FIADOR'].str.lower().str.contains(nome_pesquisado.lower())]

    if not resultado.empty:
        st.success(f"{len(resultado)} nome(s) encontrado(s):")
        st.write(resultado[['AGENCIA', 'NOME-FIADOR', 'CATEGORIA']])
    else:
        st.warning("Nenhum nome encontrado.")
