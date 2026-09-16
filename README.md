# Task Management API

A small FastAPI service for creating and managing tasks in memory.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Test

```powershell
python -m pytest
```

Tasks have an `id`, `title`, `description`, `status`, and `priority`. Valid statuses are
`todo`, `in_progress`, and `done`; valid priorities are `low`, `medium`, and `high`.