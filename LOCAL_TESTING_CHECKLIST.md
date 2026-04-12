# Local Testing Checklist - RagaRasa Music Therapy

Use this checklist to verify all components work correctly in your local environment before deploying to the cloud.

---

## Pre-Testing Setup

- [ ] Read `LOCAL_DEVELOPMENT_GUIDE.md` completely
- [ ] Verified Python 3.9+ installed: `python --version`
- [ ] Verified Node.js 18+ installed: `node --version`
- [ ] Verified Git installed: `git --version`
- [ ] MongoDB available (local or Atlas connection string ready)
- [ ] All three service directories exist and accessible
- [ ] No processes running on ports 8000, 5000, 5173

---

## Phase 1: Backend Service Testing

### Step 1: Backend Virtual Environment
- [ ] Navigated to `Backend/` directory
- [ ] Created virtual environment: `python -m venv venv`
- [ ] Activated venv: `.\venv\Scripts\Activate.ps1` (PowerShell)
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] No errors during pip install

### Step 2: Backend Configuration
- [ ] Checked `.env` file exists
- [ ] `EMOTION_SERVICE_URL=http://localhost:5000/detect` (local service)
- [ ] `MONGODB_URI` set correctly (local or Atlas)
- [ ] `PORT=8000`
- [ ] `DEBUG_MODE=true`
- [ ] `LOG_LEVEL=DEBUG`

### Step 3: MongoDB Connection Test
- [ ] MongoDB is running (local or Atlas accessible)
- [ ] Can connect to MongoDB:
  ```python
  python
  >>> from pymongo import MongoClient
  >>> MongoClient('YOUR_CONNECTION_STRING').admin.command('ismaster')
  >>> # Should return: {'ok': 1, ...}
  ```

### Step 4: Start Backend Server
- [ ] Terminal showing `(venv)` prefix
- [ ] Ran: `python main.py`
- [ ] No errors in startup output
- [ ] Message shows: `Uvicorn running on http://127.0.0.1:8000`
- [ ] Can access http://localhost:8000/docs (Swagger UI loads)

### Step 5: Backend Health Check
- [ ] Opened http://localhost:8000/docs
- [ ] Swagger UI displays all endpoints
- [ ] Can see endpoints like `/api/health`, `/api/emotion`, `/api/songs`, etc.
- [ ] Try GET `/api/health` in Swagger - should return `{"status":"OK"}`

### Step 6: Backend Database Check
- [ ] Try GET `/api/songs` in Swagger
- [ ] Returns list of songs (may be empty if not seeded)
- [ ] No error responses
- [ ] Check terminal for any ERROR logs

**Status:** ✅ Backend working / ❌ Debug issues

---

## Phase 2: Emotion Recognition Service Testing

### Step 7: Emotion Service Virtual Environment
- [ ] Opened new terminal/PowerShell window
- [ ] Navigated to `emotion_recognition/` directory
- [ ] Created virtual environment: `python -m venv venv`
- [ ] Activated venv: `.\venv\Scripts\Activate.ps1`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] **NOTE:** This may take 5-10 minutes due to HSEmotion model download

### Step 8: Emotion Service Configuration
- [ ] `.env` file exists
- [ ] `FLASK_ENV=development`
- [ ] `FLASK_DEBUG=1`
- [ ] `PORT=5000`

### Step 9: Start Emotion Service
- [ ] Terminal showing `(venv)` prefix
- [ ] Ran: `python api.py`
- [ ] No errors in startup output
- [ ] Message shows: `Running on http://127.0.0.1:5000`

### Step 10: Emotion Service Health Check
- [ ] Opened http://localhost:5000/health in browser
- [ ] Returns: `{"status":"OK"}`
- [ ] Try http://localhost:5000/test
- [ ] Returns emotion detection results (emotion, confidence, probabilities)

### Step 11: Test Emotion Detection
- [ ] In Python terminal:
  ```python
  import requests
  response = requests.post('http://localhost:5000/detect', json={'text': 'I am so happy'})
  print(response.json())
  ```
- [ ] Returns emotion data with emotion label and confidence score
- [ ] No errors in emotion service terminal

**Status:** ✅ Emotion Service working / ❌ Debug issues

---

## Phase 3: Frontend Service Testing

### Step 12: Frontend Setup
- [ ] Opened new terminal/PowerShell window
- [ ] Navigated to `raga-rasa-soul-final-v2/` directory
- [ ] Ran: `npm install`
- [ ] No errors during npm install
- [ ] `node_modules/` directory created

