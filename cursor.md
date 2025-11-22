# Agent: ECE 570 AI Debugging Assistant – Project Context

## 1. Course & Track

- Course: **ECE 57000 – Introduction to Artificial Intelligence / Machine Learning**, Purdue University.  
- Project track: **Track 2 – ProductPrototype (From Problem to Prototype)**.  

The project must ultimately deliver:

- **4–6 page anonymous report** in ICLR style (4–6 pages of main text; references and appendix do not count).
- **Code ZIP** with a clear `README.md` explaining:
  - Code structure and dependencies.
  - How to run the backend and frontend.
  - Which parts are written by the student vs. adapted/copied (with attribution).
- **5-minute demo video** showing the prototype in action.
- **BetterPoster-style poster**, 48" x 36" landscape, with a large, clear central takeaway.

This context should influence design decisions: emphasize practical usefulness, system design quality, and demonstrable performance.

---

## 2. High-Level Project Summary

**Working name:** AI-Powered Code Quality & Bug Explanation Assistant.

**Core problem:**  
Developers and students spend too much time interpreting cryptic error messages and manually debugging with low-level logs, stack traces, and scattered forum answers. This is slow, mentally taxing, and often confusing.

**Project goal:**  
Build an AI assistant that consumes **source code + error message** and returns **structured, actionable feedback**:

- A clear **root-cause explanation** of the bug.
- A concrete **suggested fix** (or next debugging steps).
- A **numeric quality/confidence score** (0–100) for the explanation.

**Target users:**

- Junior software engineers.
- Students in programming-heavy courses.
- Developers who regularly hit confusing runtime or compile-time errors.

The project is **not** about inventing a new ML algorithm. It is about designing and building a **robust, usable system** around existing LLMs.

---

## 3. System Architecture (Conceptual)

**Overall architecture (as of Checkpoint 2):**

- **Frontend**
  - Planned: TypeScript frontend (via lovable.dev).
  - Role: Capture user inputs (code, error message, optional metadata), send to backend, and present structured results.
  - UI is thin: it should not contain core logic, only display and interaction.

- **Backend**
  - Framework: **FastAPI** (Python), asynchronous.
  - Role: Orchestrate calls to external models, parse/repair JSON, compute scores, and expose a stable API to the frontend.

- **Models (via Hugging Face Inference API)**
  - **Yi-Coder-1.5B** as a primary code model.
  - **Mistral-7B** as a second model for ensemble / fallback.
  - Additional models may be considered later, but these two are the main ones.

- **Core processing workflow**
  1. Frontend sends a request with code + error message (and optional metadata).
  2. Backend builds a **prompt** that instructs the model(s) to produce a structured JSON response (explanation, suggestion, score, etc.).
  3. Backend calls one or more LLMs (Yi-Coder, Mistral) via the HF Inference API, preferably in parallel.
  4. Backend **extracts and validates JSON** from each model’s text output, attempting to repair malformed JSON.
  5. Backend **aggregates** the multiple model responses into a single, unified answer (ensemble behavior).
  6. Backend computes a **quality score** and attaches metadata (latencies, models used, cache hits).
  7. Backend returns a **clean, fixed-schema JSON** object to the frontend.

---

## 4. Progress Summary (Checkpoint 1 → Checkpoint 2)

### Checkpoint 1 (CP1): Single-Model Prototype

Core achievements:

- Implemented a helper function to call the HF Inference API:
  - Low temperature (around 0.2) for more deterministic JSON-like responses.
  - Reasonable `max_new_tokens` and timeout settings.
- Implemented JSON extraction logic:
  - Uses a regex to extract the first `{ ... }` block from the model’s text output.
  - Attempts to parse it as JSON and normalizes keys.
  - Fails gracefully if parsing doesn’t work.
- Established a **single-model pipeline**:
  - Input: code + error message.
  - Output: explanation, suggestion, and a score in JSON (when parsing succeeds).
- Demonstrated on example bugs (e.g., calling `.map` on `undefined` in JavaScript) with reasonable explanations and suggested fixes.

