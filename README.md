# FastAPI Starter Project

A clean starter template for a FastAPI backend.

## Project Structure

```text
app/
  api/
    routes.py
  main.py
tests/
requirements.txt
```

## Quick Start

1. Create a virtual environment:

```powershell
python -m venv .venv
```

2. Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the server:

```powershell
uvicorn app.main:app --reload
```

5. Open docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Run Tests

```powershell
pytest -q
```
