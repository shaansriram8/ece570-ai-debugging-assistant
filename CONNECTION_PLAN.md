# Frontend-Backend Connection Plan

This document outlines the steps to connect your React frontend to your FastAPI backend.

## Current Status ✅

- **Frontend:** Already configured to call the API (see `frontend/src/pages/Index.tsx`)
- **Backend:** CORS middleware configured to allow all origins
- **API Endpoint:** Frontend expects `/analyze` endpoint (matches backend)
- **Request Format:** Frontend sends correct request structure

## Connection Steps

### Step 1: Verify Backend is Running

**Goal:** Ensure backend is accessible before connecting frontend.

1. **Start the backend:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Test the health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "hf_api_reachable": true,
     "models_configured": ["01-ai/Yi-1.5B-Coder", "mistralai/Mistral-7B-Instruct-v0.2"],
     "backend_version": "1.0.0"
   }
   ```

3. **Test the analyze endpoint manually:**
   ```bash
   curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{
       "code": "const arr = undefined;\nconst result = arr.map(x => x * 2);",
       "error_message": "TypeError: Cannot read property \"map\" of undefined",
       "language": "javascript"
     }'
   ```

   If this works, your backend is ready! ✅

### Step 2: Configure Frontend Environment (Optional)

**Goal:** Set up environment variables for API URL configuration.

1. **Create `.env` file in frontend directory:**
   ```bash
   cd frontend
   touch .env
   ```

2. **Add API URL to `.env`:**
   ```bash
   VITE_API_BASE_URL=http://localhost:8000
   ```

   **Note:** If you don't create this file, the frontend will default to `http://localhost:8000` anyway.

3. **For production deployment, update to production URL:**
   ```bash
   VITE_API_BASE_URL=https://your-backend-domain.com
   ```

4. **Add `.env` to `.gitignore`** (if not already there):
   - Check `frontend/.gitignore` contains `.env` or `*.local`

### Step 3: Start Frontend Development Server

**Goal:** Run frontend and connect to backend.

1. **Install frontend dependencies (if not done):**
   ```bash
   cd frontend
   npm install
   # or
   bun install
   ```

2. **Start the frontend:**
   ```bash
   npm run dev
   # or
   bun dev
   ```

3. **Frontend should start on:** `http://localhost:5173` (or port shown in terminal)

4. **Open in browser:** Navigate to the URL shown in terminal

### Step 4: Test the Connection

**Goal:** Verify frontend can successfully communicate with backend.

1. **Ensure both are running:**
   - Backend: `http://localhost:8000` (should see "Uvicorn running")
   - Frontend: `http://localhost:5173` (should see your app)

2. **Test in the browser:**
   - Enter sample code:
     ```javascript
     const arr = undefined;
     const result = arr.map(x => x * 2);
     ```
   - Enter error message:
     ```
     TypeError: Cannot read property 'map' of undefined
     ```
   - Select language: `javascript` (optional)
   - Click "Analyze"

3. **Expected behavior:**
   - ✅ Loading indicator appears
   - ✅ Results appear with explanation, suggestion, and score
   - ✅ No CORS errors in browser console

4. **Check browser console:**
   - Open DevTools (F12 or Cmd+Option+I)
   - Check Console tab for errors
   - Check Network tab to see the API request/response

### Step 5: Troubleshooting

#### Problem: CORS Errors

**Symptoms:**
```
Access to fetch at 'http://localhost:8000/analyze' from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Solution:**
- ✅ Backend already has CORS middleware configured (`allow_origins=["*"]`)
- If still seeing errors, verify backend is running and restart it

#### Problem: Connection Refused

**Symptoms:**
```
Failed to fetch
TypeError: Failed to fetch
```

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check backend is on port 8000: Check terminal output
3. Check firewall/security settings
4. Verify `VITE_API_BASE_URL` in frontend `.env` matches backend URL

#### Problem: 404 Not Found

**Symptoms:**
```
404 Not Found
```

**Solution:**
1. Verify endpoint path: Should be `/analyze` (not `/api/analyze`)
2. Check backend routes: `grep "@app.post" backend/main.py`
3. Verify API_BASE_URL doesn't have trailing slash: `http://localhost:8000` not `http://localhost:8000/`