### Checkpoint 2 (CP2): Reliability, Ensemble, and Evaluation

Focus shifted from “just works” to **reliability + measurable performance**.

Key additions:

- **Multi-model async inference**
  - Function like `evaluate_code(prompt, models)` that:
    - Calls multiple models in parallel (`asyncio.gather`).
    - Wraps each model call in try/except so a single failure does not crash the overall request.
    - Parses each model’s output into JSON using the extraction/repair logic.
    - Aggregates multiple model outputs into a single final result via an `aggregate_results` step.

- **Automated explanation scoring**
  - Function like `score_explanation(pred, gold)` that:
    - Compares the predicted explanation/suggestion to a gold/reference explanation.
    - Uses a semantic similarity function (with a threshold, e.g., 0.7) to decide if they “match.”
    - Produces a **0–100 score** based on how many fields (e.g., explanation, suggestion) match.
    - Handles missing fields gracefully instead of crashing.

- **Evaluation dataset**
  - Constructed a small evaluation set (~50) of code + error examples with reference explanations.
  - Used this dataset to compute:
    - Valid JSON rate.
    - Mean explanation quality score.
    - Average latency.

- **Caching and performance improvements**
  - Implemented a caching layer to avoid repeated HF calls for identical requests.
  - Async multi-model pipeline significantly reduced latency compared to sequential calls.

Observed improvements (example numbers from CP2 evaluation):

- **Valid JSON rate:** increased from roughly 68% to ~94%.
- **Mean explanation quality score:** increased from low 70s to mid 80s (0–100 scale).
- **Average latency:** decreased from ~5+ seconds to ~3–4 seconds.

These are approximate, but the trend is important: CP2 shows **better reliability, better perceived quality, and lower latency**.

---

## 5. Backend Responsibilities (What This Agent Should Prioritize)

The backend is the heart of the system. Cursor should help keep it clean, consistent, and robust.

### 5.1 Stable API Surface

Design and maintain a clear primary endpoint (e.g., `POST /analyze`):

- **Request body** fields (example):
  - `code: string`
  - `error_message: string`
  - Optional: `language: string`
  - Optional: `mode: "quick" | "detailed"` or similar

- **Response body** (fixed schema) fields (example):
  - `explanation: string`
  - `suggestion: string`
  - `score: number` (0–100)
  - Optional: `severity: string` or `bug_type: string`
  - `meta: {`
    - `models_used: string[]`
    - `per_model_latency_ms: Record<string, number>`
    - `total_latency_ms: number`
    - `had_repair: boolean`
    - `from_cache: boolean`
    - `backend_version?: string`
    - `}`
  
Also desirable:

- A simple healthcheck endpoint (e.g., `GET /health`) that indicates:
  - Backend is running.
  - HF API is reachable (or not).
  - Which models are configured.

Cursor should treat this API as a **contract** with the frontend and avoid breaking it without deliberate changes.

---

## 6. Model Orchestration & JSON Handling

### 6.1 Prompt Construction

- Build prompts that:
  - Clearly show the code and error message.
  - Instruct the model to output **only** a JSON object with the expected fields.
  - Include any helpful context (language/framework, debugging hints).

### 6.2 Multi-Model Calling

- Support multiple models (Yi-Coder, Mistral, etc.) with:
  - Async HTTP calls to HF Inference API.
  - Per-model timeouts and error handling.
  - Configurable model list (from environment or config file).

### 6.3 Output Aggregation

- Parse each model’s output into a common JSON schema.
- Aggregate using a clear strategy, for example:
  - Majority vote / consensus on explanation.
  - Prefer primary model unless it fails; fallback to secondary.
  - Combine scores or pick the best candidate based on heuristics.

### 6.4 JSON Extraction, Repair, and Validation

- Extract the JSON block from free-form text reliably.
- Attempt repair when:
  - There are minor syntax issues (e.g., trailing commas, wrong quotes).
  - Required fields are missing but can be inferred or defaulted.
