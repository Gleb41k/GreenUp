.PHONY: help run dev migrate upgrade seed test lint format clean manual app stop start

help:
	@echo "FastAPI Enterprise"
	@echo ""
	@echo "  run        - запуск API"
	@echo "  dev        - запуск с hot-reload"
	@echo "  migrate    - создать миграцию"
	@echo "  upgrade    - применить миграции"
	@echo "  seed       - заполнить БД тестовыми данными"
	@echo "  test       - запустить тесты"
	@echo "  lint       - проверка flake8"
	@echo "  format     - формат кода black"
	@echo "  clean      - очистка"
	@echo "  setup      - установка проекта"
	@echo "  manual     - установка проекта для локального python"
	@echo "  app        - зайти в контейнер приложения"
	@echo "  stop		- остановить все контейнеры"
	@echo "  start		- запустиь все контейнеры"


app:
	docker compose exec app bash

stop:
	docker compose stop

start:
	docker compose up -d

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
	fi

	@echo "🔑 Генерация JWT_SECRET_KEY..."
	@JWT_SECRET_KEY=$$(openssl rand -hex 32); \
	sed -i'' -e "s|JWT_SECRET_KEY=<GENERATED>|JWT_SECRET_KEY=$$JWT_SECRET_KEY|" .env; \
	echo "JWT_SECRET_KEY сгенерирован и добавлен в .env"

	@echo "🐳 Запуск Docker..."
	docker compose up -d

	@echo "✅ Setup завершён."

manual:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
	fi

	@echo "🔑 Генерация JWT_SECRET_KEY..."
	@JWT_SECRET_KEY=$$(openssl rand -hex 32); \
	sed -i'' -e "s|JWT_SECRET_KEY=<GENERATED>|JWT_SECRET_KEY=$$JWT_SECRET_KEY|" .env; \
	echo "JWT_SECRET_KEY сгенерирован и добавлен в .env"

	@echo "🐳 Запуск Docker..."
	docker compose up celery rabbitmq redis db -d

	@echo "📦 Установка зависимостей через Poetry..."
	poetry install --no-root

	@echo "📜 Применение миграций..."
	poetry run alembic upgrade head

	@echo "✅ Setup завершён."


run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	@read -p "Message: " msg; \
	poetry run alembic revision --autogenerate -m "$$msg"

upgrade:
	poetry run alembic upgrade head

seed:
	python scripts/seed.py

test:
	@echo "Running tests..."
	@poetry run pytest -v

test-cov:
	@echo "Running tests with coverage..."
	@poetry run pytest --cov=app --cov-report=term-missing --cov-report=html

test-unit:
	@poetry run pytest tests/unit -v

test-feature:
	@poetry run pytest tests/feature -vv

format:
	@echo "Formatting code with black + isort..."
	@poetry run black app tests
	@poetry run isort app tests

lint:
	@echo "Linting with flake8..."
	@poetry run flake8 app tests

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .coverage htmlcov