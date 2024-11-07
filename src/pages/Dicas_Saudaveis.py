import streamlit as st


st.title("Dicas Saudaveis:")
st.markdown(
    """
    ### Higiene do sono:
    - 1. Definir um horário para acordar diariamente.
    - 2. Se exponha a luz natural por 30 minutos diariamente.
    - 3. Não tomar cafeína depois das 15h """)
st.video("https://www.youtube.com/watch?v=8NO6JRBnZpg")

st.subheader("Entenda os Ciclos do sono")
st.markdown(
    """
    - 1º Estágio: fase da sonolência, quando se inicia a transição do sono leve para o mais profundo,
    em que a pessoa pode ser facilmente despertada.
    - 2º Estágio: a atividade cardíaca é reduzida e os músculos ficam relaxados, nela também acontece a desconexão do cérebro com os estímulos do mundo real.
   -  3º Estágio: caracterizada pelo descanso da atividade cerebral e pelo sono profundo, o que acontece em média 40 minutos por noite.
    #### Fase do sono REM
    Na fase do sono REM, acontece o descanso profundo e liberação de hormônios, além do repouso da mente.
    É uma fase de extrema importância para a recuperação da energia física. 
    Nela também é quando acontece uma intensa atividade cerebral e a consolidação da memória.
    Outra importante característica desta fase é o intenso movimento ocular.""")
st.video("https://www.youtube.com/watch?v=o74VRQBnV8E")

st.subheader("Alimentação Saudavel")
st.markdown(
    """ 
    - 1 Comer em horários consistentes, todos os dias
    - 2 Planejar a alimentação com antecedência
    - 3 Ter uma logística: estipular o horário, onde/como vai guardar/resfriar/esquentar/comer a comida
    - 4 Controlar Caloria: ter uma noção da relação quantidade de comida/caloria"""
)
st.video("https://www.youtube.com/watch?v=qTH_P4PBEI8")

st.markdown(
    """
### Habitos

- 1- Dormir 7 a 9 horas
- 2- Tomar água (35ml X seu peso)
- 3- Tomar 15 min de sol por dia
- 4-  Diminuir o açúcar 
- 5-  Ler todo dia
- 6-  Exercitar-se
- 7-  Desapegar-se de coisas
- 8- Arrume a sua cama
- 9- Evite o álcool 
- 10- Evite sobrecarga de informações
    
"""
)
st.video("https://www.youtube.com/watch?v=Dmfe_B6UOyQ")


st.subheader("Dicas de Livros")
url = "https://amzn.to/3NXj1S3"
if st.button("Visit Amazon Link"):
    st.markdown(f"[Go to Amazon]({url})", unsafe_allow_html=True)