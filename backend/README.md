# AI Code Quality & Bug Explanation Assistant - Backend

Backend API for the AI-powered code debugging assistant. This FastAPI application analyzes code and error messages to provide structured explanations and fix suggestions.

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── models.py               # Pydantic request/response models
├── config.py              # Configuration management
├── hf_client.py           # Hugging Face Inference API client
├── json_handler.py        # JSON extraction and repair utilities
├── aggregator.py          # Multi-model response aggregation
├── scorer.py              # Quality scoring utilities
├── cache.py               # Response caching layer
├── evaluator.py           # Evaluation pipeline
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── evaluation_dataset.json # Evaluation dataset
└── README.md              # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `HF_API_KEY`: Your Hugging Face API key (required)

### 3. Run the Backend

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `GET /health`

Health check endpoint. Returns backend status and configuration.

**Response:**
```json
{
  "status": "healthy",
  "hf_api_reachable": true,
  "models_configured": ["01-ai/Yi-1.5B-Coder", "mistralai/Mistral-7B-Instruct-v0.2"],
  "backend_version": "1.0.0"
}
```

### `POST /analyze`

Main analysis endpoint. Analyzes code and error message.

**Request Body:**
```json
{
  "code": "const arr = undefined;\nconst result = arr.map(x => x * 2);",
  "error_message": "TypeError: Cannot read property 'map' of undefined",
  "language": "javascript"
}
```

**Response:**
```json
{
  "explanation": "The variable 'arr' is undefined...",
  "suggestion": "Initialize 'arr' as an empty array...",
  "score": 85,
  "severity": "high",
  "bug_type": "null reference",
  "meta": {
    "models_used": ["01-ai/Yi-1.5B-Coder", "mistralai/Mistral-7B-Instruct-v0.2"],
    "per_model_latency_ms": {
      "01-ai/Yi-1.5B-Coder": 1200.5,
      "mistralai/Mistral-7B-Instruct-v0.2": 1500.2
    },
    "total_latency_ms": 1520.3,
    "had_repair": false,
    "from_cache": false,
    "backend_version": "1.0.0"
  }
}
```

## Running Evaluation

To run the evaluation pipeline on the evaluation dataset:

```bash
python evaluator.py
```

This will:
1. Load examples from `evaluation_dataset.json`
2. Run analysis on each example
3. Compute metrics (valid JSON rate, mean scores, latency)
4. Save results to `evaluation_results.json`

## Code Attribution

### Original Code
- All core logic in `main.py`, `hf_client.py`, `json_handler.py`, `aggregator.py`, `scorer.py`, `cache.py`, `evaluator.py` - written by student

### Adapted/Used Libraries
- **FastAPI**: Web framework (https://fastapi.tiangolo.com/)
- **Pydantic**: Data validation (https://docs.pydantic.dev/)
- **httpx**: Async HTTP client (https://www.python-httpx.org/)
- **Hugging Face Inference API**: Model inference service (https://huggingface.co/docs/api-inference/)

## Configuration

Key configuration options in `config.py`:
- `primary_model`: Primary model for analysis
- `secondary_model`: Fallback/secondary model
- `temperature`: Model temperature (default: 0.2)
- `max_new_tokens`: Maximum tokens to generate (default: 512)
- `cache_enabled`: Enable response caching (default: true)

## Development Notes

- The backend uses async/await for parallel model calls
- JSON extraction and repair handles malformed model outputs
- Caching reduces redundant API calls
- Evaluation pipeline supports offline metrics computation

## Troubleshooting

**"HF_API_KEY not configured"**
- Make sure you've created a `.env` file with your Hugging Face API key

**Model API errors**
- Check that your API key has access to the configured models
- Verify model names are correct in `config.py`

**Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

