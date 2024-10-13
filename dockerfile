
# Usar uma imagem base do Python 3.11.9
FROM python:3.11.9

# Definir o diretório de trabalho no container
WORKDIR /src

# Copiar todos os arquivos do projeto para o diretório de trabalho
COPY . /src

# Instalar as dependências listadas em requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta 8501 para o Streamlit
EXPOSE 8501

# Comando de entrada para iniciar o Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]