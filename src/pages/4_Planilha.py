import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from io import BytesIO

# Função para gerar o modelo de xlsx
def gerar_modelo():
    # Criar um DataFrame como exemplo de modelo
    dados = {
        "Tipo": ["Corrida"],
        "Data": ["03-11-2024"],
        "Titulo": ["Treino"],
        "Tempo": ["00:59:20"],
        "Distancia": ["5,3 KM"],
        "Elevacao": ["124"]
    }
    df_modelo = pd.DataFrame(dados)
    
    # Salvar o DataFrame como xlsx em memória
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_modelo.to_excel(writer, index=False, sheet_name='Modelo')
    output.seek(0)  # Reinicia o ponteiro para o início do arquivo em memória
    
    return output

# Título da aplicação
st.title("Controle de Treinos")

# Opção para baixar o modelo de xlsx
st.subheader("Baixar modelo")
st.markdown("Clique no botão abaixo para baixar o modelo de arquivo em formato .xlsx")

modelo = gerar_modelo()
st.download_button(
    label="Baixar Modelo XLSX",
    data=modelo,
    file_name="modelo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Opção para carregar o arquivo xlsx
st.subheader("Carregar arquivo")
st.markdown("Após preencher sua planilha conforme o modelo, carregue aqui o seu arquivo .xlsx")
st.markdown("Carregue seu próprio arquivo .xlsx para visualização")

# Carregar o arquivo
uploaded_file = st.file_uploader("Escolha o arquivo", type=["xlsx"])

# Exibir o conteúdo do arquivo carregado
if uploaded_file is not None:
    # Tentar importar o openpyxl e ler o arquivo
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.write("Conteúdo do arquivo carregado:")
        #st.dataframe(df)
        
        # Verificar se as colunas necessárias estão presentes no dataframe
        if all(col in df.columns for col in ['Data', 'Tipo', 'Tempo', 'Titulo', 'Distancia']):

            df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
            df['Ano'] = df['Data'].dt.year.astype('Int64')  # Converte o ano para int, lidando com NaNs
            df['Mes'] = df['Data'].dt.month
            df['Dia'] = df['Data'].dt.day

            # Converter nomes dos meses para português
            meses = {
                1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
                5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
            }
            df['Mes_nome'] = df['Mes'].map(meses)

            # Filtros de Ano e Mês
            st.sidebar.header('Filtros')
            ano_selecionado = st.sidebar.selectbox("Selecione o Ano", df["Ano"].dropna().unique())
            mes_selecionado = st.sidebar.selectbox("Selecione o Mês", df["Mes_nome"].dropna().unique())
            
            # Filtrar dados por ano e mês selecionados
            df_filtrado = df[(df["Ano"] == ano_selecionado) & (df["Mes_nome"] == mes_selecionado)]

            if not df_filtrado.empty:
                # Obter tipos de atividades
                tipos_atividades = df_filtrado['Tipo'].unique()

                # Contar dias treinados por tipo de atividade
                dias_treinados = df_filtrado.groupby('Tipo')['Dia'].count().reset_index()
                dias_treinados.columns = ['Tipo', 'Dias Treinados']
                
                # Dias treinados no total
                total_dias_treinados = df_filtrado['Dia'].nunique()
                total_provas = df_filtrado[df_filtrado['Titulo'] == 'Prova'].shape[0]

                # Função para converter tempo em segundos
                def time_to_seconds(time_str):
                    try:
                        h, m, s = map(int, time_str.split(':'))
                        return h * 3600 + m * 60 + s
                    except (ValueError, AttributeError):
                        return 0  # Ignorar valores inválidos

                # Calcular o total de tempo por atividade
                total_tempo_por_tipo = {}
                for tipo in tipos_atividades:
                    tempos = df_filtrado[df_filtrado['Tipo'] == tipo]['Tempo'].tolist()
                    total_segundos = sum(time_to_seconds(t) for t in tempos)
                    total_tempo = str(datetime.timedelta(seconds=total_segundos))
                    
                    total_tempo_por_tipo[tipo] = total_tempo

                # Gráfico de Pizza
                fig_pizza, ax_pizza = plt.subplots()
                ax_pizza.pie(dias_treinados['Dias Treinados'], labels=dias_treinados['Tipo'], autopct=lambda p: f'{int(p * sum(dias_treinados["Dias Treinados"]) / 100)}', startangle=90)
                ax_pizza.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                #3ax_pizza.set_title(f'Dias Treinados por Atividade em {meses[mes_selecionado]}/{ano_selecionado}')

                # Convertendo e filtrando dados
                df_filtrado.loc[:, 'Distancia'] = (
                df_filtrado['Distancia']
                .astype(str)
                .str.replace(',', '.', regex=False)
                .str.extract(r'(\d+\.\d+)')[0]
                .astype(float)
                )

                # Filtra as distâncias maiores que 0 e calcula o total por tipo
                df_kms = df_filtrado[df_filtrado['Distancia'] > 0]
                total_kms_por_tipo = df_kms.groupby('Tipo')['Distancia'].sum().reset_index()

                # Criando o gráfico de linhas
                fig_line, ax_line = plt.subplots()
                sns.lineplot(data=total_kms_por_tipo, x='Tipo', y='Distancia', marker='o', ax=ax_line)
                ax_line.set_title('Total de KMs por Atividade')
                ax_line.set_xlabel('Tipo de Atividade')
                ax_line.set_ylabel('Total de KMs')

                st.header('Resumo dos Treinamentos')
                num_atividades = len(tipos_atividades)

                if num_atividades <= 3:
                    colunas = st.columns(num_atividades + 1)  # Coluna extra para "Dias Treinados" e "Provas"
                    for i, tipo in enumerate(tipos_atividades):
                        colunas[i].metric(tipo.capitalize(), total_tempo_por_tipo[tipo])
                    colunas[-1].metric("Dias Treinados", total_dias_treinados)
                    colunas[-1].metric("Provas", total_provas)
                else:
                    colunas1 = st.columns(4)  # Limite de 4 colunas na primeira linha
                    colunas2 = st.columns(num_atividades - 4 + 1)  # Colunas restantes na segunda linha, mais uma para "Dias Treinados" e "Provas"
    
                    for i in range(4):
                        colunas1[i].metric(tipos_atividades[i].capitalize(), total_tempo_por_tipo[tipos_atividades[i]])
    
                    for i in range(4, num_atividades):
                        colunas2[i - 4].metric(tipos_atividades[i].capitalize(), total_tempo_por_tipo[tipos_atividades[i]])
    
                    colunas2[-1].metric("Dias Treinados", total_dias_treinados)
                    colunas2[-1].metric("Provas", total_provas)

                   


    

                # Mostrar gráficos lado a lado
                try:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.pyplot(fig_pizza)
                    with col2:
                        st.pyplot(fig_line)
                except Exception as e:
                    st.error(f"Erro ao renderizar os gráficos: {e}")
            else:
                st.info("Não há dados disponíveis para o ano e mês selecionados.")
        else:
            st.error("O arquivo carregado não contém as colunas necessárias: 'Data', 'Tipo', 'Tempo', 'Titulo' e 'Distancia'.")
    except ImportError:
        st.error("O pacote 'openpyxl' não está instalado. Por favor, instale-o usando 'pip install openpyxl'.")
else:
    st.info("Nenhum arquivo carregado ainda.")
