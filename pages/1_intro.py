import streamlit as st

def show():
    st.header("Introdução ao Problema")
    
    st.write("""
    Este estudo analisa como diferentes ambientes moldam a imunidade materna durante a gravidez, 
        comparando populações expostas a níveis contrastantes de microrganismos.
    """)
   
    st.write("""
    👩🏽‍🦱 Mulheres Tsimane, de uma comunidade indígena na floresta boliviana, com alta exposição a patógenos naturais e fertilidade tradicional.
    
    👩🏼 Mulheres nos EUA, vivendo em ambiente urbano com baixa exposição microbiana.

    O foco está na análise de seis tipos de células imunológicas:

    Leucócitos totais (WBC)

    Linfócitos

    Neutrófilos

    Monócitos

    Eosinófilos

    Basófilos
    """)

# Chamada da função principal da aba
show()