### Step 13: Frontend Configuration
- [ ] `.env.local` file exists
- [ ] `VITE_API_URL=http://127.0.0.1:8000`
- [ ] `VITE_APP_NAME=RagaRasa Music Therapy`
- [ ] `VITE_ENV=development`

### Step 14: Start Frontend Development Server
- [ ] Terminal not showing errors
- [ ] Ran: `npm run dev`
- [ ] Output shows: `Local: http://localhost:5173/`
- [ ] "press h to show help" message visible

### Step 15: Frontend Loading Test
- [ ] Opened http://localhost:5173 in browser
- [ ] Page loads without blank/error screen
- [ ] RagaRasa logo/title visible
- [ ] No CORS errors in browser console (press F12)
- [ ] No network errors in Network tab

**Status:** ✅ Frontend working / ❌ Debug issues

---

## Phase 4: Full Stack Integration Testing

### Step 16: All Services Running
- [ ] Backend running on http://localhost:8000 (check terminal)
- [ ] Emotion Service running on http://localhost:5000 (check terminal)
- [ ] Frontend running on http://localhost:5173 (check terminal)
- [ ] All three terminals showing no error messages

### Step 17: API Connectivity Test
- [ ] Open http://localhost:5173
- [ ] Press F12 to open Developer Tools
- [ ] Go to Console tab
- [ ] Paste this test:
  ```javascript
  fetch('http://127.0.0.1:8000/api/health')
    .then(r => r.json())
    .then(d => console.log('✅ Backend:', d))
    .catch(e => console.error('❌ Backend Error:', e))
  ```
- [ ] Console shows: `✅ Backend: {status: "OK"}`
- [ ] No CORS errors in console

### Step 18: Emotion Service Connectivity Test
- [ ] In browser console:
  ```javascript
  fetch('http://127.0.0.1:5000/health')
    .then(r => r.json())
    .then(d => console.log('✅ Emotion:', d))
    .catch(e => console.error('❌ Emotion Error:', e))
  ```
- [ ] Console shows: `✅ Emotion: {status: "OK"}`
- [ ] No errors

### Step 19: Check Network Requests
- [ ] Keep Developer Tools open (F12)
- [ ] Go to Network tab
- [ ] Reload page (Ctrl+R)
- [ ] Check requests made during page load:
  - [ ] Should see requests to http://127.0.0.1:8000 (backend)
  - [ ] Status codes should be 2xx (success) or 304 (cached)
  - [ ] No 4xx or 5xx errors
  - [ ] No failed network requests

### Step 20: Test Emotion Detection Flow (if UI supports it)
- [ ] Navigate to emotion detection section in app
- [ ] Input some text (e.g., "I am very happy")
- [ ] Click detect/submit button
- [ ] Check Network tab for POST request to `/api/emotion`
- [ ] Response shows emotion and confidence
- [ ] UI displays the result correctly
- [ ] No console errors

### Step 21: Test Recommendation Flow (if UI supports it)
- [ ] Navigate to recommendations section
- [ ] Trigger recommendation generation (if available)
- [ ] Check Network tab for requests to `/api/recommendations`
- [ ] UI displays recommended songs
- [ ] No console errors

### Step 22: Test Songs/Catalog (if available)
- [ ] Navigate to songs/catalog section
- [ ] Check Network tab for requests to `/api/songs`
- [ ] Songs display in UI
- [ ] No console errors

**Status:** ✅ All systems integrated / ❌ Debug issues

---

## Phase 5: Error Handling & Edge Cases

### Step 23: Test Backend Error Handling
- [ ] Try invalid endpoint: http://localhost:8000/api/invalid
- [ ] Should return 404 error (not crash)
- [ ] Try POST to `/api/emotion` with empty body
- [ ] Should return validation error (not crash)
- [ ] No "Internal Server Error 500" in responses

### Step 24: Test Emotion Service Fallback
- [ ] Stop Emotion Service (Ctrl+C in its terminal)
- [ ] Try emotion detection in app
- [ ] Either:
  - [ ] Shows error message to user (graceful), OR
  - [ ] Falls back to default emotion
  - [ ] Does NOT crash the app
- [ ] Restart Emotion Service

### Step 25: Test Database Connection Loss
- [ ] Query works: http://localhost:8000/api/songs (should work)
- [ ] If MongoDB is down:
  - [ ] API shows timeout error
  - [ ] Does NOT crash
  - [ ] Restart MongoDB

### Step 26: Console Warnings Check
- [ ] Open http://localhost:5173
- [ ] Press F12 → Console tab
- [ ] Check for any warnings (yellow triangle icons):
  - [ ] Deprecation warnings OK (just log)
  - [ ] CORS errors = FAIL (needs investigation)
  - [ ] Missing API keys = FAIL (needs setup)
  - [ ] Any "Cannot read property" errors = FAIL (needs debugging)

