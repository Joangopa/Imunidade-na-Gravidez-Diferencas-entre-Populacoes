import streamlit as st
import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from joblib import load


# Configuração da página
st.set_page_config(
    page_title="Imunidade na Gravidez",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CRIAR ABAS ---
aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
    "📌", 
    "🧬 Introdução", 
    "📊 Conjunto de dados", 
    "📈 Análises", 
    "🤖 Estimando Neutrófilos",
    "📌 Considerações Finais"
])


# --- Aba 1: Introdução com imagem do título ---
with aba1:

    st.markdown("<h1 style='text-align: center;'>Imunidade na Gravidez: Diferenças entre Populações Tsimane e Estadounidense</h1>", 
            unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])  # Centralizar a imagem
    with col2:
        st.image("assets/imagem_titulo.png", 
                 caption="Ilustração do problema",
                 width=400)

# --- Aba 2: Texto e imagem com tipos celulares ---
with aba2:
    st.header("Introdução ao Problema")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.write("""
            Este estudo analisa como diferentes ambientes moldam a imunidade materna durante a gravidez, 
            comparando populações expostas a níveis contrastantes de microrganismos.
        """)

        st.write("""
            👩🏽‍🦱 Mulheres Tsimane, de uma comunidade indígena na floresta boliviana, com alta exposição a patógenos naturais e fertilidade tradicional.

            👩🏼 Mulheres nos EUA, vivendo em ambiente urbano com baixa exposição microbiana.

            O foco está na análise de seis tipos de células imunológicas:
        """)

        col_esq, col_dir = st.columns(2)
        with col_esq:
            st.markdown("- **Leucócitos totais**")
            st.markdown("- **Linfócitos**")
            st.markdown("- **Neutrófilos**")

        with col_dir:
            st.markdown("- **Monócitos**")
            st.markdown("- **Eosinófilos**")
            st.markdown("- **Basófilos**")

    with col2:
        st.image("assets/imagem_tipo_celulas.png", 
                 caption="Tipos de Células Imunológicas e função",
                 use_container_width=True)


# --- Aba 3 ---
with aba3:
    st.header("📊 Dados e Variáveis")

    st.write("""
    O conjunto de dados considera dois tipos de populações. A primeira delas corresponde a dados de mulheres Tsimane.  
    A segunda fonte de dados corresponde a dados de mulheres morando nos Estados Unidos.  
    A idade das mulheres das duas fontes de dados varia entre 18 e 45 anos.
    """)
    
    st.write("Consideramos 6 grupos de variáveis no conjunto de dados distribuídos da seguinte forma:")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Descrição das Variáveis")

        st.markdown("**Contagem Leucocitária (células/µL)**")
        st.markdown("- WBC: Leucócitos totais")
        st.markdown("- NEU: Neutrófilos")
        st.markdown("- LYM: Linfócitos")
        st.markdown("- MON: Monócitos")
        st.markdown("- EOS: Eosinófilos")
        st.markdown("- BAS: Basófilos")

        st.markdown("**Dados Antropométricos**")
        st.markdown("- BMI: Índice de massa corporal (kg/m²)")
        st.markdown("- Age: Idade em anos")

        st.markdown("**Dados Reprodutivos**")
        st.markdown("- NumPartos: Número de partos")
        st.markdown("- RepStatus: Status reprodutivo (Cycling: Não grávida. T1, T2, T3: Trimestre da gravidez)")

        st.markdown("**Metadados**")
        st.markdown("- Population: Origem populacional (THLHP: Tsimane, NHANES: Mulheres EUA)")

    with col2:
        st.subheader("Distribuição dos Dados")

        try:
            image = Image.open("assets/imagem_relacao_gravidas_dados_finais.png")
            st.image(image, 
                     caption="Distribuição por estado reprodutivo e origem populacional",
                     use_container_width=True)
        except FileNotFoundError:
            st.warning("Imagem não encontrada no caminho especificado")
        except Exception as e:
            st.error(f"Erro ao carregar a imagem: {e}")

