# Backend - FastAPI

REST API developed with FastAPI.

## Setup

1. From the project root, activate the virtual environment:
```bash
source gid_env/bin/activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

## Running

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

## Configuration

Environment variables are configured in `.env`:

- `APP_NAME` - Application name
- `APP_VERSION` - Application version
- `DEBUG` - Debug mode (True/False)
- `ENVIRONMENT` - Environment (development/production)
- `HOST` - Server host
- `PORT` - Server port
- `SECRET_KEY` - Secret key for JWT tokens
- `ALLOWED_ORIGINS` - CORS allowed origins (comma-separated)
- `LOG_LEVEL` - Logging level
