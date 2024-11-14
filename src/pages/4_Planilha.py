import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np
from io import BytesIO
import plotly.express as px

# Função para gerar o modelo de xlsx
def gerar_modelo():
    dados = {
        "Tipo": ["Corrida"],
        "Data": ["03-11-2024"],
        "Titulo": ["Treino"],
        "Tempo": ["00:59:20"],
        "Distancia": ["5,3 KM"],
        "Elevacao": ["124"]
    }
    df_modelo = pd.DataFrame(dados)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_modelo.to_excel(writer, index=False, sheet_name='Modelo')
    output.seek(0)
    
    return output

# Título da aplicação
st.title("Controle de Treinos")

# Opção para baixar o modelo de xlsx
st.subheader("Baixar modelo")
modelo = gerar_modelo()
st.download_button(
    label="Baixar Modelo XLSX",
    data=modelo,
    file_name="modelo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Função auxiliar para converter tempo em segundos
def time_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except (ValueError, AttributeError):
        return 0

# Carregar o arquivo de exemplo
uploaded_file = st.file_uploader("Escolha o arquivo", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    # Conversão e limpeza de dados
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
    df['Ano'] = df['Data'].dt.year.astype('Int64')
    df['Mes'] = df['Data'].dt.month_name(locale='pt_BR')  # Convertendo número do mês para o nome em português
    df['Tempo_segundos'] = df['Tempo'].apply(time_to_seconds)
    df['Distancia'] = df['Distancia'].astype(str).str.replace(',', '.', regex=False).astype(float)
    df['Tempo_minutos'] = df['Tempo_segundos'] / 60  # Nova coluna em minutos

    # Filtros de ano e mês
    st.sidebar.header('Filtros')
    ano_selecionado = st.sidebar.selectbox("Selecione o Ano", df["Ano"].dropna().unique())
    mes_selecionado = st.sidebar.selectbox("Selecione o Mês", df["Mes"].dropna().unique())
    df['Data'] = pd.to_datetime(df['Data'])

    # Contar os dias de treino por mês
    df['Mes'] = df['Data'].dt.to_period('M').astype(str)  # Convertemos Period para string
    monthly_counts = df.groupby('Mes').size().reset_index(name='days_trained')

    # Criar gráfico de barras
    fig = px.bar(monthly_counts, x='Mes', y='days_trained', 
                 title='Mês com mais dias treinados', 
                 labels={'Mes': 'Mês', 'days_trained': 'Dias Treinados'},
                 range_y=[0, 31])  # Definir o limite do eixo y de 0 a 31
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)
    
    df['Mes_nome'] = df['Data'].dt.month_name(locale='pt_BR')  # Converte para o nome do mês para filtrar
    df_filtrado = df[(df["Ano"] == ano_selecionado) & (df["Mes_nome"] == mes_selecionado)]
    
    # Métricas
    if not df_filtrado.empty:
        total_distancia = df_filtrado['Distancia'].sum()
        media_tempo = str(datetime.timedelta(seconds=int(df_filtrado['Tempo_segundos'].mean())))
        total_dias = df_filtrado['Data'].nunique()
        maior_distancia = df_filtrado['Distancia'].max()
        maior_distancia_data = df_filtrado.loc[df_filtrado['Distancia'].idxmax(), 'Data']
        total_tempo = str(datetime.timedelta(seconds=int(df_filtrado['Tempo_segundos'].sum())))

        # Cards de métricas principais
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Distância", f"{total_distancia:.2f} KM")
        col2.metric("Tempo Médio por Treino", media_tempo)
        col3.metric("Dias Treinados", total_dias)
        col4.metric("Maior Distância em um Dia", f"{maior_distancia:.2f} KM em {maior_distancia_data.strftime('%d-%m-%Y')}")
        
        # Gráficos
        # Gráfico de barras por tipo de atividade
        tipo_distancia = df_filtrado.groupby('Tipo')['Distancia'].sum().reset_index()
        tipo_tempo = df_filtrado.groupby('Tipo')['Tempo_segundos'].sum().reset_index()
        tipo_tempo['Tempo_horas'] = tipo_tempo['Tempo_segundos'] / 3600

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=tipo_distancia, x='Tipo', y='Distancia', ax=ax1, color='skyblue')
        ax1.set_ylabel("Distância Total (KM)")
        ax2 = ax1.twinx()
        sns.barplot(data=tipo_tempo, x='Tipo', y='Tempo_horas', ax=ax2, color='lightgreen')
        ax2.set_ylabel("Tempo Total (Horas)")
        
        # Gráfico de linha para evolução de distância e tempo
        df_filtrado = df_filtrado.sort_values('Data')
        fig2, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_filtrado, x='Data', y='Distancia', marker='o', label='Distância', ax=ax)
        ax.set_ylabel("Distância (KM)")
        ax2 = ax.twinx()
        sns.lineplot(data=df_filtrado, x='Data', y='Tempo_segundos', marker='o', color='orange', label='Tempo', ax=ax2)
        ax2.set_ylabel("Tempo (Segundos)")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Distância Total e Tempo Total por Tipo de Atividade")
            st.pyplot(fig1)
        with col2:
            st.write("Evolução da Distância e Tempo por Data")
            st.pyplot(fig2)

        # Gráfico de calor por mês
        df_calendario = df_filtrado.copy()
        df_calendario['Mes'] = df_calendario['Data'].dt.month_name(locale='pt_BR')  # Usando o nome do mês em português
        heatmap_data = df_calendario.pivot_table(index="Tipo", columns="Mes", values="Distancia", aggfunc="sum").fillna(0)
        fig1, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".2f", ax=ax)  # Adicionando duas casas decimais
        ax.set_title("Frequência de Atividades por Mês")
        
        # Distribuição de tempos (em minutos) por mês
        fig2, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(data=df_filtrado, x="Mes", y="Tempo_minutos", ax=ax, palette="viridis")
        ax.set_title("Distribuição de Tempos por Mês")
        ax.set_ylabel("Tempo (em minutos)")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Frequência de Atividades (Calendário)")
            st.pyplot(fig1)
        with col2:
            st.write("Distribuição de Tempos por Mês")
            st.pyplot(fig2)
        
    else:
        st.info("Não há dados disponíveis para o ano e mês selecionados.")
else:
    st.info("Nenhum arquivo carregado ainda.")
