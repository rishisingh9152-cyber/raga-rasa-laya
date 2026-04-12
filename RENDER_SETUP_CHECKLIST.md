# Quick Reference: Render Service Creation Checklist

## Before Starting
- [ ] Log in to https://dashboard.render.com
- [ ] Have GitHub login ready
- [ ] Copy these values:
  - MONGODB_URI: `mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject`
  - EMOTION_SERVICE_URL: `https://raga-rasa-music.onrender.com/detect`

## Delete Old Service
- [ ] Go to Render dashboard
- [ ] Find `raga-rasa-backend` service
- [ ] Scroll to "Danger Zone"
- [ ] Click "Delete Service"
- [ ] Confirm deletion

## Create New Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub: `rishisingh9152-cyber/raga-rasa-laya`
- [ ] Select branch: `main`

## Configuration
- [ ] Name: `raga-rasa-backend`
- [ ] Runtime: Python 3
- [ ] Build: `pip install -r Backend/requirements.txt`
- [ ] Start: `cd Backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
- [ ] Region: Your closest region
- [ ] Plan: Free

## Environment Variables (Add These)
- [ ] MONGODB_URI = `mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject`
- [ ] EMOTION_SERVICE_URL = `https://raga-rasa-music.onrender.com/detect`
- [ ] PORT = `8000`

## Python Version
- [ ] Look for Python version dropdown
- [ ] If found: Select **3.10**
- [ ] If not found: OK - runtime.txt and .python-version will handle it

## Create & Monitor
- [ ] Click "Create Web Service"
- [ ] Watch logs appear
- [ ] Look for: "Installing python-3.10..." (NOT 3.14)
- [ ] Wait for status: **Live** (green)

## Test Endpoints
- [ ] Test: `https://raga-rasa-backend.onrender.com/health`
- [ ] Expected: `{"status":"ok",...}`
- [ ] Test: `https://raga-rasa-backend.onrender.com/recommendations?emotion=happy`
- [ ] Expected: `{"status":"success","recommendations":[...]}`
- [ ] Verify: URLs in recommendations start with `https://res.cloudinary.com/`

## Update Vercel
- [ ] Go to https://vercel.com
- [ ] Open `raga-rasa-music-52` project
- [ ] Settings → Environment Variables
- [ ] Set: `REACT_APP_API_URL = https://raga-rasa-backend.onrender.com`
- [ ] Redeploy

## Final Test
- [ ] Open: https://raga-rasa-music-52.vercel.app
- [ ] Check console (F12): No JSON errors
- [ ] Click "Detect Emotion 🎯"
- [ ] Recommendations should load
- [ ] Player should appear with Cloudinary URLs
- [ ] Audio should play ✅

## If Issues
| Problem | Action |
|---------|--------|
| Build fails | Check Backend/requirements.txt |
| Python 3.14 in logs | Rebuild service or check runtime.txt |
| No recommendations | Check MONGODB_URI in env vars |
| JSON parse error | Check API is returning JSON (not HTML) |
| No audio | Check Cloudinary URLs in response |

---

**Status: Ready to Create New Service** ✅