- Enforce that the final response:
  - Has all required keys.
  - Has correct value types.
  - Never returns malformed JSON to the frontend.

---

## 7. Evaluation, Scoring, and Experiment Runner

### 7.1 Per-Response Scoring

- Implement logic to assign a 0–100 quality score for each explanation, for evaluation purposes.
- For the live system, the score may be:
  - Directly from the model’s own self-assessment, or
  - Derived from internal heuristics (e.g., whether all fields are filled, presence of key concepts).

### 7.2 Offline Evaluation

Provide a way (CLI or script entrypoint) to:

- Run the full backend logic on a fixed evaluation dataset of `(code, error, gold_explanation)` triples.
- Compute and store:
  - Valid JSON rate.
  - Mean explanation score.
  - Latency statistics (per model and total).
- Output results in a machine-readable format (e.g., JSON or CSV) that can later be turned into:
  - Tables and figures for the report.
  - Plots for the poster.

Cursor should keep the evaluation pipeline simple and reproducible.

---

## 8. Caching, Logging, and Configuration

### 8.1 Caching

- Cache responses based on:
  - Code (or a hash of it).
  - Error message.
  - Model configuration (which models, which settings).
- Return cached results when identical requests are repeated.
- Indicate in the `meta` field if the response came from cache.

### 8.2 Logging & Observability

- Use structured logs:
  - Request IDs / trace IDs.
  - High-level inputs (without logging full source code if privacy is a concern).
  - Model errors, timeouts, and parse failures.
  - Whether JSON repair was used.

- Ensure logs are useful for:
  - Debugging backend errors.
  - Understanding why a particular request behaved oddly.

### 8.3 Configuration & Secrets

- Read HF API keys and model names from environment variables or a config file.
- Keep a "model registry" or config block that defines:
  - Which models are active.
  - Model-specific parameters (e.g., temperature, max tokens).
- Make it easy to run:
  - In dev mode (e.g., using fewer models).
  - In a more robust prod-like configuration.

---

## 9. Frontend (lovable.dev + TypeScript) Expectations

Cursor should assume:

- Frontend will be a TypeScript app generated/edited via lovable.dev.
- It will:
  - Provide a textarea or code editor for the code snippet.
  - Provide a field for the error message or stack trace.
  - Optionally let the user specify language/mode.
  - Call the backend `POST /analyze` (or similar) endpoint.
  - Render:
    - Explanation
    - Suggested fix
    - Score
    - Any metadata (like which models were used, latency, etc.).
  - Show loading and error states in a clean way.

The frontend **must not** reimplement core logic; it should rely on the backend’s structured JSON.

---

## 10. Constraints & Preferences

- The project is evaluated as a **ProductPrototype**:
  - Focus on **real user problem**, **system design**, and **engineering execution**.
  - Show that the tool actually helps with debugging.
- The final report, poster, and code must be **anonymous** (no student names, IDs, or personal identifiers).
- Code should be:
  - Clear and maintainable.
  - Organized to make evaluation easy (e.g., a clear entrypoint to run experiments).
  - Explicit about what is original vs. adapted.

---

## 11. How This Agent Should Behave in Cursor

When operating in this repository, this agent should:

- **Preserve and respect the API contract** between backend and frontend.
- **Improve reliability**:
  - Favor changes that increase JSON validity, explanation quality, and robustness.
- **Improve performance**:
  - Reduce latency where reasonable without overcomplicating the system.
- **Preserve evaluation hooks**:
  - Make sure experiment runners and metrics remain easy to use.
- **Avoid unnecessary complexity**:
  - Don’t introduce extra frameworks or patterns unless they clearly help the Track 2 goals.
- **Explain trade-offs**:
  - When suggesting non-trivial changes, briefly note how they impact:
    - Developer experience.
    - Reliability and speed.
    - Ease of writing the report and preparing the demo.

This context should be used as the persistent “project brain” for all code completions, refactors, and design suggestions in this workspace.
