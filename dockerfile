# Usar uma imagem base do Python 3.12
FROM python:3.11

# Instalar dependências do sistema operacional necessárias (caso precise)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry

# Definir o diretório de trabalho no container
WORKDIR /src

# Copiar todos os arquivos do projeto para o diretório de trabalho
COPY . /src

# Instalar as dependências via Poetry, desabilitando o ambiente virtual
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Expor a porta 8501 para o Streamlit
EXPOSE 8501

# Comando de entrada para iniciar o Streamlit
ENTRYPOINT ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501"]
