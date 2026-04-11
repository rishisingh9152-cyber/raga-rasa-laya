# 🚀 Complete Render Deployment Guide - Both Services

## Service 1: Emotion Recognition Service

### Current Status
- ✅ Repository: https://github.com/rishisingh9152-cyber/raga-rasa-laya
- ✅ Branch: main
- ✅ Directory: emotion_recognition/
- ✅ URL: https://emotion-recognition-lr88.onrender.com

### Files in Place
```
emotion_recognition/
├── api.py                 ✅ Flask app with /health and /detect endpoints
├── emotion_detector.py    ✅ HSEmotion model integration
├── requirements.txt       ✅ All dependencies
├── Procfile              ✅ web: python api.py
└── runtime.txt           ✅ python-3.10.15
```

### Render Configuration
1. Go to: https://dashboard.render.com → emotion-recognition service
2. Click **Settings** → **Build & Deploy**
3. Set these values:

| Field | Value |
|-------|-------|
| Name | emotion-recognition |
| Environment | Python 3 |
| Branch | main |
| Root Directory | (leave blank) |
| Build Command | pip install -r emotion_recognition/requirements.txt |
| Start Command | cd emotion_recognition && python api.py |
| Plan | Free |

4. Click **Save**
5. Click **Manual Deploy** → Select branch `main`

### Test Endpoint
```bash
curl https://emotion-recognition-lr88.onrender.com/
# Should return service info
```

---

## Service 2: Backend API (raga-rasa-backend)

### Current Status
- ✅ Repository: https://github.com/rishisingh9152-cyber/raga-rasa-laya
- ✅ Branch: main
- ✅ Framework: FastAPI + MongoDB
- ✅ Language: Python 3.10.15

### Files in Place
```
Backend/
├── main.py               ✅ (in app/ subdirectory)
├── app/
│   ├── main.py          ✅ FastAPI app with all routes
│   ├── database.py       ✅ Uses MONGODB_URI env var
│   ├── routes/           ✅ All API endpoints
│   └── services/
│       └── emotion_client.py  ✅ Uses EMOTION_SERVICE_URL env var
├── requirements.txt      ✅ All dependencies (fastapi, pymongo, etc.)
├── Procfile             ✅ Start command configured
└── runtime.txt          ✅ python-3.10.15
```

### Render Configuration for raga-rasa-backend

#### Step 1: Create New Service
1. Go to: https://dashboard.render.com
2. Click **"New +" → "Web Service"**
3. Connect GitHub repository: `raga-rasa-laya`
4. Choose branch: `main`

#### Step 2: Basic Settings

| Field | Value |
|-------|-------|
| Name | raga-rasa-backend |
| Environment | Python 3 |
| Region | Ohio (or closest to you) |
| Branch | main |
| Root Directory | (leave blank) |
| Build Command | pip install -r Backend/requirements.txt |
| Start Command | cd Backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 |
| Plan | Free |

#### Step 3: Environment Variables (REQUIRED!)
Click **"Advanced"** and add these variables:

```
MONGODB_URI=mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject
EMOTION_SERVICE_URL=https://emotion-recognition-lr88.onrender.com
PORT=8000
JWT_SECRET=dt_aRvdBIakTz2GI_qC4U1EqVVgmq4nrRDSc5XX73iY
```

**COPY-PASTE READY:**
| Key | Value |
|-----|-------|
| MONGODB_URI | mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject |
| EMOTION_SERVICE_URL | https://emotion-recognition-lr88.onrender.com |
| PORT | 8000 |
| JWT_SECRET | dt_aRvdBIakTz2GI_qC4U1EqVVgmq4nrRDSc5XX73iY |

#### Step 4: Deploy Settings
- Auto-Deploy: **ON** (auto-redeploy on git push)
- Health Check Path: `/health` (optional)
- Notification Email: Your email

#### Step 5: Create Service
Click **"Create Web Service"** button

---

## 🧪 Testing Both Services

### Test 1: Emotion Recognition Service
```bash
curl https://emotion-recognition-lr88.onrender.com/
# Should return service info with model details
```

### Test 2: Backend Health Check
```bash
curl https://raga-rasa-backend-XXXX.onrender.com/health
# Should return:
# {"status":"ok","service":"Raga-Rasa Soul API","version":"2.0.0"}
```

### Test 3: Backend → Emotion Service Integration
```bash
# Backend calls emotion service internally
curl -X POST https://raga-rasa-backend-XXXX.onrender.com/emotion/live
```

---

## 🔗 Service Connection Flow

```
User Browser
    ↓
Raga-Rasa Backend (FastAPI)
    ↓
Emotion Recognition Service (Flask)  ← For emotion detection
    ↓
MongoDB Atlas Database
```

---

## 📋 Key Configuration Files Committed

| File | Purpose | Status |
|------|---------|--------|
| emotion_recognition/Procfile | Set start command | ✅ Committed |
| emotion_recognition/runtime.txt | Force Python 3.10.15 | ✅ Committed |
| emotion_recognition/requirements.txt | Dependencies | ✅ Committed |
| Backend/Procfile | Set start command | ✅ Committed |
| Backend/runtime.txt | Force Python 3.10.15 | ✅ Committed |
| Backend/requirements.txt | Dependencies | ✅ Committed |
| Backend/app/database.py | Uses MONGODB_URI env var | ✅ Committed |
| Backend/app/services/emotion_client.py | Uses EMOTION_SERVICE_URL env var | ✅ Committed |
| render.yaml | Auto-config for both services | ✅ Committed |

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Pillow build failed"
**Cause:** Python 3.14 doesn't support old Pillow versions
**Solution:** ✅ FIXED - Added Backend/runtime.txt with Python 3.10.15

### Issue 2: "gunicorn: command not found"
**Cause:** Missing Procfile or wrong start command
**Solution:** ✅ FIXED - Created Procfile with correct commands

### Issue 3: "MONGODB_URI not found"
**Cause:** Environment variables not set in Render
**Solution:** ✅ Add environment variables in Render dashboard (see above)

### Issue 4: "Connection refused to emotion service"
**Cause:** EMOTION_SERVICE_URL not set or wrong URL
**Solution:** ✅ Check environment variable is set to: https://emotion-recognition-lr88.onrender.com

---

## 🚀 Deployment Timeline

1. **Emotion Recognition**: Already deployed ✅
2. **Backend Service**: Deploy new service (create fresh)
3. **Set Environment Variables**: CRITICAL!
4. **Manual Deploy**: Both services should auto-deploy
5. **Test Health Endpoints**: Verify both running
6. **Integration Test**: Test emotion detection

---

## 📞 Need Help?

If deployment fails:
1. Check **Logs** in Render dashboard
2. Verify **Build Command** is correct
3. Verify **Start Command** uses correct paths
4. Verify **Environment Variables** are ALL set
5. Check **Python Version**: Should be 3.10.15 (not 3.14)

---

**Repository:** https://github.com/rishisingh9152-cyber/raga-rasa-laya
**Last Commit:** 6a5769da
**Status:** ✅ Ready for deployment

