FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

CMD ["bash", "-c", "alembic upgrade head && celery -A app.tasks.price_tasks worker --beat & uvicorn app.main:app --host 0.0.0.0 --port 8000"]