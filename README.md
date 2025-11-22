# ECE 570 - AI Code Quality & Bug Explanation Assistant

An AI-powered debugging assistant that analyzes source code and error messages to provide structured explanations and fix suggestions using multiple language models.

## 🎯 Project Overview

This project helps developers and students understand and fix code errors by:
- Providing clear **root-cause explanations** of bugs
- Suggesting **concrete fixes** or debugging steps  
- Assigning a **confidence score** (0-100) for the explanation

**Target Users:** Junior software engineers, students in programming courses, developers encountering confusing errors.

## 📁 Project Structure

```
ece570-ai-debugging-assistant/
├── backend/              # FastAPI backend service
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Pydantic request/response models
│   ├── hf_client.py     # Hugging Face Inference API client
│   ├── aggregator.py    # Multi-model response aggregation
│   ├── json_handler.py  # JSON extraction and repair
│   ├── scorer.py        # Quality scoring utilities
│   ├── cache.py         # Response caching layer
│   ├── evaluator.py     # Evaluation pipeline
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Backend documentation
│
├── frontend/            # React/TypeScript frontend
│   ├── src/            # Source code
│   ├── public/         # Static assets
│   ├── package.json    # Node dependencies
│   └── README.md       # Frontend documentation
│
├── cursor.md           # Project context and requirements
├── LOVABLE_PROMPT.md   # Frontend generation prompt
└── README.md           # This file
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp env.example .env
   # Edit .env and add your HF_API_KEY
   ```

4. **Run the backend:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   bun install
   ```

3. **Configure API URL (optional):**
   Create a `.env` file in the frontend directory:
   ```bash
   VITE_API_BASE_URL=http://localhost:8000
   ```
   (Defaults to `http://localhost:8000` if not set)

4. **Run the development server:**
   ```bash
   npm run dev
   # or
   bun dev
   ```
   
   The frontend will be available at `http://localhost:5173` (or the port Vite assigns)

## 🔧 Technology Stack

### Backend
- **Framework:** FastAPI (Python)
- **API Client:** httpx (async HTTP client)
- **Validation:** Pydantic v2
- **Server:** Uvicorn
- **LLM API:** Hugging Face Inference API

### Frontend
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui
- **Routing:** React Router

## 📚 Documentation

- **Backend Documentation:** See [backend/README.md](backend/README.md)
- **Backend Report:** See [backend/BACKEND_REPORT.md](backend/BACKEND_REPORT.md)
- **Frontend Documentation:** See [frontend/README.md](frontend/README.md)
- **Project Requirements:** See [cursor.md](cursor.md)

## 🔑 Environment Variables

### Backend (.env in backend/)
- `HF_API_KEY` (required) - Your Hugging Face API key
- `PRIMARY_MODEL` (optional) - Primary model name
- `SECONDARY_MODEL` (optional) - Secondary model name
- `CACHE_ENABLED` (optional) - Enable/disable caching

### Frontend (.env in frontend/)
- `VITE_API_BASE_URL` (optional) - Backend API URL (defaults to `http://localhost:8000`)

## 📡 API Endpoints

### `GET /health`
Health check endpoint - returns backend status and configuration.

### `POST /analyze`
Main analysis endpoint - analyzes code and error message.

**Request:**
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
    "models_used": ["01-ai/Yi-1.5B-Coder"],
    "total_latency_ms": 1200.5,
    "from_cache": false
  }
}
```

## 🧪 Evaluation

Run the evaluation pipeline:

```bash
cd backend
python evaluator.py
```

This will:
- Load examples from `evaluation_dataset.json`
- Run analysis on each example
- Compute metrics (valid JSON rate, scores, latency)
- Save results to `evaluation_results.json`

## 🏗️ Development

### Backend Development
- The backend uses async/await for parallel model calls
- JSON extraction and repair handles malformed model outputs
- Caching reduces redundant API calls

### Frontend Development
- The frontend is a thin client - all logic is in the backend
- Uses React hooks for state management
- Responsive design with Tailwind CSS

## 📝 Code Attribution

### Original Code
- All backend logic in `backend/` - written by student
- All frontend logic in `frontend/` - generated via lovable.dev

### Adapted/Used Libraries
- **FastAPI:** Web framework
- **Pydantic:** Data validation
- **httpx:** Async HTTP client
- **Hugging Face Inference API:** Model inference service
- **React:** Frontend framework
- **shadcn/ui:** UI component library

## 🔒 Security Notes

- Never commit `.env` files containing API keys
- The `.gitignore` file is configured to exclude sensitive files
- Use `env.example` files to document required environment variables

## 📄 License

This is an academic project for ECE 570 at Purdue University.

## 🤝 Contributing

This is a course project. See `cursor.md` for project requirements and context.

