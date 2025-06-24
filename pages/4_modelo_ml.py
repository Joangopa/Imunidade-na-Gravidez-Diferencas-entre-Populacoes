import streamlit as st
import pandas as pd
from PIL import Image
from joblib import load


modelo_path = 'model/modelo_gradient_boosting.pkl'
scaler_path = 'model/scaler.pkl'

modelo = load(modelo_path)
scaler = load(scaler_path)

st.header("🤖 Modelo de Aprendizado de Máquina")

paragrafo_resumo = """
A escolha do modelo de regressão para estimar os níveis de neutrófilos (NEU) é estratégica por utilizar variáveis acessíveis e de baixo custo: 
contagem de leucócitos (WBC), Índice de Massa Corporal (IMC), idade, histórico reprodutivo e grupo populacional. Essas variáveis capturam 
importantes influências biológicas, oferecendo uma solução custo-efetiva para estimar NEU, ideal para triagens e monitoramento em locais com recursos limitados.
"""

# Carregando a imagem
img_corr = Image.open("assets/matiz_correlacao_ml.png")

# Criando as colunas
col1, col2 = st.columns(2)

with col1:
    st.write(paragrafo_resumo)

with col2:
    st.image(img_corr, caption="Matriz de Correlação para Features do Modelo")

# 1. Função para mostrar o reporte do modelo
def show_model_report():
    st.subheader("Desempenho do Modelo GradientBoosting Regressor")
    
   
    
    # Visualizações
    col1, col2 = st.columns(2)
    
    with col1:
         # Métricas do modelo
        st.write("""
        Métricas de Avaliação do Modelo:
        | Métrica       | Valor       |
        |---------------|-------------|
        | MAE           | 616.030     |
        | R²            | 0.802       |
        | R²-ajustado   | 0.799       |
        """)
            
    
    
    with col2:
        try:
            img_pred = Image.open("assets/real_vs_predict_regressao.png")
            st.image(img_pred, caption="Valores Reais vs. Preditos pelo Modelo")
        except FileNotFoundError:
            st.warning("Imagem de predições não encontrada")
    
    try:
        img_feat = Image.open("assets/impato_variaveis_modelo.png")
        st.image(img_feat, caption="Importância das Variáveis no Modelo", width=700)
    except FileNotFoundError:
        st.warning("Imagem de importância de variáveis não encontrada")

# 2. Função para coletar inputs do usuário
def get_user_inputs():
    st.subheader("Simulador de Predição")
    st.write("Preencha os dados para gerar a predição:")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            wbc = st.number_input("Contagem total de leucócitos (WBC)", 
                                min_value=0, max_value=22000, value=7000)
            population = st.selectbox("População", 
                                   ["Tsimane", "Americano"], 
                                   index=0)
            rep_status = st.selectbox("Trimestre da gravidez", 
                                    ["0 - Não grávida", 
                                     "1 - Primeiro trimestre", 
                                     "2 - Segundo trimestre", 
                                     "3 - Terceiro trimestre"], 
                                    index=0)
        
        with col2:
            bmi = st.number_input("Índice de massa corporal (BMI)", 
                                min_value=10.0, max_value=50.0, value=24.0, step=0.1)
            age = st.number_input("Idade", 
                                min_value=15, max_value=80, value=30)
            num_partos = st.number_input("Número de partos", 
                                       min_value=0, max_value=20, value=1)
        
        submitted = st.form_submit_button("Gerar Predição")
    
    return submitted, {
        'WBC': wbc,
        'BMI': bmi,
        'Age': age,
        'NumPartos': num_partos,
        'Population': population,
        'RepStatus': rep_status
    }

# 3. Função para criar o dataframe de input
def create_input_dataframe(inputs):
    input_data = {
        'WBC': [inputs['WBC']],
        'BMI': [inputs['BMI']],
        'Age': [inputs['Age']],
        'NumPartos': [inputs['NumPartos']],
        'Population_bin': [1 if inputs['Population'] == "Americano" else 0],
        'RepStatus_cat': [int(inputs['RepStatus'][0])],
        'RepStatus_bin': [0 if inputs['RepStatus'].startswith("0") else 1]
    }
    return pd.DataFrame(input_data)

# 4. Função para mostrar resultados
def show_results(input_df):
    #st.subheader("Dados de Input Criados")
    #st.dataframe(input_df)
    
    if modelo is not None and scaler is not None:
        try:
            # Aplicar o scaler
            scaled_input = scaler.transform(input_df)
            
            # Fazer a predição
            prediction = modelo.predict(scaled_input)[0]
            
            # Mostrar resultado
            st.subheader("Resultado da Predição")
            st.metric(label="Contagem estimada de neutrófilos (NEU)", 
                     value=f"{prediction:.2f}")
            
            # Explicação adicional
            st.info("""
            **Interpretação:**  
            Este valor representa a contagem estimada de neutrófilos (células/μL) no sangue 
            com base nos parâmetros fornecidos.
            """)
            
        except Exception as e:
            st.error(f"Erro ao processar a predição: {str(e)}")
    else:
        st.error("Modelo ou scaler não carregados corretamente!")

    
# Função principal da aba
def show():
    
    
    # Seção 1: Reporte do Modelo
    show_model_report()
    
    # Divisão
    st.markdown("---")
    
    # Seção 2: Inputs e Predição
    submitted, user_inputs = get_user_inputs()
    
    if submitted:
        input_df = create_input_dataframe(user_inputs)
        show_results(input_df)

# Chamada da função principal
show()