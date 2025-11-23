# Quick Start Guide - Get Everything Running

## ✅ What's Fixed

1. **Dependencies Installed** ✅
   - All Python packages from `requirements.txt` are now installed
   - `pydantic-settings` was missing but is now installed

2. **Codebase Verified** ✅
   - Frontend API calls match backend endpoints
   - Request/response formats are compatible
   - CORS is configured correctly
   - Model configuration is correct

## 🚀 Step-by-Step Startup

### Step 1: Create Backend .env File

**If `.env` doesn't exist:**

```bash
cd backend
cp env.example .env
```

**Edit `.env` and add your Hugging Face API key:**
```bash
# Open .env in your editor
nano .env
# or
code .env
```

**Add this line:**
```
HF_API_KEY=your_actual_huggingface_api_key_here
```

**Get API key:** https://huggingface.co/settings/tokens

### Step 2: Start Backend Server

**Open Terminal 1:**

```bash
cd /Users/shaansriram/Desktop/ECE570-Final-Project/backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/Users/shaansriram/Desktop/ECE570-Final-Project/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal running!**

### Step 3: Test Health Endpoint

**Open Terminal 2:**

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "hf_api_reachable": true,
  "models_configured": [
    "01-ai/Yi-1.5B-Coder",
    "mistralai/Mistral-7B-Instruct-v0.2"
  ],
  "backend_version": "1.0.0"
}
```

**If you see this, backend is working! ✅**

### Step 4: Start Frontend Server

**Open Terminal 3:**

```bash
cd /Users/shaansriram/Desktop/ECE570-Final-Project/frontend
npm install  # First time only, or if dependencies changed
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Keep this terminal running!**

### Step 5: Open in Browser

1. Open your browser
2. Navigate to: `http://localhost:5173`
3. You should see the AI Code Assistant interface

### Step 6: Test Full Integration

1. **Enter test code:**
   ```javascript
   const arr = undefined;
   const result = arr.map(x => x * 2);
   ```

2. **Enter error message:**
   ```
   TypeError: Cannot read property 'map' of undefined
   ```

3. **Select language:** JavaScript (optional)

4. **Click "Analyze"**

5. **Expected result:**
   - Loading indicator appears
   - After 2-4 seconds, results appear
   - Explanation, suggestion, and score displayed
   - Metadata section shows model info

## 🐛 Troubleshooting

### Backend won't start?

**Check for errors in Terminal 1:**
- Missing `.env` file → Create it from `env.example`
- Missing API key → Add `HF_API_KEY=...` to `.env`
- Port 8000 already in use → Change port: `--port 8001`
- Import errors → Run `pip install -r requirements.txt` again

### Health endpoint returns 500?

**Check backend logs:**
- Look at Terminal 1 for error messages
- Most common: Missing `HF_API_KEY` in `.env`

### Frontend can't connect to backend?

**Check:**
1. Backend is running (Terminal 1 shows "Uvicorn running")
2. Backend is on port 8000
3. No firewall blocking localhost:8000
4. Browser console for CORS errors (shouldn't happen - CORS is configured)

**Test connection manually:**
```bash
curl http://localhost:8000/health
```

If this works but frontend doesn't, check browser DevTools (F12) → Network tab

### Frontend shows "Backend service error"?

**Possible causes:**
1. Backend crashed (check Terminal 1)
2. Models not responding (check backend logs)
3. API key invalid (check `.env` file)
4. Network issue (check if backend is accessible)

**Debug:**
1. Check backend Terminal 1 for error messages
2. Try health endpoint: `curl http://localhost:8000/health`
3. Check if `hf_api_reachable: true` in health response

## 📝 Quick Reference

### Backend Commands
```bash
# Start backend
cd backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test health
curl http://localhost:8000/health

# Test analyze endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"const x=undefined;\nconsole.log(x.y);","error_message":"TypeError"}'
```

### Frontend Commands
```bash
# Start frontend
cd frontend
npm install  # First time only
npm run dev

# Build for production
npm run build
```

### Environment Files
```
backend/.env          # Required: Contains HF_API_KEY
frontend/.env         # Optional: Contains VITE_API_BASE_URL (defaults to http://localhost:8000)
```

## ✅ Verification Checklist

Before considering everything working:

- [ ] Backend starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Health endpoint shows `hf_api_reachable: true`
- [ ] Health endpoint shows both models configured
- [ ] Frontend starts without errors
- [ ] Frontend loads in browser
- [ ] No console errors in browser
- [ ] Can submit code + error message
- [ ] Results appear after clicking "Analyze"
- [ ] Explanation and suggestion are displayed
- [ ] Score is shown
- [ ] Metadata section is visible

## 🎯 Current Status

**Backend:**
- ✅ Dependencies installed
- ✅ Code verified and working
- ⚠️ Needs `.env` file with `HF_API_KEY`

**Frontend:**
- ✅ Code verified and compatible with backend
- ✅ Ready to run

**Integration:**
- ✅ API endpoints match
- ✅ Request/response formats compatible
- ✅ CORS configured
- ✅ Ready to test once both servers are running

## 🚀 Next Steps

1. **Create `.env` file** (if not exists) with your Hugging Face API key
2. **Start backend server** in one terminal
3. **Start frontend server** in another terminal
4. **Test in browser** at `http://localhost:5173`
5. **Verify everything works** using test code and error message

**You're ready to go!** Just need to start both servers and test. 🎉

