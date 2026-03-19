from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# делаем sync URL для Celery и Alembic
sync_db_url = settings.DB_URL.replace(
    "postgresql+asyncpg://",
    "postgresql://"
)

engine = create_engine(sync_db_url, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)