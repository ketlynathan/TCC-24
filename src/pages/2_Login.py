import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import timedelta
from rich import print as rprint
from lib.http import create_authenticated_client
import locale



# Caminho da imagem da logo
LOGO_PATH = "pages/img/Movimente-se.png"

# Streamlit layout configuration
st.set_page_config(layout="wide", page_title="Dashboard de Atividades")

# Data caching and processing
@st.cache_data
def get_and_process_activities():
    try:
        # Create authenticated client for API access
        http_client = create_authenticated_client()

        # Retrieve data from Strava API
        response = http_client.get("https://www.strava.com/api/v3/athlete/activities")
        response.raise_for_status()  # Raise an error for non-200 status codes
        activities = response.json()

        # Retrieve athlete data
        athlete_response = http_client.get("https://www.strava.com/api/v3/athlete")
        athlete_response.raise_for_status()
        athlete_data = athlete_response.json()

        # Create a DataFrame from the activities
        df = pd.DataFrame(activities)

        # Configurar o idioma para português do Brasil
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        # Process date and time columns
        df['start_date_local'] = pd.to_datetime(df['start_date_local'])
        df['date'] = df['start_date_local'].dt.date
        df['month_str'] = df['start_date_local'].dt.strftime('%B %Y')  # Nome completo do mês em português
        df['time'] = pd.to_timedelta(df['moving_time'], unit='s')

        # Map activity types to Portuguese descriptions
        activity_map = {
            "Run": "Corrida",
            "Ride": "Ciclismo",
            "Walk": "Caminhada",
            "Crossfit": "Crossfit",
            "Workout": "Pilates"
        }
        df["type_pt"] = df["type"].map(activity_map)

        return df, athlete_data
    except Exception as e:
        st.error(f"Erro ao obter atividades: {e}")
        return pd.DataFrame(), {}

# Placeholder for the button and the data
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# Function to load data when button is clicked
def load_data():
    st.session_state.data, st.session_state.athlete_data = get_and_process_activities()
    st.session_state.data_loaded = True

