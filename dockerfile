# Usando uma imagem base Python
FROM python:3.12-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando o pyproject.toml e poetry.lock
COPY pyproject.toml poetry.lock /app/

# Instalando o poetry
RUN pip install poetry

# Instalando as dependências do projeto
RUN poetry install --no-dev

# Copiando o código-fonte
COPY . /app

# Expondo a porta 8501, que é onde o Streamlit roda por padrão
EXPOSE 8501

# Definindo o comando para rodar o projeto com Streamlit
CMD ["poetry", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false"]
