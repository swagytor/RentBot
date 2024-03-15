
### Команда для создания миграций(makemigrations)
```bash
alembic revision --autogenerate -m "message"
```

### Команда для миграций(migrate)
```bash
alembic upgrade head
```

### Команда для миграций(migrate)
```bash
alembic downgrade -1
```

### Запуск сервера
```bash
uvicorn app.main:app --reload --host 0.0.0.0
```