import streamlit as st
import pandas as pd
import re

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
                'NOME-FIADOR': 'Fiador',
                'CATEGORIA': 'Categoria',
                'NOME-EMISSOR': 'Emissor',
                'TIPO-INSTRUMENTO': 'Tipo Instrumento',
                'NOME-INSTRUMENTO': 'Instrumento',
                'DATA-MATURIDADE': 'Data Maturidade',
                'PAGO-POR-EMISSOR': 'Pago por emissor?',
                'RATING': 'Rating',
                'DATA-RATING': 'Data Rating',
                'CLASSIFICACAO-ACAO': 'Ação',
                'PERSPECTIVA-RATING': 'Perspectiva',
                'WATCH-STATUS-RATING': 'Status',
                'TIPO-ANUNCIO': 'Anúncio',
                'TIPO-PRAZO': 'Prazo',
                'TIPO-RATING': 'Tipo',
                'SUBTIPO-RATING': 'Subtipo'
        })

        # Cria a coluna combinada 'Emissor/Fiador'
        df["Emissor/Fiador"] = df["Fiador"].fillna(df["Emissor"])

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

    padrao = re.escape(nome_normalizado)
    regex = re.compile(padrao)
    resultado = df[
    df["Emissor/Fiador"].str.lower().str.contains(regex, na=False) |
    df["Instrumento"].str.lower().str.contains(regex, na=False)
]

    if not resultado.empty:
        st.success(f"✅ {len(resultado)} resultado(s) encontrado(s):")
        tabela = resultado[
            ['Agência', 'Emissor/Fiador', 'Categoria', 'Instrumento', 'Rating', 'Data Rating',
             'Ação', 'Perspectiva', 'Anúncio', 'Tipo', 'Subtipo']]
        
        tabela = tabela.sort_values(by='Data Rating', ascending=False)

        tabela['Instrumento'] = tabela['Instrumento'].replace({None: '', 'None': ''})
        tabela['Data Rating'] = tabela['Data Rating'].dt.strftime('%d/%m/%Y')

        st.dataframe(tabela.fillna(''), hide_index=True, use_container_width=True)
   
    else:
        st.warning("⚠️ Nenhum resultado encontrado para o nome pesquisado.")

elif nome_pesquisado and df.empty:
    st.info("ℹ️ A busca não pôde ser realizada porque os dados não foram carregados.")

# --- RODAPÉ / COMENTÁRIOS FINAIS ---
st.markdown("---")
st.caption("📅 Dados atualizados em: **01 de Junho de 2025**")
st.caption("🔐 Fonte: Base interna consolidada de emissões das agências: Fitch Ratings; S&P Ratings; Moody's Ratings; Austin Ratings; SR Ratings; Bells&Bayes; AM Best Ratings.")
st.caption("⚠️ Algumas fontes só tornam públicas as avaliações de rating 12 meses após a emissão. Considere verificar outras fontes.")