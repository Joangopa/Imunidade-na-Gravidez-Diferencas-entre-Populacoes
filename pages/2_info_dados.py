import streamlit as st
import pandas as pd
from PIL import Image

def show_variables_description():
    """Mostra a descrição das variáveis em formato de lista"""
    st.subheader("Descrição das Variáveis")
    
    var_groups = {
        "Grupo de Variáveis": [
            "Contagem Leucocitária (células/µL)",
            "Dados Antropométricos",
            "Dados Reprodutivos",
            "Metadados"
        ],
        "Variáveis": [
            ["WBC: Leucócitos totais", "NEU: Neutrófilos", "LYM: Linfócitos", 
             "MON: Monócitos", "EOS: Eosinófilos", "BAS: Basófilos"],
            ["BMI: Índice de massa corporal (kg/m²)", "Age: Idade em anos"],
            ["NumPartos: Número de partos", 
             "RepStatus: Status reprodutivo (Cycling: Não grávida. T1, T2, T3: Trimestre da gravidez)"],
            ["Population: Origem populacional (THLHP:Tsimane, NHANES: Mulheres EUA)"]
        ]
    }
    
    df = pd.DataFrame(var_groups)
    
    with st.expander("📋 Detalhes das Variáveis", expanded=True):
        for _, row in df.iterrows():
            st.write(f"**{row['Grupo de Variáveis']}**")
            for item in row['Variáveis']:
                st.write(f"- {item}")
            st.write("")

def show_data_distribution_image():
    """Mostra a imagem com a distribuição dos dados"""
    try:
        image = Image.open("assets/imagem_relacao_gravidas_dados_finais.png")
        st.subheader("Distribuição dos Dados")
        st.image(image, 
                caption="Distribuição por estado reprodutivo e origem populacional",
                use_container_width=True)
    except FileNotFoundError:
        st.warning("Imagem não encontrada no caminho especificado")
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {e}")

def show():
    st.header("📊 Dados e Variáveis")

    st.write("""
    O conjunto de dados considera dois tipos de populações. A primeira delas correspondente a dados de mulheres Tsimane. 
    A segunda fonte de dados corresponde a dados de mulheres morando nos Estados Unidos.  
    A idade das mulheres das duas fontes de dados varia entre 18 e 45 anos.  
    """)
    st.write("""
    Consideramos 6 grupos de variáveis no conjunto de dados distribuídos da seguinte forma:
    """)
    
    # Layout com duas colunas
    col1, col2 = st.columns([3, 2])  # Ajuste a proporção conforme necessário
    
    with col1:
        show_variables_description()
    
    with col2:
        show_data_distribution_image()

# Chamada principal
show()