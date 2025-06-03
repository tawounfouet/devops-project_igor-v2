FROM python:3.11-slim

WORKDIR /app
RUN apt-get update \
    && apt-get install -y build-essential gcc libpq-dev \
    && pip install poetry==2.1.2 \
    && pip install gunicorn \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["gunicorn", "server_config.wsgi:application", "--bind", "0.0.0.0:8000"]

CMD ["yarn", "dev", "--host", "0.0.0.0", "--port", "4173"]
