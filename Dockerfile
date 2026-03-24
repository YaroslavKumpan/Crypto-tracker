FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN chmod +x entrypoint.sh && \
    sed -i 's/\r$//' entrypoint.sh && \
    sed -i 's/\r$//' alembic.ini

ENV PYTHONPATH=/app

ENTRYPOINT ["/app/entrypoint.sh"]