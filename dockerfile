
FROM python:3.11.9
WORKDIR /src
COPY . /src
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]