import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Análise de Dados e Modelo ML",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center;'>Imunidade na Gravidez: Diferenças entre Populações Tsimane e Estadounidense</h1>", 
            unsafe_allow_html=True)

# Centralizar a imagem usando colunas
col1, col2, col3 = st.columns([1, 2, 1])  # A coluna do meio é mais larga
with col2:
    st.image("assets/imagem_titulo.png", 
            caption="Ilustração do problema",
            width=500)