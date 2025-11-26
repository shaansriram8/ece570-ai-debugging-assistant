# AI Code Quality & Bug Explanation Assistant

An AI-powered debugging assistant that analyzes source code and error messages to provide structured explanations and fix suggestions. This project uses a FastAPI backend with Hugging Face Inference models and a React frontend.

## 🎯 Project Overview

This tool helps developers and students understand and fix code errors by:
- Providing clear **root-cause explanations** of bugs
- Suggesting **concrete fixes** or debugging steps  
- Assigning a **confidence score** (0-100) for the explanation
- Using **multiple AI models** for verification
- **Caching responses** for instant feedback on known issues

**Target Users:** Junior software engineers, students, and developers debugging complex errors.

## 📁 Project Structure

```
ece570-final-project/
├── backend/              # FastAPI backend service (Python)
│   ├── main.py           # Application entry point
│   ├── services/         # Core business logic (cache, etc.)
│   ├── hf_client.py      # Hugging Face API client
│   ├── evaluation_dataset.json # Dataset for evaluation
│   └── ...
│
└── frontend/             # React frontend application (TypeScript)
    ├── src/              # UI source code
    └── ...
```

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** (for the backend)
- **Node.js 18+** (for the frontend)
- **npm** or **bun** (package manager)

**You will also need:**
- A **Hugging Face API Key** (Free). Get one here: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

## 🛠️ Setup Instructions

### 1. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend/` directory:
    ```bash
    cp env.example .env
    ```
    Open `.env` and paste your Hugging Face API Key:
    ```ini
    HF_API_KEY=hf_your_token_here
    ```

5.  **Start the Backend Server:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    The backend will be running at `http://localhost:8000`.

### 2. Frontend Setup

1.  **Navigate to the frontend directory (in a new terminal):**
    ```bash
    cd frontend
    ```

2.  **Install Node dependencies:**
    ```bash
    npm install
    ```

3.  **Start the Frontend:**
    ```bash
    npm run dev
    ```
    The frontend will be running at `http://localhost:8000` (or `http://localhost:5173`).

## 📡 API Endpoints

- **`POST /analyze`**: Analyzes code and error message.
- **`GET /health`**: Checks backend health and model configuration.
- **Docs**: Visit `http://localhost:8000/docs` for interactive API documentation.

## 🔧 Configuration

You can tune the backend behavior in `backend/config.py` or via environment variables in `backend/.env`:

- `CACHE_ENABLED`: Enable/disable response caching (Default: True)
- `CACHE_TTL_SECONDS`: How long to cache responses (Default: 3600s)
- `PRIMARY_MODEL`: The main AI model to use (Default: Qwen2.5-Coder)

## ⚖️ Provenance & Attribution

### Original Code
- **Backend (`backend/`):** All Python source code (`main.py`, `hf_client.py`, `services/`, etc.) was written originally for this project with help from generative AI for debugging and help when writing boilerplate.
- **Frontend (`frontend/`):** The React/TypeScript frontend application was written originally for this project with help from generative AI for UI.
- **Evaluation Dataset (`backend/evaluation_dataset.json`):** Curated custom dataset for evaluating model performance.

### External Libraries
This project relies on the following open-source libraries:
- **FastAPI** & **Uvicorn**: Web server framework.
- **Pydantic**: Data validation.
- **React** & **Shadcn UI**: Frontend UI components.
- **Hugging Face Inference API**: Used for model inference (no local model weights required).

## 📊 Data & Model Handling

- **Models:** This project uses the Hugging Face Inference API. No large model weights need to be downloaded locally. The code automatically queries the configured models (`Qwen/Qwen2.5-Coder-7B-Instruct`) via the API.
- **Data:** The evaluation dataset is included in `backend/evaluation_dataset.json`. No external download is required.

## 📝 License

This is an academic project.
