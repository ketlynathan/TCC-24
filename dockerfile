# Use uma imagem base slim para reduzir o tamanho da imagem
FROM python:3.11-slim-buster

# Copie o requirements.txt (se estiver usando)
COPY requirements.txt requirements.txt

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o código da aplicação
COPY . .

# Defina o diretório de trabalho
WORKDIR /app

# Exponha a porta 8501 para o Streamlit
EXPOSE 8501

# Comando para executar a aplicação
CMD ["streamlit", "run", "app.py"]