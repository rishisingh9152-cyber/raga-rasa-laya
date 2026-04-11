# 🚀 STEP-BY-STEP: Deploy raga-rasa-backend on Render

## CURRENT PROBLEM
- Render is using Python 3.14 (not honoring runtime.txt)
- Render is trying to build old dependencies (Pillow 10.1.0, TensorFlow, etc.)
- Build fails because Python 3.14 incompatibility

## SOLUTION
Delete the broken service and create a new one with CORRECT settings.

---

## 🔴 STEP 1: DELETE Old Service

1. Go to: https://dashboard.render.com
2. Click on **raga-rasa-backend** service
3. Scroll down → Click **"Delete Service"**
4. Type the service name to confirm deletion
5. Click **Delete**

Wait a few seconds for it to disappear.

---

## 🟢 STEP 2: CREATE New Service (CORRECT WAY)

### 2.1: Create the Service
1. Go to: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect"** next to `raga-rasa-laya` repository
4. You should see the repo connect

### 2.2: Configure Service

Fill in EXACTLY these values:

```
Name: raga-rasa-backend
Environment: Python 3
Region: Ohio
Branch: main
Root Directory: (LEAVE BLANK - THIS IS CRITICAL!)
Build Command: pip install -r Backend/requirements.txt
Start Command: cd Backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Plan: Free
```

**IMPORTANT:** The Root Directory field must be EMPTY/BLANK.

### 2.3: Add Environment Variables

Click **"Advanced"** and add these EXACTLY:

| Key | Value |
|-----|-------|
| MONGODB_URI | mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject |
| EMOTION_SERVICE_URL | https://emotion-recognition-lr88.onrender.com |
| PORT | 8000 |
| JWT_SECRET | dt_aRvdBIakTz2GI_qC4U1EqVVgmq4nrRDSc5XX73iY |

### 2.4: Deploy Settings (Optional)
- Auto-Deploy: ON (auto-redeploy on git push)
- Health Check Path: /health
- Notification Email: (your email)

### 2.5: Create Service
Click **"Create Web Service"** button.

Wait 5-10 minutes for deployment.

---

## 🧪 STEP 3: VERIFY Deployment

Once deployment completes:

### 3.1: Check Logs
1. Click on the service name
2. Check the **Logs** tab at the bottom
3. Look for any error messages
4. Should see: `✅ Uvicorn running on 0.0.0.0:8000`

### 3.2: Test Health Endpoint
```bash
# Get your service URL from Render dashboard (usually looks like):
# https://raga-rasa-backend-XXXX.onrender.com

# Test it:
curl https://raga-rasa-backend-XXXX.onrender.com/health

# Should return:
# {"status":"ok","service":"Raga-Rasa Soul API","version":"2.0.0"}
```

### 3.3: Test Emotion Service Integration
```bash
curl https://raga-rasa-backend-XXXX.onrender.com/
# Should return API info
```

---

## 📋 What Changed

✅ **Backend/requirements.txt** - Simplified to only essential packages:
- fastapi
- uvicorn
- pydantic
- pymongo
- email-validator
- python-multipart
- requests

❌ **REMOVED** (causing Python 3.14 incompatibility):
- tensorflow
- torch/torchvision/torchaudio
- h5py
- scikit-learn
- librosa
- opencv-python (heavy)

**Note:** If you need these packages, we'll add them back after verifying the base service works.

---

## 🎯 Summary

1. **Delete** the broken raga-rasa-backend service
2. **Create** a NEW service with the config above
3. **Test** the health endpoint
4. **Report** any errors from the logs

**Key Points:**
- ✅ Root Directory: BLANK (no value)
- ✅ Branch: main
- ✅ All 4 environment variables set
- ✅ Python will default to 3.11+ (compatible with our packages)

---

**Repository:** https://github.com/rishisingh9152-cyber/raga-rasa-laya
**Latest Commit:** e5f88f7c (simplified requirements)
**Status:** Ready to deploy

