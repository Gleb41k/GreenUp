FROM python:3.14-slim

# Установка зависимостей системы
# Включает build-essential для сборки пакетов с C-расширениями (например, psycopg2-binary, argon2-cffi)
# и postgresql-client для pg_isready и других утилит.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    bash \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_VERSION=2.2.1
ENV POETRY_HOME=/opt/poetry

# Настройки для создания .venv внутри /app
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

# Добавление Poetry в PATH
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN pip install "poetry==${POETRY_VERSION}"

# Рабочая директория
WORKDIR /app

# Копируем только pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# УДАЛЯЕМ СТАРЫЙ .venv (если остался от кэша)
RUN rm -rf .venv

# Установка зависимостей
# poetry lock не нужен, т.к. мы скопировали poetry.lock
# --no-root: устанавливаем только зависимости, без самого проекта (его нет)
# --only main: устанавливаем только основные зависимости, исключая dev и test для продакшена (если вы будете использовать этот образ для prod)
# Для dev-окружения (как у вас в docker-compose) можно убрать --only main и добавить [dev,test] в poetry install,
# но для универсальности оставим пока так, а для dev-окружения в docker-compose.yml
# будем устанавливать все зависимости, используя аргументы команды.
RUN poetry lock
RUN poetry install --no-root --only main

COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint
RUN chmod +x /usr/local/bin/docker-entrypoint

# Копируем код
COPY . .

# Запуск
EXPOSE 8000
ENTRYPOINT ["docker-entrypoint"]