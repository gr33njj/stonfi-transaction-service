# STON.fi Transaction Service

Сервис для получения и хранения транзакций обмена (свопов) на платформе STON.fi в сети TON (The Open Network). Приложение использует FastAPI для создания REST API, SQLAlchemy для работы с базой данных PostgreSQL и `aiohttp` для взаимодействия с TON API.

## Основные возможности
- **Получение транзакций**: Эндпоинт `/transactions/fetch` запрашивает транзакции обмена для указанного адреса кошелька через TON API и сохраняет их в базе данных PostgreSQL.
- **Фильтрация транзакций**: Эндпоинт `/transactions/filter` позволяет фильтровать сохраненные транзакции по адресу кошелька и временному диапазону.
- **Документация API**: Автоматически генерируемая документация доступна по адресам `/docs` (Swagger UI) и `/redoc` (ReDoc).

## Технологии
- **Backend**: FastAPI, Python 3.11
- **База данных**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Драйвер БД**: `psycopg` 3.2.7
- **Запросы к TON API**: `aiohttp` 3.10
- **Контейнеризация**: Docker, Docker Compose
- **Окружение**: `python-dotenv` для управления переменными окружения

## Требования
- Python 3.11+
- Docker и Docker Compose
- Ключ API от TON API (получите через `@tonapi_bot` в Telegram)

## Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/gr33njj/stonfi-transaction-service.git
cd stonfi-transaction-service
```

### 2. Настройте переменные окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql+psycopg2://postgres:db_password@db:5432/stonfi_db
TONAPI_KEY=ton_api_key
```

- Замените `db_password` на пароль для PostgreSQL.
- Замените `ton_api_key` на ключ от @tonapi_bot.

### 3. Запустите приложение

```bash
docker-compose up --build
```

Приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000)

### 4. Доступ к документации

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Использование API

### Получение транзакций

**Эндпоинт**: `POST /transactions/fetch`

**Пример запроса**:

```bash
curl -X POST "http://localhost:8000/transactions/fetch" -H "Content-Type: application/json" -d "{"wallet_address": "EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt"}"
```

**Пример ответа**:

```json
[
  {
    "id": 1,
    "wallet_address": "EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt",
    "transaction_hash": "abc123...",
    "pool_address": "EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt",
    "amount_in": 1.5,
    "amount_out": 0.0,
    "token_in": "TON",
    "token_out": "Unknown",
    "timestamp": "2025-05-03T12:00:00",
    "status": "success"
  }
]
```

### Фильтрация транзакций

**Эндпоинт**: `POST /transactions/filter`

**Пример запроса**:

```bash
curl -X POST "http://localhost:8000/transactions/filter" -H "Content-Type: application/json" -d "{
  \"wallet_address\": \"EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt\",
  \"start_time\": \"2023-01-01T00:00:00\",
  \"end_time\": \"2025-12-31T23:59:59\"
}"
```

**Пример ответа**:

```json
[
  {
    "id": 1,
    "wallet_address": "EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt",
    "transaction_hash": "abc123...",
    "pool_address": "EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt",
    "amount_in": 1.5,
    "amount_out": 0.0,
    "token_in": "TON",
    "token_out": "Unknown",
    "timestamp": "2025-05-03T12:00:00",
    "status": "success"
  }
]
```

## Структура проекта

```
stonfi-transaction-service/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI приложение
│   ├── database.py       # Настройка SQLAlchemy и подключение к БД
│   ├── models.py         # Модели SQLAlchemy
│   ├── schemas.py        # Pydantic-схемы для валидации
│   ├── tonapi_client.py  # Клиент для TON API
├── Dockerfile            # Конфигурация Docker-образа
├── docker-compose.yml    # Конфигурация сервисов (web, db)
├── requirements.txt      # Зависимости Python
├── .env                  # Переменные окружения (не в Git)
├── .gitignore            # Игнорируемые файлы
└──  README.md             # Документация проекта
```
