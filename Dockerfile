FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

ENV PYTHONPATH=/app

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]