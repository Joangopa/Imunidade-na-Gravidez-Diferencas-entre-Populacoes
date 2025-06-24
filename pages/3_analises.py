import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Carregar os dados
@st.cache_data  # Cache para melhor performance
def load_data():
    data = pd.read_csv('assets/Hove_et_al_2020.csv')
    # Filtro dos dados
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

# Configuração da página
st.set_page_config(layout="wide")
st.title("Análise de Dados de Imunidade")

# Criar duas colunas
col1, col2 = st.columns(2)

# Primeiro gráfico - Histogramas
with col1:
    st.subheader("Distribuição das Contagens Celulares na População Geral")
    
    variaveis = ['WBC', 'NEU', 'LYM', 'MON', 'BAS', 'EOS']
    fig1, axes = plt.subplots(2, 3, figsize=(12, 8))  # Aumentei o tamanho para melhor visualização
    sns.set(style="whitegrid")
    sns.set_context("notebook", font_scale=1.2)
    
    for ax, var in zip(axes.flat, variaveis):
        sns.histplot(data=dados, x=var, kde=True, bins=30, color='skyblue', ax=ax)
        ax.set_title(f'Distribuição de {var}', fontsize=14)
        ax.set_xlabel(f'{var} (cells/μL)', fontsize=12)  # Adicionei a unidade de medida
        ax.set_ylabel('Frequência', fontsize=12)
    
    plt.tight_layout()
    st.pyplot(fig1)

# Segundo gráfico - Violinos
with col2:
    st.subheader("Comparação por Status Reprodutivo e População")
    
    cell_types = ['WBC', 'NEU', 'LYM', 'MON', 'BAS', 'EOS']
    dados_long = dados.melt(
        id_vars=['RepStatus', 'Population'],
        value_vars=cell_types,
        var_name='Cell_Type',
        value_name='Cell_Count'
    )
    
    # Definir ordens
    repstatus_order = ['Cycling', 'T1', 'T2', 'T3']
    population_order = ['NHANES', 'THLHP']
    
    dados_long['RepStatus'] = pd.Categorical(dados_long['RepStatus'], categories=repstatus_order, ordered=True)
    dados_long['Population'] = pd.Categorical(dados_long['Population'], categories=population_order, ordered=True)
    dados_long['Cell_Type'] = pd.Categorical(dados_long['Cell_Type'], categories=cell_types, ordered=True)
    
    # Configurações do gráfico
    sns.set_context("notebook", font_scale=1.2)
    
    # Use plt.subplots em vez de catplot para melhor controle
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
        
        # Adicionar médias
        for j, status in enumerate(repstatus_order):
            for k, pop in enumerate(population_order):
                pop_data = subset[(subset['RepStatus'] == status) & (subset['Population'] == pop)]
                mean_val = pop_data['Cell_Count'].mean()
                offset = -0.05 if pop == 'NHANES' else 0.05  # Ajuste no offset para melhor visualização
                ax.scatter(j + offset, mean_val, color='black', s=50, marker='o', zorder=10,
                          edgecolor='white', linewidth=0.8)
        
        ax.set_title(cell_type, fontsize=14)
        ax.set_xlabel("Status Reprodutivo", fontsize=12)
        ax.set_ylabel("cells/μL", fontsize=12)
        ax.tick_params(axis='both', labelsize=10)
        
        # Ajustar a legenda
        if i == 0:  # Mostrar legenda apenas no primeiro gráfico
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels, title='População', fontsize=10, title_fontsize=11)
        else:
            ax.get_legend().remove()
    
    plt.tight_layout()
    st.pyplot(fig2)

# Adicionar espaço no final
st.markdown("<br><br>", unsafe_allow_html=True)

# Mostrar a imagem - corrigi o caminho para usar barra normal
col, col2 = st.columns([1, 1])  # A coluna do meio é mais larga
with col:
    st.subheader("Resultados do teste U: identificação dos grupos com menores contagens celulares")
    st.image("assets/imagem_tabela_menor_contagem.png", 
            caption="A tabela indica a população com menor contagem celular média para cada tipo de célula",
            width=500)
    
with col2:
    st.subheader("Relação de agrupamentos K-means e PCA com separação de populações")
    st.image("assets/agrupamentos_pca.png", 
            caption="A imagem mostra os agrupamentos K-means e PCA com separação de populações",
            width=500)