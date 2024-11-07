import streamlit as st
import pandas as pd
from rich import print as rprint

# Função para calcular o IMC
def calcular_imc(peso, altura):
    return peso / (altura ** 2)

# Função para calcular o peso ideal (usaremos um IMC de referência de 22)
def calcular_peso_ideal(altura, genero):
    imc_ideal = 22
    return imc_ideal * (altura ** 2)

# Função para determinar a categoria do IMC
def categoria_imc(imc, idade):
    if idade < 65:
        if imc < 18.5:
            return "Abaixo do peso"
        elif 18.5 <= imc < 24.9:
            return "Peso normal"
        elif 25 <= imc < 29.9:
            return "Sobrepeso"
        else:
            return "Obesidade"
    else:
        if imc < 22:
            return "Abaixo do peso"
        elif 22 <= imc < 27:
            return "Peso normal"
        elif 27 <= imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidade"

# Função principal para exibir a interface
def main():
    st.set_page_config(page_title="Calculadora de IMC", layout="wide")

    st.markdown(
        """
        <style>
        .main {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center; color:  #FF5733;'>Calculadora de IMC</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Avalie seu Índice de Massa Corporal</h3>", unsafe_allow_html=True)

    # Dividir a tela em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        with st.form(key="imc_form"):
            st.subheader("Informe seus dados")
            genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
            idade = st.number_input("Informe sua idade:", min_value=1, max_value=120, step=1)
            peso = st.number_input("Informe seu peso (kg):", min_value=1.0, step=0.1)
            altura = st.number_input("Informe sua altura (m):", min_value=0.5, step=0.01)
            submit_button = st.form_submit_button(label="Calcular")

    if submit_button:
        if peso and altura and idade:
            imc = calcular_imc(peso, altura)
            peso_ideal = calcular_peso_ideal(altura, genero)
            peso_a_perder = max(0, peso - peso_ideal)
            categoria = categoria_imc(imc, idade)
            
            with col2:
                st.success("Cálculo realizado com sucesso!")
                st.write(f"Seu IMC é: {imc:.2f} ({categoria})")
                st.write(f"Seu peso ideal é: {peso_ideal:.2f} kg")
                
                if peso_a_perder > 0:
                    st.write(f"Você precisa perder {peso_a_perder:.2f} kg para alcançar seu peso ideal.")
                    
                else:
                    st.write("Parabéns! Você está no seu peso ideal.")
                
                # Armazenar os dados em um DataFrame
                data = {
                    "Gênero": [genero],
                    "Idade": [idade],
                    "Peso": [peso],
                    "Altura": [altura],
                    "IMC": [imc],
                    "Categoria": [categoria],
                    "Peso Ideal": [peso_ideal],
                    "Peso a Perder": [peso_a_perder]
                }
                df = pd.DataFrame(data)
                st.dataframe(df)
                st.subheader("Veja também")
                st.text("Consequencia do sedentarismo")
                st.video("https://www.youtube.com/watch?v=alZZ2PQ0SL8")
                st.text("Você sabia?")
                st.video("https://www.youtube.com/watch?v=EEv4_DcDVFk")
                
                # Usar rich para imprimir o DataFrame
                rprint(df)
        else:
            with col2:
                st.error("Por favor, preencha todos os campos.")

    # Adicionar áudio e vídeos
    st.subheader("Dicas de Saúde")
    st.video("https://www.youtube.com/watch?v=PtJ5UiSLdpE")
    
    #st.video(video_file_2.read())
    
    #video_file_3 = open("path_to_video_file_3.mp4", "rb")
    #st.video(video_file_3.read())

if __name__ == '__main__':
    main()
