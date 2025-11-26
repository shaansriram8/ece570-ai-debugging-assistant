# Backend - AI Debugging Assistant

The FastAPI backend service that powers the debugging assistant. It handles request validation, calls Hugging Face inference models, caches results, and aggregates responses.

## ⚡️ Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- A Hugging Face API Key (Get it [here](https://huggingface.co/settings/tokens))

### 2. Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp env.example .env
# EDIT .env and add your HF_API_KEY!

# 3. Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Running Tests

To verify the backend is working correctly (including the cache system):

```bash
# Run cache integration tests
python -m pytest tests/test_cache_integration.py -v
```

## 📂 Key Files

- `main.py`: API entry point and route definitions
- `hf_client.py`: Client for communicating with Hugging Face API
- `services/cache_service.py`: In-memory caching logic
- `validator.py`: Input validation logic
- `config.py`: Configuration settings

## ⚙️ Configuration

The backend is configurable via the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `HF_API_KEY` | **Required**. Your Hugging Face API token | - |
| `CACHE_ENABLED` | Enable response caching | `true` |
| `CACHE_MAX_SIZE` | Max number of cached responses | `512` |
| `CACHE_DEFAULT_TTL_SECONDS` | Cache expiration time in seconds | `3600` |

## 📡 API Documentation

Once the server is running, visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