#### Problem: 500 Internal Server Error

**Symptoms:**
```
Backend service error. Please try again later.
```

**Solution:**
1. Check backend terminal for error messages
2. Verify `.env` file exists in `backend/` with `HF_API_KEY`
3. Check backend logs for specific error
4. Test backend directly with curl (see Step 1)

#### Problem: Request Format Errors

**Symptoms:**
```
400 Bad Request
Invalid request. Please check your inputs.
```

**Solution:**
1. Verify request body format matches backend schema:
   - `code`: string (required)
   - `error_message`: string (required)  
   - `language`: string (optional)
2. Check browser Network tab to see actual request payload
3. Compare with backend `AnalyzeRequest` model in `backend/models.py`

### Step 6: Verify Full Integration

**Goal:** Confirm all features work end-to-end.

1. **Test with different languages:**
   - JavaScript
   - Python
   - C/C++
   - Leave language empty (auto-detect)

2. **Test error handling:**
   - Invalid code/error combination
   - Network error (stop backend, try request)
   - Empty inputs (should be prevented by frontend validation)

3. **Test results display:**
   - ✅ Explanation appears
   - ✅ Suggestion appears
   - ✅ Score displays correctly
   - ✅ Metadata section shows model info
   - ✅ Loading states work correctly

4. **Test cache behavior:**
   - Submit same request twice
   - Second request should be faster
   - Check `from_cache: true` in metadata

### Step 7: Production Deployment Considerations

**Goal:** Prepare for production deployment.

1. **Update CORS in backend (important for security):**
   ```python
   # In backend/main.py, change:
   allow_origins=["*"],  # Development only
   
   # To:
   allow_origins=["https://your-frontend-domain.com"],  # Production
   ```

2. **Environment variables for production:**
   - Backend: Update `.env` with production API keys
   - Frontend: Update `VITE_API_BASE_URL` to production backend URL
   - Build frontend: `npm run build` (creates `dist/` folder)

3. **Health check endpoint:**
   - Frontend could call `/health` on load to verify backend connectivity
   - Display backend status in UI

## Quick Start Checklist

- [ ] Backend running on `http://localhost:8000`
- [ ] Backend health check works: `curl http://localhost:8000/health`
- [ ] Backend `.env` file exists with `HF_API_KEY`
- [ ] Frontend dependencies installed: `npm install` in `frontend/`
- [ ] Frontend running on `http://localhost:5173`
- [ ] Frontend `.env` file exists (optional, defaults work)
- [ ] Test request works in browser
- [ ] No CORS errors in console
- [ ] Results display correctly

## Testing Commands

### Test Backend Directly
```bash
# Health check
curl http://localhost:8000/health

# Analyze endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "const x = undefined;\nconsole.log(x.y);",
    "error_message": "TypeError: Cannot read property \"y\" of undefined"
  }'
```

### Test Frontend API Call
Open browser console and run:
```javascript
fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    code: 'const x = undefined;\nconsole.log(x.y);',
    error_message: "TypeError: Cannot read property 'y' of undefined"
  })
})
.then(r => r.json())
.then(console.log)
.catch(console.error)
```

## Expected File Structure After Setup

```
ECE570-Final-Project/
├── backend/
│   ├── .env              # Contains HF_API_KEY
│   └── ...
├── frontend/
│   ├── .env              # Contains VITE_API_BASE_URL (optional)
│   └── ...
└── ...
```

## Summary

Your frontend is **already configured** to connect to the backend! The connection should work out of the box if:

1. ✅ Backend is running on port 8000
2. ✅ Frontend is running on port 5173
3. ✅ Both are on same machine (localhost)

The frontend code already:
- Uses correct endpoint (`/analyze`)
- Sends correct request format
- Handles errors appropriately
- Shows loading and error states

**You should be able to run both servers and test immediately!** 🚀

## Next Steps

1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: Navigate to frontend URL
4. Test: Enter code and error message, click Analyze
5. Verify: Results should appear within a few seconds

If you encounter any issues, refer to the troubleshooting section above.

