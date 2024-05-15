FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY . /app
WORKDIR /app
ENV ENV=local

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["uvicorn", "api.api_server:app", "--host", "0.0.0.0", "--port", "9999"]
