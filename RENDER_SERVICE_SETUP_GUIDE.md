# 🚀 Create New Render Backend Service - Step-by-Step Guide

## Prerequisites
- ✅ Render account: https://dashboard.render.com
- ✅ GitHub account with access to: https://github.com/rishisingh9152-cyber/raga-rasa-laya
- ✅ MongoDB URI: `mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject`
- ✅ Emotion Service URL: `https://raga-rasa-music.onrender.com/detect`

---

## Phase 1: Delete Old Service (5 minutes)

### Step 1.1: Go to Render Dashboard
1. Open: https://dashboard.render.com
2. Log in if needed
3. You should see your services list

### Step 1.2: Find Old Backend Service
1. Look for service named: **`raga-rasa-backend`**
2. Click on it to open details

### Step 1.3: Delete Service
1. Scroll down to the bottom of the page
2. Look for **"Danger Zone"** section (red area)
3. Click **"Delete Service"**
4. Confirm the deletion (may need to type service name)
5. Wait for it to be removed (usually instant)

**Expected Result**: Service disappears from dashboard

---

## Phase 2: Create New Service (10 minutes)

### Step 2.1: Start Creating New Service
1. In Render dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**

### Step 2.2: Connect GitHub Repository
1. Under "Connect a repository", click **"Connect"**
2. Search for and select: **`rishisingh9152-cyber/raga-rasa-laya`**
3. Confirm connection
4. Select branch: **`main`**

### Step 2.3: Configure Service Settings

Fill in these fields exactly:

| Field | Value |
|-------|-------|
| **Name** | `raga-rasa-backend` |
| **Region** | *Your closest region (e.g., Oregon, Virginia)* |
| **Branch** | `main` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r Backend/requirements.txt` |
| **Start Command** | `cd Backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| **Plan** | Free (or Starter if you want paid) |

### Step 2.4: Set Environment Variables

Click **"Add Environment Variable"** for each:

**Variable 1: MONGODB_URI**
```
Key: MONGODB_URI
Value: mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject
```

**Variable 2: EMOTION_SERVICE_URL**
```
Key: EMOTION_SERVICE_URL
Value: https://raga-rasa-music.onrender.com/detect
```

**Variable 3: PORT**
```
Key: PORT
Value: 8000
```

### Step 2.5: Look for Python Version Selection

**IMPORTANT**: Look for a Python version selector dropdown
- If you see it, select: **`3.10`** or **`3.10.15`**
- If you don't see it, that's OK - we have runtime.txt and .python-version files that will handle it

### Step 2.6: Create Service

Click **"Create Web Service"** button

**Expected Result**: Render starts building your service

---

## Phase 3: Wait & Monitor Build (5-15 minutes)

### Step 3.1: Watch the Logs
1. You'll see a logs section show up
2. Watch for these stages:
   - `Building...` → Downloading dependencies
   - `Installing Python 3.10...` → ✅ Good sign (NOT 3.14!)
   - `Running build command...` → Installing requirements
   - `Starting service...` → Service starting
   - `Live` → ✅ Service is running!

### Step 3.2: Look for Python Version Confirmation

In the logs, you should see text like:
```
Installing python-3.10.15
```

**If you see 3.14**, something went wrong. Check:
- Did you see Python 3.10 in the logs?
- Is the service status "Live" or "Failed"?

### Step 3.3: Wait for "Live" Status

Don't proceed until you see:
- Service status: **"Live"** (green)
- URL generated: `https://raga-rasa-backend.onrender.com` (or similar)

---

## Phase 4: Verify Deployment Works (5 minutes)

### Step 4.1: Test Health Endpoint

Open in browser or curl:
```
https://raga-rasa-backend.onrender.com/health
```

**Expected Response**:
```json
{
  "status": "ok",
  "service": "Raga-Rasa Soul API",
  "version": "1.0.0"
}
```

### Step 4.2: Test Recommendations Endpoint

Open in browser:
```
https://raga-rasa-backend.onrender.com/recommendations?emotion=happy
```

