import streamlit as st
import os
import time

# Define a pasta que contém os arquivos de música
music_dir = "src/pages/audio"  

# Lista os arquivos de música
music_files = [f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav", ".ogg"))]

# Configura os estados globais
if "current_track_index" not in st.session_state:
    st.session_state.current_track_index = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "repeat" not in st.session_state:
    st.session_state.repeat = False

# Função para obter o caminho do arquivo da música atual
def get_current_track():
    if st.session_state.current_track_index < len(music_files):
        return music_files[st.session_state.current_track_index]
    return None

# Função para avançar para a próxima música
def next_track():
    st.session_state.current_track_index += 1
    if st.session_state.current_track_index >= len(music_files):
        if st.session_state.repeat:
            st.session_state.current_track_index = 0  # Reinicia a playlist se estiver no modo de repetição
        else:
            st.session_state.playing = False  # Para se a playlist terminou e o modo de repetição está desativado
            st.session_state.current_track_index = 0
    st.experimental_rerun()

# Função para iniciar ou pausar a reprodução
def play_pause():
    st.session_state.playing = not st.session_state.playing
    if st.session_state.playing:
        st.experimental_rerun()

# Interface do Streamlit
st.title("Music Player")
st.write("Selecione uma música para começar a tocar:")

# Dropdown para selecionar a música inicial
selected_file = st.selectbox("Escolha uma música", music_files, index=st.session_state.current_track_index)

# Define o índice da faixa selecionada se o usuário escolher outra música
if selected_file:
    st.session_state.current_track_index = music_files.index(selected_file)

# Mostra o nome da música atual
current_track = get_current_track()
if current_track:
    st.write(f"Reproduzindo agora: {current_track}")

    # Exibe o áudio e define um botão de controle
    audio_file = open(os.path.join(music_dir, current_track), "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/ogg")
    st.write("Baixe para seu celular é só clicar nos 3 pontinhos")