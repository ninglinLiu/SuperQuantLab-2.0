# SuperQuantLab 2.0 Backend

## Setup

### Using Poetry (Recommended)

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run development server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Using uv

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

- `app/main.py` - FastAPI application entry point
- `app/core/` - Configuration
- `app/models/` - Pydantic models
- `app/data/` - Data loading and transformation
- `app/strategies/` - Trading strategies
- `app/engines/` - Backtest, behavior, chaos, microstructure, meta engines
- `app/services/` - LLM strategy generation service
- `app/api/` - API routes

## Testing

```bash
poetry run pytest
```