# Função para exibir a tela de login
def login_screen():
    st.markdown(
        f"""
        <style>
        .logo {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 150px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.image(LOGO_PATH)
    st.title("Movimente-se - Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Login"):
        if email and senha:
            st.success("Login realizado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

    if st.button("Entrar com Strava"):
        load_data()

    st.markdown("[Esqueci a senha](#)", unsafe_allow_html=True)
    st.markdown("[Cadastrar](#)", unsafe_allow_html=True)

# Função para exibir a tela de cadastro
def cadastro_screen():
    st.title("Movimente-se - Cadastro")

    nome = st.text_input("Nome Completo")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        if nome and email and senha:
            cadastrar_usuario(nome, email, senha)
        else:
            st.error("Por favor, preencha todos os campos.")

# Função para cadastrar usuário (dummy function)
def cadastrar_usuario(nome, email, senha):
    st.success(f"Usuário {nome} cadastrado com sucesso!")
    st.info("Um email de confirmação foi enviado para sua conta.")

# Função para exibir a tela de recuperação de senha
def esqueci_senha_screen():
    st.title("Movimente-se - Esqueci a Senha")

    email = st.text_input("Email")

    if st.button("Enviar"):
        if email:
            st.success("Instruções para redefinir sua senha foram enviadas para seu email.")
        else:
            st.error("Por favor, preencha o campo de email.")

# Controle de navegação entre telas
def main():
    if st.session_state.data_loaded:
        dashboard()
    else:
        menu = ["Login", "Cadastro", "Esqueci a Senha"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            login_screen()
        elif choice == "Cadastro":
            cadastro_screen()
        elif choice == "Esqueci a Senha":
            esqueci_senha_screen()

def dashboard():
    df = st.session_state.data
    athlete_data = st.session_state.athlete_data

    if df.empty:
        st.warning("Nenhuma atividade foi carregada.")
    else:
        # Display athlete data
        st.title("Dados do Atleta - Strava")

        # Display athlete profile image
        #st.image(athlete_data.get('profile'), caption=athlete_data.get('username'), width=150)

        # Convert relevant athlete data to DataFrame and display in Streamlit
        athlete_info = {
            'Username': athlete_data.get('username'),
            'Sexo': athlete_data.get('sex'),
            'Estado': athlete_data.get('state'),
            'Peso': athlete_data.get('weight'),
            'Summit': athlete_data.get('summit'),
            'Última atualização': athlete_data.get('updated_at')
        }
        athlete_df = pd.DataFrame([athlete_info])
        
        data_iso = athlete_data.get('updated_at')

        # Convertendo a string ISO para um objeto datetime
        data_datetime = datetime.datetime.fromisoformat(data_iso)

        # Formatando a data como desejado (ex: 03/11/2024)
        data_formatada = data_datetime.strftime("%d/%m/%Y")

        # Exibindo a data formatada
       
        col1, col2, col3, col4 = st.columns(4)
        col2.write(athlete_data.get('state'))
        col1.write(athlete_data.get('username'))
        col3.write(data_formatada)
        col4.write("Ultima atualização")


        # Sidebar filters
        st.sidebar.header("Filtros")
        selected_month = st.sidebar.selectbox("Selecione o Mês", df["month_str"].unique())
        selected_sport = st.sidebar.selectbox("Selecione o Tipo de Atividade", df["type_pt"].unique())
        

        # Filter DataFrame based on selections
        filtered_df = df[(df["month_str"] == selected_month) & (df["type_pt"] == selected_sport)]
        if filtered_df.empty:
            st.warning("Nenhum registro dessa atividade nesse mês.")
            # Reset key metrics to zero
            total_distance = 0
            total_time = timedelta(seconds=0)
            total_elevation_gain = 0
            total_days = 0

        else:
            # Key metrics calculation
            total_distance = filtered_df["distance"].sum() / 1000  # km
            total_time = filtered_df["time"].sum()
            total_elevation_gain = filtered_df["total_elevation_gain"].sum()
            total_elevation_gain_str = f"{total_elevation_gain:.2f}"
            total_days = filtered_df["date"].nunique()
            days_in_month = filtered_df["start_date_local"].dt.days_in_month.iloc[0]

            # Formatting time and distance
            total_time_str = f"{total_time.components.hours:02}:{total_time.components.minutes:02}"
            total_distance_str = f"{total_distance:.2f} km"

            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Distância Total", total_distance_str)
            col2.metric("Tempo Total", total_time_str)
            col3.metric("Ganho de Elevação Total", total_elevation_gain_str)
            col4.metric("Dias de Atividade", total_days)

            # Bar chart: number of days trained in the month
            days_not_trained = days_in_month - total_days

            fig1, ax1 = plt.subplots(figsize=(6, 6))  # Ensure same size
            ax1.barh(["Dias Treinados"], [total_days], color='skyblue')
            ax1.barh(["Dias Não Treinados"], [days_not_trained], color='lightgray', left=total_days)
            ax1.set_xlim(0, days_in_month)
            ax1.set_xlabel('Dias')

            # Pie chart: hours trained versus hours in a day
            total_hours_in_day = 24
            hours_trained = total_time.total_seconds() / 3600
            hours_not_trained = total_hours_in_day - hours_trained if hours_trained < total_hours_in_day else 0

            fig2, ax2 = plt.subplots(figsize=(6, 6))  # Ensure same size
            ax2.pie([hours_trained, hours_not_trained], labels=['Horas Treinadas', 'Horas Não Treinadas'],
                    autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff'])
            ax2.axis('equal')

            st.markdown("---")

            # Displaying the charts side by side
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(fig1)
            with col2:
                st.pyplot(fig2)
           
        st.markdown("---")
        #st.subheader("Velocidade Média por Tipo de Atividade")
        fig2, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df, x="type_pt", y="average_speed", palette="viridis", ax=ax)
        ax.set_xlabel("Tipo de Atividade")
        ax.set_ylabel("Velocidade Média (m/s)")
        ax.set_title("Distribuição de Velocidade Média por Tipo de Atividade")
        #st.pyplot(fig2)

        col1, col2 = st.columns(2)
        with col1:
            #st.subheader("Progresso de Distância Comparado à Meta Mensal")
            monthly_distance = df.groupby('month_str')['distance'].sum() / 1000  # Convertendo para km
            meta_mensal = st.number_input("Defina sua meta mensal de distância (km)", min_value=0, max_value=500, value=100, step=10)

            st.write("Progresso Mensal com Meta de Distância")
            fig1, ax = plt.subplots(figsize=(10, 6))
            monthly_distance.plot(kind='line', marker='o', ax=ax, label="Distância Percorrida")
            ax.axhline(meta_mensal, color='red', linestyle='--', label=f"Meta Mensal ({meta_mensal} km)")
            ax.set_xlabel("Mês")
            ax.set_ylabel("Distância (km)")
            ax.legend()
            st.pyplot(fig1)
        with col2:
            st.write("Distribuição de Velocidade Média por Tipo de Atividade")
            st.pyplot(fig2)

        # Renderizando o gráfico no Streamlit
        
        #st.subheader("Distribuição do Tipo de Atividade")
        activity_counts = df['type_pt'].value_counts()
        fig1, ax = plt.subplots()
        ax.pie(activity_counts, labels=activity_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("viridis", len(activity_counts)))
        ax.axis("equal")
        #st.pyplot(fig1)

        #st.subheader("Mapa de Calor de Dias Ativos")
        df['day_of_week'] = df['start_date_local'].dt.day_name()
        df['day'] = df['start_date_local'].dt.day
        activity_counts = df.pivot_table(index='day_of_week', columns='day', values='id', aggfunc='count').fillna(0)
        fig2, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(activity_counts, cmap="YlGnBu", ax=ax, cbar_kws={'label': 'Atividades'})
        #st.pyplot(fig2)
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribuição de Atividades por Tipo")
            st.pyplot(fig1)
        with col2:
            st.write("Mapa de Calor de Dias Ativos")
            st.pyplot(fig2)

        #st.subheader("Atividades por Tipo e Mês")
        monthly_activities = df.groupby(['month_str', 'type_pt']).size().unstack(fill_value=0)
        fig1, ax = plt.subplots(figsize=(10, 6))
        monthly_activities.plot(kind='bar', stacked=True, ax=ax, colormap="viridis")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Número de Atividades")
        #ax.set_title("Distribuição de Atividades por Tipo e Mês")
        #st.pyplot(fig1)

        #st.subheader("Distância Acumulada ao Longo do Tempo")
        df['cumulative_distance'] = df['distance'].cumsum() / 1000  # Convertendo para km
        fig2, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['start_date_local'], df['cumulative_distance'], color='blue', linewidth=2)
        ax.set_xlabel("Data")
        ax.set_ylabel("Distância Acumulada (km)")
        #ax.set_title("Progresso de Distância ao Longo do Tempo")
        #st.pyplot(fig2)

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribuição de Atividades por Tipo e Mês")
            st.pyplot(fig1)
        with col2:
            st.write("Progresso de Distância ao Longo do Tempo")
            st.pyplot(fig2)


        #st.subheader("Velocidade Média vs Distância")
        fig1, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='distance', y='average_speed', hue='type_pt', palette="viridis", ax=ax)
        ax.set_xlabel("Distância (m)")
        ax.set_ylabel("Velocidade Média (m/s)")
        #ax.set_title("Velocidade Média vs Distância por Tipo de Atividade")
        #st.pyplot(fig1)

        #st.subheader("Distribuição de Intensidade das Atividades")
        fig2, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df['distance'] / 1000, bins=20, kde=True, color="blue", ax=ax)  # Convertendo para km
        ax.set_xlabel("Distância (km)")
        #ax.set_title("Frequência de Atividades por Distância")
        #st.pyplot(fig2)

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.write("Velocidade Média vs Distância por Tipo de Atividade")
            st.pyplot(fig1)
        with col2:
            st.write("Frequência de Atividades por Distância")
            st.pyplot(fig2)

        


if __name__ == "__main__":
    main()
