# Usar uma imagem base do Python 3.12
FROM python:3.12

# Atualizar o pip para a versão mais recente
RUN pip install --upgrade pip

# Instalar o uv
RUN pip install uv

# Definir o diretório de trabalho no container
WORKDIR /src

# Copiar todos os arquivos do projeto para o diretório de trabalho
COPY . /src

# Instalar as dependências listadas no pyproject.toml
RUN  uv sync

RUN  .\.venv\Scripts\activate                                                                                 

# Expor a porta 8501 para o Streamlit
EXPOSE 8501

# Comando de entrada para iniciar o Streamlit
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
