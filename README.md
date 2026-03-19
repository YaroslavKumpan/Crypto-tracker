# 🚀 Crypto Price Tracker

Сервис для сбора и хранения цен криптовалют с биржи Deribit с последующим предоставлением данных через API.

---

## 📌 Описание

Приложение:

* Каждую минуту получает **index price** для:

  * `BTC_USD`
  * `ETH_USD`
* Сохраняет данные в **PostgreSQL**
* Предоставляет API для получения:

  * всех цен
  * последней цены
  * цен по диапазону дат

---

## 🧱 Стек технологий

* **FastAPI** — API
* **PostgreSQL** — база данных
* **SQLAlchemy (async + sync)** — ORM
* **Alembic** — миграции
* **Celery + Redis** — фоновые задачи
* **aiohttp** — клиент для Deribit API
* **Docker / Docker Compose** — контейнеризация
* **Poetry** — управление зависимостями
* **Pytest** — тестирование

---

## 🏗 Архитектура

```
                +------------------+
                |   FastAPI API    |
                +--------+---------+
                         |
                         v
                +------------------+
                |   PostgreSQL     |
                +------------------+
                         ^
                         |
         +---------------+----------------+
         |                                |
+------------------+         +------------------+
| Celery Worker    |         | Celery Beat      |
| (fetch prices)   |         | (scheduler)      |
+------------------+         +------------------+
         |
         v
+------------------+
|  Deribit API     |
+------------------+
```

---

## ⚙️ Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <https://github.com/YaroslavKumpan/Crypto-tracker.git>
cd crypto-tracker
```

---

### 2. Создание `.env`

```env
DB_URL=postgresql+asyncpg://user:password@db:5432/crypto
REDIS_URL=redis://redis:6379/0
```

---

### 3. Запуск проекта

```bash
docker-compose up --build
```

---

### 4. Доступ к сервисам

* API документация (Swagger):

```
http://localhost:8000/docs
```

---

## 📡 API

### 🔹 1. Получить все цены

```
GET /prices?ticker=btc_usd
```

---

### 🔹 2. Получить последнюю цену

```
GET /price/latest?ticker=btc_usd
```

---

### 🔹 3. Получить цены по дате

```
GET /prices/filter?ticker=btc_usd&start=1700000000&end=1700001000
```

---

## 🧪 Тестирование

```bash
pytest
```

---

## 🐳 Docker сервисы

* `app` — FastAPI
* `worker` — Celery worker
* `beat` — Celery scheduler
* `db` — PostgreSQL
* `redis` — брокер

---

## 🧠 Design Decisions

### 1. Разделение async и sync БД

* FastAPI использует **async SQLAlchemy**
* Celery использует **sync SQLAlchemy**

📌 Причина:
Celery работает в отдельных процессах и не дружит с async ORM из коробки.

---

### 2. Использование aiohttp

📌 Почему:

* асинхронные HTTP-запросы
* высокая производительность
* поддержка параллельных запросов

---

### 3. Параллельное получение цен

```python
asyncio.gather(...)
```

📌 Почему:

* быстрее, чем последовательные запросы
* независимость BTC / ETH

---

### 4. Celery + Beat

📌 Почему:

* стандарт для фоновых задач
* масштабируемость
* отказоустойчивость

---

### 5. Docker Compose

📌 Почему:

* быстрый запуск
* изоляция сервисов
* удобство разработки

---

### 6. Healthcheck

📌 Почему:

* гарантирует готовность PostgreSQL и Redis
* предотвращает race condition

---

### 7. Poetry с `--no-root`

📌 Почему:

* проект не является библиотекой
* используется только как dependency manager

---

### 8. Alembic

📌 Почему:

* контроль схемы БД
* безопасные миграции

---

### 9. Retry в Celery

```python
autoretry_for=(Exception,)
```

📌 Почему:

* устойчивость к падениям API
* автоматическое восстановление

---

## ⚠️ Возможные улучшения

* Добавить кеширование (Redis)
* Метрики (Prometheus + Grafana)
* Лимиты запросов
* Авторизация
* CI/CD pipeline

---

## 👨‍💻 Автор

Yaroslav Kumpan
