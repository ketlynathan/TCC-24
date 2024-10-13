#!/bin/bash

# Iniciar o Streamlit em segundo plano
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &

# Iniciar a API
python api.py

# Esperar pelos processos filhos
wait
