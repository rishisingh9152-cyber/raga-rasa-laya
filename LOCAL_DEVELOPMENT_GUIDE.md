# Local Development Setup Guide - RagaRasa Music Therapy

**Goal:** Set up the entire RagaRasa stack locally (Backend + Emotion Service + Frontend) for testing before cloud deployment.

**Total Setup Time:** ~30-40 minutes
**Estimated Testing Time:** ~20-30 minutes

---

## Prerequisites

Ensure you have the following installed:
- **Python 3.9+** ([download](https://www.python.org/downloads/))
- **Node.js 18+** ([download](https://nodejs.org/))
- **Git** (for version control)
- **MongoDB** (local or MongoDB Atlas connection string)
- **Text Editor/IDE** (VS Code recommended)

Verify installations:
```bash
python --version
node --version
npm --version
git --version
```

---

## Project Structure

```
Raga Rasa Laya/
├── Backend/                          # FastAPI backend
│   ├── main.py
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── routes/
│   ├── requirements.txt
│   ├── .env                          # Local backend config
│   └── venv/                         # Virtual environment
│
├── emotion_recognition/              # Flask emotion service
│   ├── api.py
│   ├── emotion_detector.py
│   ├── requirements.txt
│   ├── .env
│   └── venv/                         # Virtual environment
│
└── raga-rasa-soul-final-v2/          # React frontend
    ├── src/
    ├── package.json
    ├── vite.config.ts
    ├── .env.local                    # Local frontend config
    └── node_modules/
```

---

## Phase 1: Backend Setup (FastAPI)

### Step 1.1: Navigate to Backend Directory
```bash
cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\Backend"
```

### Step 1.2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 1.3: Activate Virtual Environment

**On Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry the activation command above.

**Expected output:** You should see `(venv)` prefix in your terminal.

### Step 1.4: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected:** All packages installed successfully (should take ~2-3 minutes)

### Step 1.5: Verify Backend Configuration

Check that your `.env` file has the correct settings for local development:

```env
# Backend/.env
EMOTION_SERVICE_URL=http://localhost:5000/detect
MONGODB_URI=mongodb://localhost:27017
API_BASE_URL=http://localhost:8000
PORT=8000
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

**Important:** Make sure `EMOTION_SERVICE_URL` points to your local emotion service (port 5000).

### Step 1.6: Verify MongoDB Connection

Option A: **Using Local MongoDB**
- Ensure MongoDB is running locally on port 27017
- Check connection: `python` → `from pymongo import MongoClient` → `MongoClient('mongodb://localhost:27017').list_database_names()`

Option B: **Using MongoDB Atlas** (Recommended if you already have it)
- Update `.env`: `MONGODB_URI=mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject`
- Test connection from Backend directory

### Step 1.7: Start Backend Server

From `Backend/` directory with `(venv)` activated:

```bash
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Verification:**
- Open browser → http://localhost:8000/docs
- You should see FastAPI Swagger documentation with all endpoints

✅ **Backend is running successfully!**

---

## Phase 2: Emotion Recognition Service Setup (Flask)

### Step 2.1: Open New Terminal Window/Tab

Keep the backend running. Open a new terminal.

### Step 2.2: Navigate to Emotion Service Directory
```bash
cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\emotion_recognition"
```

### Step 2.3: Create Virtual Environment
```bash
python -m venv venv
```

### Step 2.4: Activate Virtual Environment

**On Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

### Step 2.5: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** This may take longer (5-10 minutes) because it downloads the HSEmotion model (~500MB).

**Expected output:** All packages installed, model downloaded

### Step 2.6: Verify Configuration

Check `.env` file:
```env
# emotion_recognition/.env
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
```

### Step 2.7: Start Emotion Service

From `emotion_recognition/` directory with `(venv)` activated:

```bash
python api.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server. Do not use it in production deployment.
```

**Verification:**
- Open browser → http://localhost:5000/health
- Should return: `{"status":"OK"}`
- Try test endpoint: http://localhost:5000/test
- Should return emotion detection results

✅ **Emotion Service is running successfully!**

---

## Phase 3: Frontend Setup (React + Vite)

### Step 3.1: Open New Terminal Window/Tab

Keep backend and emotion service running. Open a new terminal.

### Step 3.2: Navigate to Frontend Directory
```bash
cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\raga-rasa-soul-final-v2"
```

### Step 3.3: Install Dependencies
```bash
npm install
```

**Expected:** All dependencies installed (2-5 minutes)

### Step 3.4: Verify Frontend Configuration

Check `.env.local` file:
```env
# .env.local
VITE_API_URL=http://127.0.0.1:8000
VITE_APP_NAME=RagaRasa Music Therapy
VITE_APP_VERSION=1.0.0
VITE_ENV=development
```

### Step 3.5: Start Frontend Development Server

From `raga-rasa-soul-final-v2/` directory:

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.0  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**Verification:**
- Open browser → http://localhost:5173
- You should see the RagaRasa Music Therapy interface
- No CORS errors in browser console

✅ **Frontend is running successfully!**

---

## Phase 4: Full-Stack Testing

### Test 1: Health Check All Services

**Terminal 1 (Backend):**
```
✅ http://localhost:8000/docs - Swagger UI visible
```

**Terminal 2 (Emotion Service):**
```
✅ http://localhost:5000/health - Returns {"status":"OK"}
```

**Terminal 3 (Frontend):**
```
✅ http://localhost:5173 - App loads, no errors
```

### Test 2: API Connection Test

In browser console (http://localhost:5173):
```javascript
// Test backend connectivity
fetch('http://127.0.0.1:8000/api/health')
  .then(r => r.json())
  .then(d => console.log('Backend:', d))
  .catch(e => console.error('Backend Error:', e))
```

**Expected:** Connection successful, no CORS errors

### Test 3: Emotion Detection Flow

1. Open http://localhost:5173
2. Navigate to emotion detection (if available in UI)
3. Trigger emotion detection
4. Check browser Network tab to see request to `http://127.0.0.1:8000/api/emotion`
5. Verify response returns emotion data

### Test 4: Database Connectivity

In Python shell (Backend):
```python
import asyncio
from app.database import get_database

async def test_db():
    db = await get_database()
    collections = await db.list_collection_names()
    print(f"Collections: {collections}")

asyncio.run(test_db())
```

**Expected:** Lists all MongoDB collections

### Test 5: API Endpoints Testing

Use the Swagger UI at http://localhost:8000/docs to test endpoints:

1. **GET** `/api/health` - Should return `{"status":"OK"}`
2. **POST** `/api/emotion/detect` - Test with sample text
3. **GET** `/api/songs` - Should return list of songs
4. **POST** `/api/recommendations/generate` - Generate recommendations

---

## Troubleshooting

### Issue: Backend won't start - Port 8000 already in use

**Solution:**
```bash
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
python main.py --port 8001
```

### Issue: Emotion Service won't start - "Module not found"

**Solution:**
```bash
# Reinstall requirements with verbose output
pip install -r requirements.txt --verbose

# If still failing, try installing specifically
pip install flask flask-cors numpy torch transformers
```

### Issue: Frontend shows CORS error

**Solution:**
1. Verify backend `.env` has correct `EMOTION_SERVICE_URL`
2. Verify frontend `.env.local` has correct `VITE_API_URL`
3. Check backend is running on correct port
4. Clear browser cache: `Ctrl+Shift+Delete`

### Issue: MongoDB connection timeout

**Solution:**
1. If using Atlas: Check IP is whitelisted (should be 0.0.0.0/0 for local testing)
2. If using local: Start MongoDB service
3. Test connection directly:
   ```bash
   python
   >>> from pymongo import MongoClient
   >>> MongoClient('YOUR_CONNECTION_STRING').admin.command('ismaster')
   ```

### Issue: Emotion model download fails

**Solution:**
```bash
# Download manually
python -c "from transformers import AutoModel; AutoModel.from_pretrained('SuperKogito/HSEmotion-onnx')"

# Or skip and use API endpoint
# Configure to use HTTP fallback instead of local model
```

---

## Quick Reference Commands

### Start All Services (Windows PowerShell)

Create `start_local_dev.ps1`:
```powershell
# Terminal 1: Backend
Start-Process powershell -ArgumentList {
    cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\Backend"
    .\venv\Scripts\Activate.ps1
    python main.py
}

# Terminal 2: Emotion Service
Start-Process powershell -ArgumentList {
    cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\emotion_recognition"
    .\venv\Scripts\Activate.ps1
    python api.py
}

# Terminal 3: Frontend
Start-Process powershell -ArgumentList {
    cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\raga-rasa-soul-final-v2"
    npm run dev
}

Write-Host "All services starting..."
```

Run with:
```bash
powershell -ExecutionPolicy Bypass -File start_local_dev.ps1
```

### Stop All Services

```bash
# Kill processes on ports
taskkill /F /IM python.exe  # Stops all Python
taskkill /F /IM node.exe    # Stops Node/npm
```

---

## Service Endpoints Reference

| Service | URL | Purpose |
|---------|-----|---------|
| **Backend** | http://localhost:8000 | API server |
| **Backend Docs** | http://localhost:8000/docs | Swagger UI |
| **Emotion Service** | http://localhost:5000 | Emotion detection API |
| **Frontend** | http://localhost:5173 | React app |

---

## Environment Variables Checklist

### Backend/.env
- [ ] `EMOTION_SERVICE_URL=http://localhost:5000/detect`
- [ ] `MONGODB_URI=mongodb://localhost:27017` (or Atlas URL)
- [ ] `API_BASE_URL=http://localhost:8000`
- [ ] `PORT=8000`
- [ ] `DEBUG_MODE=true`
- [ ] `LOG_LEVEL=DEBUG`

### emotion_recognition/.env
- [ ] `FLASK_ENV=development`
- [ ] `FLASK_DEBUG=1`
- [ ] `PORT=5000`

### raga-rasa-soul-final-v2/.env.local
- [ ] `VITE_API_URL=http://127.0.0.1:8000`
- [ ] `VITE_APP_NAME=RagaRasa Music Therapy`
- [ ] `VITE_ENV=development`

---

## Next Steps After Local Testing

Once all services are running locally and tested:

1. **Run Full Integration Tests** (if available)
   ```bash
   cd Backend
   python integration_test.py
   ```

2. **Check for Console Errors**
   - Open http://localhost:5173
   - Press F12 to open DevTools
   - Check Console tab for any errors
   - Check Network tab to verify API calls

3. **Test Complete User Flows**
   - User registration
   - Emotion detection
   - Song recommendations
   - Rating/feedback

4. **Prepare for Cloud Deployment**
   - Document any issues found
   - Update configuration for production
   - Prepare deployment environment variables

---

## Support & Debugging

### Enable Detailed Logging

Backend (`Backend/.env`):
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

Emotion Service (`emotion_recognition/.env`):
```env
FLASK_DEBUG=1
FLASK_ENV=development
```

### Check Logs

**Backend logs:** Check terminal where `python main.py` is running
**Emotion logs:** Check terminal where `python api.py` is running
**Frontend logs:** Check browser DevTools Console tab

---

## Summary

You now have:
- ✅ Backend API running on http://localhost:8000
- ✅ Emotion Service running on http://localhost:5000
- ✅ Frontend React app running on http://localhost:5173
- ✅ All services communicating with each other
- ✅ Ready for feature testing and bug fixes
- ✅ Ready for cloud deployment when confirmed working

Next: Verify everything works, then proceed to cloud deployment (Google Cloud Run + HF Spaces).
