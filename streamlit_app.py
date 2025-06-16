import streamlit as st
import pandas as pd

# --- CONFIGURAÇÕES DA PÁGINA ---

def page_config():
    st.set_page_config(page_title="Consulta de Rating de Emissores e Emissões", layout='wide')

page_config()

# --- TÍTULO ---
st.title("🔍 Consulta Rating de Emissores e Emissões")

# --- FUNÇÃO: CARREGAMENTO SEGURO DOS DADOS ---
@st.cache_data(show_spinner="Carregando dados...")
def carregar_dados():
    try:
        df_raw = pd.read_parquet("202506-Emissoes-Consolidado.parquet")

        # Renomeia as colunas para nomes mais amigáveis
        df = df_raw.rename(columns={
            'AGENCIA': 'Agência',
            'NOME-FIADOR': 'Emissor/Fiador',
            'CATEGORIA': 'Categoria',
            'RATING': 'Rating',
            'DATA-RATING': 'Data Emissão',
            'CLASSIFICACAO-ACAO': 'Ação',
            'PERSPECTIVA-RATING': 'Perspectiva',
            'TIPO-ANUNCIO': 'Anúncio',
            'TIPO-PRAZO': 'Prazo',
            'TIPO-RATING': 'Tipo',
            'SUBTIPO-RATING': 'Subtipo'
        })

        # Remove linhas com valores ausentes no campo de busca
        df = df.dropna(subset=["Emissor/Fiador"])

        return df

    except FileNotFoundError:
        st.error("❌ Arquivo de dados não encontrado.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()

# --- CARREGAR OS DADOS ---
df = carregar_dados()

# --- CAMPO DE BUSCA ---
nome_pesquisado = st.text_input("Insira o nome da empresa:")

# --- CONSULTA ---
if nome_pesquisado and not df.empty:
    nome_normalizado = nome_pesquisado.lower().strip()

    resultado = df[df["Emissor/Fiador"].str.lower().str.contains(nome_normalizado)]

    if not resultado.empty:
        st.success(f"✅ {len(resultado)} resultado(s) encontrado(s):")
        tabela = resultado[
            ['Agência', 'Emissor/Fiador', 'Categoria', 'Rating', 'Data Emissão',
             'Ação', 'Perspectiva', 'Anúncio', 'Tipo', 'Subtipo']]
        tabela = tabela.sort_values(by='Data Emissão', ascending=False)
        tabela['Data Emissão'] = tabela['Data Emissão'].dt.strftime('%Y-%m-%d')

        st.dataframe(tabela, hide_index=True, use_container_width=True)
   
    else:
        st.warning("⚠️ Nenhum resultado encontrado para o nome pesquisado.")

elif nome_pesquisado and df.empty:
    st.info("ℹ️ A busca não pôde ser realizada porque os dados não foram carregados.")

# --- RODAPÉ / COMENTÁRIOS FINAIS ---
st.markdown("---")
st.caption("📅 Dados atualizados em: **Junho de 2025**")
st.caption("🔐 Fonte: Base interna consolidada de emissões das agências Fitch Ratings, S&P Ratings e Moody's Ratings.")