# --- Aba 4: Análises ---
with aba4:
    st.header("📈 Análise de Dados de Imunidade")

    @st.cache_data
    def load_data():
        data = pd.read_csv('assets/Hove_et_al_2020.csv')
        cond = (
            (data.WBC < 22000) &
            (data.NEU < 15000) &
            (data.LYM < 8000) &
            (data.MON < 1250) &
            (data.BAS < 400) &
            (data.EOS < 5000)
        )
        return data.loc[cond]

    dados = load_data()

    col1, col2 = st.columns(2)

    # --- HISTOGRAMAS ---
    with col1:
        st.subheader("Distribuição das Contagens Celulares na População Geral")
        variaveis = ['WBC', 'NEU', 'LYM', 'MON', 'BAS', 'EOS']
        fig1, axes = plt.subplots(2, 3, figsize=(12, 8))
        sns.set(style="whitegrid")
        sns.set_context("notebook", font_scale=1.2)

        for ax, var in zip(axes.flat, variaveis):
            sns.histplot(data=dados, x=var, kde=True, bins=30, color='skyblue', ax=ax)
            ax.set_title(f'Distribuição de {var}', fontsize=14)
            ax.set_xlabel(f'{var} (cells/μL)', fontsize=12)
            ax.set_ylabel('Frequência', fontsize=12)

        plt.tight_layout()
        st.pyplot(fig1)

    # --- GRÁFICO VIOLINO ---
    with col2:
        st.subheader("Comparação por Status Reprodutivo e População")
        cell_types = ['WBC', 'NEU', 'LYM', 'MON', 'BAS', 'EOS']
        dados_long = dados.melt(
            id_vars=['RepStatus', 'Population'],
            value_vars=cell_types,
            var_name='Cell_Type',
            value_name='Cell_Count'
        )

        repstatus_order = ['Cycling', 'T1', 'T2', 'T3']
        population_order = ['NHANES', 'THLHP']

        dados_long['RepStatus'] = pd.Categorical(dados_long['RepStatus'], categories=repstatus_order, ordered=True)
        dados_long['Population'] = pd.Categorical(dados_long['Population'], categories=population_order, ordered=True)
        dados_long['Cell_Type'] = pd.Categorical(dados_long['Cell_Type'], categories=cell_types, ordered=True)

        fig2, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        for i, cell_type in enumerate(cell_types):
            ax = axes[i]
            subset = dados_long[dados_long['Cell_Type'] == cell_type]

            sns.violinplot(
                data=subset,
                x='RepStatus',
                y='Cell_Count',
                hue='Population',
                split=True,
                inner=None,
                palette='Set1',
                order=repstatus_order,
                hue_order=population_order,
                ax=ax
            )

            # Adiciona média
            for j, status in enumerate(repstatus_order):
                for k, pop in enumerate(population_order):
                    pop_data = subset[(subset['RepStatus'] == status) & (subset['Population'] == pop)]
                    mean_val = pop_data['Cell_Count'].mean()
                    offset = -0.05 if pop == 'NHANES' else 0.05
                    ax.scatter(j + offset, mean_val, color='black', s=50, marker='o', zorder=10,
                               edgecolor='white', linewidth=0.8)

            ax.set_title(cell_type, fontsize=14)
            ax.set_xlabel("Status Reprodutivo", fontsize=12)
            ax.set_ylabel("cells/μL", fontsize=12)

            if i == 0:
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles, labels, title='População', fontsize=10, title_fontsize=11)
            else:
                ax.get_legend().remove()

        plt.tight_layout()
        st.pyplot(fig2)

    # --- IMAGENS FINAIS ---
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Resultados do teste U: Grupos com Menores Contagens")
        st.image("assets/imagem_tabela_menor_contagem.png", 
                 caption="População com menor contagem média para cada tipo celular",
                 width=500)

    with col4:
        st.subheader("K-means e PCA: Separação Populacional")
        st.image("assets/agrupamentos_pca.png", 
                 caption="Agrupamentos K-means com projeção PCA",
                 width=500)
        