**Expected Response**:
```json
{
  "status": "success",
  "user_id": "default_user",
  "emotion": "happy",
  "count": 5,
  "recommendations": [
    {
      "song_name": "...",
      "rass": "shringar",
      "streaming_url": "https://res.cloudinary.com/...",
      ...
    }
  ]
}
```

**If you get HTML error page instead of JSON**:
- Service is returning HTML (error)
- Check logs for the actual error
- Common issues:
  - Missing environment variables
  - Python version mismatch
  - MongoDB connection failed

### Step 4.3: Verify Cloudinary URLs

In the response, check that streaming_url:
- Starts with: `https://res.cloudinary.com/dlx3ufj3t/`
- NOT a local file path

**Good URL**: `https://res.cloudinary.com/dlx3ufj3t/video/upload/v.../raga-rasa/...`
**Bad URL**: `http://127.0.0.1:8000/songs/...` or `C:\Users\...`

---

## Phase 5: Update Vercel Environment (5 minutes)

### Step 5.1: Go to Vercel

1. Open: https://vercel.com
2. Log in if needed
3. Go to Projects
4. Find: **`raga-rasa-music-52`** (or your frontend project)

### Step 5.2: Update Environment Variables

1. Click on the project
2. Go to **Settings** → **Environment Variables**
3. Find or create: `REACT_APP_API_URL`
4. Set value to: `https://raga-rasa-backend.onrender.com`
5. Save

### Step 5.3: Redeploy Frontend

1. Go back to **Deployments**
2. Click the **three dots** on the latest deployment
3. Select **"Redeploy"**
4. Confirm

**Wait for Vercel to redeploy (usually 2-3 minutes)**

---

## Phase 6: Test End-to-End (5 minutes)

### Step 6.1: Test Frontend

1. Open: https://raga-rasa-music-52.vercel.app
2. Click **"Detect Emotion 🎯"** button
3. Wait for recommendations to load
4. Check browser console for errors (F12 → Console)

### Step 6.2: Check Logs

In browser console, you should see:
```
🌍 API Base URL: https://raga-rasa-backend.onrender.com
📡 Fetching recommendations from: https://raga-rasa-backend.onrender.com/recommendations?emotion=happy
✅ Recommendations received: (...)
```

### Step 6.3: Verify Player Works

1. If recommendations loaded, a player should appear
2. Check that it shows a Cloudinary URL (not local path)
3. Try clicking play - audio should stream from Cloudinary

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Build fails immediately** | Check Backend/requirements.txt exists and is valid |
| **Python 3.14 installed** | Check logs, should show 3.10. If not, service may need rebuild |
| **Service says "Failed"** | Click service, scroll to Logs tab, look for error message |
| **Timeout when testing endpoint** | Service still building, wait 5-10 more minutes |
| **JSON parse error on frontend** | Backend returning HTML error page, check Render logs |
| **No Cloudinary URLs in response** | MongoDB not updated, check `streaming_url` field exists |
| **Audio won't play** | Browser blocked CORS or Cloudinary URL invalid |

---

## Success Checklist

- [ ] Old service deleted from Render
- [ ] New service created and building
- [ ] Logs show "Python 3.10" (not 3.14)
- [ ] Service status shows "Live" (green)
- [ ] `/health` endpoint returns JSON
- [ ] `/recommendations?emotion=happy` returns valid recommendations
- [ ] URLs in recommendations are Cloudinary links (https://res.cloudinary.com/...)
- [ ] Vercel environment variable updated
- [ ] Frontend redeployed on Vercel
- [ ] Frontend loads without JSON errors
- [ ] Player appears with song recommendations
- [ ] Audio plays from Cloudinary

---

## Need Help?

If you get stuck:
1. **Check Render logs** (most problems shown there)
2. **Check browser console** on Vercel (F12 → Console)
3. **Verify environment variables** are set correctly
4. **Check MongoDB connection** (is MONGODB_URI correct?)
5. **Verify Cloudinary setup** (songs in MongoDB have streaming_url?)

---

**Ready to create the new service? Follow the steps above!** 🚀
