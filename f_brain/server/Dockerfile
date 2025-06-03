FROM python:3.11-slim

WORKDIR /app
RUN apt-get update \
    && apt-get install -y build-essential gcc libpq-dev \
    && pip install poetry==2.1.3 \
    && pip install gunicorn \
    && pip install django-admin \
    && pip install python-dotenv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-interaction --no-ansi --no-root

# Le COPY est remplacé par un volume dans docker-compose.yml

# Default command - will be overridden by docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
