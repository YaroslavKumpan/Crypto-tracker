FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

# Устанавливаем только зависимости (без проекта)
RUN poetry install --no-interaction --no-ansi --no-root

RUN chmod +x entrypoint.sh 2>/dev/null || true
ENV PYTHONPATH=/app
ENTRYPOINT ["/app/entrypoint.sh"]