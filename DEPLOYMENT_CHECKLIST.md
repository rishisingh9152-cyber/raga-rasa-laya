# ✅ QUICK DEPLOYMENT CHECKLIST

## 📋 For Emotion Recognition Service (emotion-recognition-lr88.onrender.com)

If this service is failing or needs redeployment:

1. ☐ Go to Render Dashboard → emotion-recognition service
2. ☐ Settings → Logs (check what error is showing)
3. ☐ Settings → Build & Deploy
4. ☐ Verify Build Command: `pip install -r emotion_recognition/requirements.txt`
5. ☐ Verify Start Command: `cd emotion_recognition && python api.py`
6. ☐ Verify Root Directory: (should be blank/empty)
7. ☐ Click "Manual Deploy" → Select branch `main`
8. ☐ Wait 3-5 minutes for build
9. ☐ Test: `curl https://emotion-recognition-lr88.onrender.com/`

---

## 📋 For Backend Service (raga-rasa-backend - CREATE NEW)

**IMPORTANT: You deleted the old one, so we're creating a fresh service**

### Step 1: Create Service
1. ☐ Go to https://dashboard.render.com
2. ☐ Click **"New +" → "Web Service"**
3. ☐ Click **"Connect"** next to your GitHub repo: `raga-rasa-laya`
4. ☐ Fill in these fields:

| Field | Value |
|-------|-------|
| Name | `raga-rasa-backend` |
| Environment | `Python 3` |
| Region | `Ohio` |
| Branch | `main` |
| Root Directory | (leave empty) |
| Build Command | `pip install -r Backend/requirements.txt` |
| Start Command | `cd Backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| Plan | `Free` |

### Step 2: Add Environment Variables (CRITICAL!)
1. ☐ Click **"Advanced"**
2. ☐ Add these 4 environment variables:

```
MONGODB_URI=mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject

EMOTION_SERVICE_URL=https://emotion-recognition-lr88.onrender.com

PORT=8000

JWT_SECRET=dt_aRvdBIakTz2GI_qC4U1EqVVgmq4nrRDSc5XX73iY
```

### Step 3: Create Service
1. ☐ Click **"Create Web Service"** button
2. ☐ Wait for automatic deployment (5-10 minutes)

### Step 4: Verify
1. ☐ Check Logs in Render dashboard
2. ☐ If build succeeds, test: `curl https://raga-rasa-backend-XXXX.onrender.com/health`
3. ☐ Should return: `{"status":"ok","service":"Raga-Rasa Soul API","version":"2.0.0"}`

---

## 🧪 Final Integration Test

Once both services are deployed:

```bash
# Test 1: Emotion service responds
curl https://emotion-recognition-lr88.onrender.com/

# Test 2: Backend health check
curl https://raga-rasa-backend-XXXX.onrender.com/health

# Test 3: Backend can reach emotion service
curl -X POST https://raga-rasa-backend-XXXX.onrender.com/emotion/live
```

---

## 📝 Notes

- ✅ All code is committed and pushed to `main` branch
- ✅ Both services have runtime.txt (forcing Python 3.10.15)
- ✅ Both services have Procfile (correct start commands)
- ✅ Backend uses environment variables for MongoDB & Emotion service URLs
- ✅ Deployment guide in RENDER_DEPLOYMENT_GUIDE.md

---

**Need to debug?** Check Render Dashboard Logs for exact error messages!

