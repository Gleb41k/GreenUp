# GreenUp Backend

## Быстрый старт

1. Склонируйте проект
2. Запуск через Docker (рекомендуется)
```shell
make setup
```

### Сервисы:

http://localhost:8080 — API<br/>
http://localhost:15672 — RabbitMQ Management (guest/guest)<br/>
http://localhost:6379 — Redis<br/>

## API Документация
После запуска:

Swagger: http://localhost:8000/docs<br/>
ReDoc: http://localhost:8000/redoc

## Тестирование
```shell
make test          # Все тесты
make test-cov      # С покрытием
make test-unit     # Все только unit тесты
make test-feature  # Все только feature тесты
```

## Команды (Makefile)

```shell
make run # запуск API"
```
```shell
make dev #запуск с hot-reload"
```
```shell
make migrate # создать миграцию"
```
```shell
make upgrade # применить миграции"
```
```shell
make lint  # проверка flake8"
```
```shell
make format # формат кода black"
```
```shell
make clean # очистка"
```
```shell
make setup # установка проекта"
```