# --- Aba 5: modelo ML ---
with aba5:
    st.header("🤖 Modelo de Aprendizado de Máquina")

    modelo = load("model/modelo_gradient_boosting.pkl")
    scaler = load("model/scaler.pkl")

    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        A escolha de um modelo de regressão para estimar os níveis de neutrófilos (NEU) resulta ser estratégica por utilizar variáveis acessíveis e de baixo custo: 
        contagem de leucócitos (WBC), IMC, idade, histórico reprodutivo e grupo populacional.
        """)
        st.write("""
        O modelo escolhido a partir de metricas como MAE e R²-ajustado, é o GradientBoosting Regressor.
        """)

        st.write("""
        | Métrica       | Valor       |
        |---------------|-------------|
        | MAE           | 616.030     |
        | R²            | 0.802       |
        | R²-ajustado   | 0.799       |
        """)

    with col2:
        st.image("assets/matiz_correlacao_ml.png", caption="Matriz de Correlação para as Variáveis Preditoras do Modelo de Regressão", use_container_width=True)

    st.markdown("---")
    st.subheader("Desempenho do Modelo GradientBoosting Regressor")

    col3, col4 = st.columns(2)
    with col3:
        st.image("assets/impato_variaveis_modelo.png", caption="Importância das Variáveis no Modelo", use_container_width=True)
    with col4:
        st.image("assets/real_vs_predict_regressao.png", caption="Valores Reais vs. Preditos pelo Modelo", use_container_width=True)

    #st.image("assets/impato_variaveis_modelo.png", caption="Importância das Variáveis no Modelo", width=700)

    st.markdown("---")
    st.subheader("Simulador de Predição")
    st.write("Preencha os dados para gerar a predição:")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            wbc = st.number_input("Contagem total de leucócitos (WBC)", 0, 22000, 7000)
            population = st.selectbox("População", ["Tsimane", "Americano"])
            rep_status = st.selectbox("Trimestre da gravidez", [
                "0 - Não grávida", "1 - Primeiro trimestre", "2 - Segundo trimestre", "3 - Terceiro trimestre"])
        with col2:
            bmi = st.number_input("Índice de massa corporal (BMI)", 10.0, 50.0, 24.0, step=0.1)
            age = st.number_input("Idade", 15, 80, 30)
            num_partos = st.number_input("Número de partos", 0, 20, 1)
        submitted = st.form_submit_button("Gerar Predição")

    if submitted:
        input_data = pd.DataFrame({
            'WBC': [wbc],
            'BMI': [bmi],
            'Age': [age],
            'NumPartos': [num_partos],
            'Population_bin': [1 if population == "Americano" else 0],
            'RepStatus_cat': [int(rep_status[0])],
            'RepStatus_bin': [0 if rep_status.startswith("0") else 1]
        })
        try:
            scaled_input = scaler.transform(input_data)
            prediction = modelo.predict(scaled_input)[0]
            st.subheader("Resultado da Predição")
            st.metric("Contagem estimada de neutrófilos (células/μL)", f"{prediction:.2f}")
            st.info("""
            **Interpretação:**  
            Este valor representa a contagem estimada de neutrófilos (células/μL) no sangue com base nos parâmetros fornecidos.
            """)
        except Exception as e:
            st.error(f"Erro ao realizar a predição: {str(e)}")

# --- Aba 6: Considerações Finais ---

with aba6:

    st.header("📌 Considerações Finais")

    st.markdown("""
    **A partir do conjunto de dados utilizado neste trabalho, pode-se concluir que:**
    """)

    # Lista de conclusões com marcadores
    conclusions = [
        "As duas populações estudadas apresentam perfis distintos de contagem leucocitária, "
        "refletindo provavelmente diferenças em seus ambientes e condições de vida.",
        
        "O estado reprodutivo (especialmente a gravidez) demonstra influência significativa "
        "nos parâmetros imunológicos analisados.",
        
        "A abordagem de machine learning mostrou-se eficaz para modelar as complexas interações "
        "entre variáveis biológicas, antropométricas e populacionais.",
        
        "A inclusão de metadados mais detalhados sobre a população americana poderia enriquecer "
        "as análises comparativas."
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