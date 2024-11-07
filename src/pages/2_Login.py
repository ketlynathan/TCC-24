import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
from rich import print as rprint
from lib.http import create_authenticated_client

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

        # Process date and time columns
        df['start_date_local'] = pd.to_datetime(df['start_date_local'])
        df['date'] = df['start_date_local'].dt.date
        df['month_str'] = df['start_date_local'].dt.strftime('%Y-%m')
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
        st.image(athlete_data.get('profile'), caption=athlete_data.get('username'), width=150)

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
        st.write(athlete_data.get('state'))

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
            total_days = filtered_df["date"].nunique()
            days_in_month = filtered_df["start_date_local"].dt.days_in_month.iloc[0]

            # Formatting time and distance
            total_time_str = f"{total_time.components.hours:02}:{total_time.components.minutes:02}"
            total_distance_str = f"{total_distance:.2f} km"

            # Display key metrics
            col3, col4, col5, col6 = st.columns(4)
            col3.metric("Distância Total", total_distance_str)
            col4.metric("Tempo Total", total_time_str)
            col5.metric("Ganho de Elevação Total", total_elevation_gain)
            col6.metric("Dias de Atividade", total_days)

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

            # Displaying the charts side by side
            col7, col8 = st.columns(2)
            with col7:
                st.pyplot(fig1)
            with col8:
                st.pyplot(fig2)

            # Improved Average speed chart using Seaborn
            avg_speed_df = filtered_df.groupby("type_pt")["average_speed"].mean().reset_index()

            fig3, ax3 = plt.subplots(figsize=(12, 6))
            sns.barplot(data=avg_speed_df, x="type_pt", y="average_speed", palette="viridis", ax=ax3)
            ax3.set_ylabel('Velocidade Média (m/s)')
            ax3.set_xlabel('Tipo de Atividade')
            ax3.set_title('Velocidade Média por Tipo de Atividade')
            sns.despine()

            st.pyplot(fig3)


if __name__ == "__main__":
    main()
