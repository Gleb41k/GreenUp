#!/bin/bash
set -e

## Ждём БД
until pg_isready -h db -p 5432 -U postgres; do
    echo "PostgreSQL not ready, retrying in 3s..."
    sleep 3
done

# Получаем путь к виртуальному окружению Poetry
VENV_PATH=$(poetry env info -p)

poetry lock

if [ -z "$VENV_PATH" ]; then
    echo "Виртуальное окружение Poetry не найдено. Создаём..."
    poetry install --no-root
    VENV_PATH=$(poetry env info -p)
fi

# Активируем виртуальное окружение для текущего скрипта
source "$VENV_PATH/bin/activate"


if [ "$APP_ENVIRONMENT" = "dev" ]; then
    echo "Running in development mode. Installing all dependencies..."
    # Проверка и установка всех групп зависимостей: main, dev, test
    poetry install --no-root
fi

# Запускаем команду, переданную в контейнер
exec "$@"