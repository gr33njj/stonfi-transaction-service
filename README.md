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
git clone https://github.com/your-username/stonfi-transaction-service.git
cd stonfi-transaction-service