FROM python:3.11.9
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry install
EXPOSE 8501
CMD [ "poetry", "run", "streamlit", "app.py", "--server.port-8501" ]