**Status:** ✅ Error handling works / ❌ Issues found

---

## Phase 6: Performance & Logging

### Step 27: Check Response Times
- [ ] Open Developer Tools Network tab
- [ ] Reload http://localhost:5173
- [ ] Check request times:
  - [ ] API health check: < 100ms
  - [ ] Songs list: < 500ms
  - [ ] Emotion detection: < 2000ms (emotion model inference)
  - [ ] Recommendations: < 1000ms

### Step 28: Monitor Logs
- [ ] **Backend terminal:** Check for any ERROR or WARNING logs
- [ ] **Emotion Service terminal:** Check for any errors during emotion detection
- [ ] **Browser console:** Check for any runtime errors
- [ ] **All logs are informational (INFO level):** ✅

### Step 29: Memory Usage
- [ ] Open Task Manager (Ctrl+Shift+Esc)
- [ ] Check resource usage:
  - [ ] Python (Backend + Emotion): < 500MB total
  - [ ] Node (Frontend): < 300MB
  - [ ] System remains responsive
  - [ ] No memory leaks (usage stays constant)

**Status:** ✅ Performance acceptable / ❌ Optimize needed

---

## Phase 7: Pre-Deployment Verification

### Step 30: Configuration Review
- [ ] All `.env` files have been checked
- [ ] No hardcoded secrets in code
- [ ] Database connection works reliably
- [ ] API URLs are correct for local development
- [ ] CORS is not causing issues

### Step 31: Data Persistence
- [ ] Add test data in app (if possible)
- [ ] Restart Backend service
- [ ] Data is still there ✅
- [ ] No data loss on restart

### Step 32: Service Restart Test
- [ ] Stop Backend service (Ctrl+C)
- [ ] Frontend still loads (cached)
- [ ] Restart Backend
- [ ] Frontend reconnects automatically
- [ ] API calls work again

### Step 33: Browser Compatibility
- [ ] Test in Chrome/Edge: ✅ Works
- [ ] Test in Firefox: ✅ Works
- [ ] Test in Safari (if available): ✅ Works
- [ ] Mobile browser (DevTools device mode): ✅ Responsive

### Step 34: Documentation Review
- [ ] `LOCAL_DEVELOPMENT_GUIDE.md` covers your setup: ✅
- [ ] All steps matched your experience
- [ ] No missing instructions
- [ ] Troubleshooting section was helpful (or not needed)

**Status:** ✅ Ready for deployment / ❌ Issues to fix

---

## Common Issues & Quick Fixes

### Issue: Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Or change port in .env
PORT=8001
```

### Issue: CORS Error
```
Access to XMLHttpRequest at 'http://localhost:8000/...' from origin 'http://localhost:5173' has been blocked
```

**Fix:**
1. Check Backend `.env` has correct CORS settings
2. Ensure Backend is running
3. Clear browser cache (Ctrl+Shift+Delete)
4. Hard refresh (Ctrl+Shift+R)

### Issue: "Cannot connect to MongoDB"
```
Error: MongoServerSelectionError: connect ECONNREFUSED 127.0.0.1:27017
```

**Fix:**
1. If using local MongoDB: `mongod` command to start
2. If using Atlas: Check connection string in `.env`
3. Verify IP whitelist in Atlas (should include 0.0.0.0/0 for local dev)

### Issue: Emotion Service Timeout
```
Error: Connection timeout when calling emotion service
```

**Fix:**
1. Check Emotion Service is running
2. Wait 1-2 minutes for model to download first time
3. Check `EMOTION_SERVICE_URL` in Backend `.env`
4. Check port 5000 is not blocked by firewall

### Issue: Frontend Won't Connect to Backend
```
Failed to fetch from http://127.0.0.1:8000
```

**Fix:**
1. Check `VITE_API_URL` in Frontend `.env.local`
2. Check Backend is running on port 8000
3. Try accessing http://localhost:8000/docs directly
4. Check Windows Firewall settings

---

## Testing Sign-Off

Once all checkboxes above are marked as ✅, you're ready for cloud deployment!

**Date Tested:** _______________

**Tested By:** _______________

**All Systems Operational:** ☐ YES ☐ NO

**Issues Found:** 
```
(List any issues found)
```

**Next Steps:**
- [ ] All issues resolved
- [ ] Push changes to GitHub
- [ ] Deploy Backend to Google Cloud Run
- [ ] Deploy Emotion Service to HF Spaces
- [ ] Update Frontend with production URLs

---

## Notes

Write any observations, issues, or suggestions here:

```
(Your notes here)
```
