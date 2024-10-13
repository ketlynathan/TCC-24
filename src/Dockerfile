# Usar uma imagem base do Python 3.11.9
FROM python:3.11.9

# Atualizar o pip para a versão mais recente
RUN pip install --upgrade pip

# Definir o diretório de trabalho no container
WORKDIR /src

# Copiar todos os arquivos do projeto para o diretório de trabalho
COPY . /src

# Verificar se o arquivo requirements.txt existe e instalar as dependências
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; else echo "requirements.txt not found, skipping..."; fi

# Expor a porta 8501 para o Streamlit
EXPOSE 8501

# Comando de entrada para iniciar o Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]
