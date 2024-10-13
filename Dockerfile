# Usar uma imagem base do Python 3.11.9
FROM python:3.11.9

# Atualizar o pip para a versão mais recente
RUN pip install --upgrade pip

# Definir o diretório de trabalho no container
WORKDIR /src

# Copiar todos os arquivos do projeto para o diretório de trabalho
COPY . /src

# Instalar as dependências listadas no requirements.txt
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; else echo "requirements.txt not found, skipping..."; fi

# Expor a porta 8501 para o Streamlit
EXPOSE 8501

# Copiar o script de inicialização para o container
COPY start.sh /usr/local/bin/start.sh

# Dar permissão de execução ao script de inicialização
RUN chmod +x /usr/local/bin/start.sh

# Comando de entrada para iniciar o Streamlit e a API
ENTRYPOINT ["/usr/local/bin/start.sh"]
