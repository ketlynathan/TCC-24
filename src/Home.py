import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


st.image("pages/img/Movimente-se.png")
st.write("# Bem vindo ao MOVIMENTE-SE! 👋")

st.sidebar.success("Selecione opção desejada.")

st.markdown(
    """
    MOVIMENTE-SE é uma plataforma dedicada a promover um estilo de vida ativo e saudável.
      Aqui você encontrará diversos recursos para te ajudar nessa jornada.

     👈 Selecione uma opção na barra lateral para a opção deseja!
   
    ### Quer saber mais?
    - Confira nosso [Instagram](https://www.instagram.com/kemovimentese/)
    - Escute nosso [podcast no Spotify](https://open.spotify.com/show/6mBtDw0ylxWTUCggSYW9bo)
    - Visite nosso [canal no YouTube](https://www.youtube.com/channel/UCNri68wZCBg5UCc859v_Mxg)
    - Siga-nos no [Strava](https://www.strava.com/athletes/117129739)
    ### Veja mais recursos:
    - Pegue seu Livro: [Harmonia Trifásica 1](https://amzn.to/49D0cwa)
    - Explore o [Harmonia Trifásica 2](https://amzn.to/3SZvIi3)
"""
)

st.sidebar.markdown(
        "Desenvolvido por [Ketlyn Athan](https://www.linkedin.com/in/ketlyn-athan-633a41187/)")