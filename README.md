# 📌 Проект: Telegram-бот автоответчик

## 🛠️ Технологический стек

* **Язык:** Python 3.12+
* **База данных:** PostgreSQL
* **Очереди:** Celery + RabbitMQ
* **Бот:** Pyrogram
* **Миграции:** Alembic
* **Тестирование:** Pytest
* **Контейнеризация:** Docker, Docker Compose

---

## 🚀 Установка и запуск проекта

### 1️⃣ Клонирование репозитория

```bash
# Клонируем репозиторий
git clone https://github.com/Pu104ver/funnel.git
cd funnel
```

### 2️⃣ Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3️⃣ Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4️⃣ Настройка переменных окружения

Создай `.env` файл в корне проекта и добавь нужные поля (пример можешь взять из .env_example с вариантом для запуска с помощью докера):

```env
BOT_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
POSTGRES_ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@db/your_db_name
POSTGRES_DATABASE_URL=postgresql://postgres:postgres@db/your_db_name

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=your_db_name
POSTGRES_HOST=db
POSTGRES_PORT=5432

RABBITMQ_URL=pyamqp://guest:guest@rabbit//
REDIS_URL=redis://redis_cont:6379/0
DEBUG=True

```

---

## 🗄️ Настройка базы данных

### 5️⃣ Запуск локальной PostgreSQL через Docker

```bash
docker run --name pg_db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=db_name -p 5432:5432 -d postgres
```

### 6️⃣ Применение миграций

```bash
alembic upgrade head
```

---

## 🤖 Настройка Telegram-бота

1. Зарегистрируй бота в [@BotFather](https://t.me/BotFather), получи `BOT_TOKEN`.
2. Получи `API_ID` и `API_HASH` на [my.telegram.org](https://my.telegram.org/).
3. Добавь их в `.env` файл.

Запуск бота:

```bash
python -m app.bot.bot
```

---

## 🐳 Запуск через Docker

### 7️⃣ Собрать и запустить контейнеры

```bash
docker-compose up --build
```

### 8️⃣ Остановить контейнеры

```bash
docker-compose down
```

## 🧪 Запуск тестов

```bash
pytest -s
```

---

## 🛠 Полезные команды

### Проверка статуса миграций

```bash
alembic current
```

### Создание новой миграции

```bash
alembic revision --autogenerate -m "Добавил новую таблицу"
```

### Откат миграции

```bash
alembic downgrade -1
```

### Команды из под докер-контейнера

```bash
docker compose exec [OPTIONS] SERVICE COMMAND [ARGS...]
```

Например:

```bash
docker compose exec bot sh
```

---

## 📌 Заключение

Теперь ты знаешь, как запустить проект с нуля. Если возникли вопросы — пиши в Telegram🚀!![1740088944957](image/README/1740088944957.png)
