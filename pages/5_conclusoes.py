import streamlit as st

st.header("📌 Considerações Finais")
    
st.markdown("""
    **A partir do conjunto de dados utilizado neste trabalho, pode-se concluir que:**
    """)
    
    # Lista de conclusões com marcadores
conclusions = [
        "As duas populações estudadas apresentam perfis distintos de contagem leucocitária, "
        "refletindo provavelmente diferenças em seus ambientes e condições de vida",
        
        "O estado reprodutivo (especialmente a gravidez) demonstra influência significativa "
        "nos parâmetros imunológicos analisados",
        
        "A abordagem de machine learning mostrou-se eficaz para modelar as complexas interações "
        "entre variáveis biológicas, antropométricas e populacionais",
        
        "A inclusão de metadados mais detalhados sobre a população americana poderia enriquecer "
        "as análises comparativas"
    ]
    
for conclusion in conclusions:
    st.markdown(f"- {conclusion}")
    
st.markdown("---")
    
st.subheader("Recomendações para Pesquisas Futuras")
st.markdown("""
    Sugere-se para trabalhos futuros:
    
    1. **Ampliação da amostra**: Incluir outras populações para análise comparativa
    2. **Dados adicionais**: Coletar informações sobre dieta, atividade física e exposição ambiental
    3. **Modelagem avançada**: Explorar técnicas de deep learning para padrões mais complexos
    4. **Estudo longitudinal**: Acompanhar as variações nos parâmetros ao longo do tempo
    """)