# 🚀 Backend Deployment Instructions (Updated)

## Current Status
- ✅ **Emotion Service**: Deployed at https://raga-rasa-music.onrender.com
- ⏳ **Backend Service**: Ready to deploy

## Environment Variables Needed
When creating the backend service on Render, add these environment variables:

```
MONGODB_URI=mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject
EMOTION_SERVICE_URL=https://raga-rasa-music.onrender.com
JWT_SECRET=dt_aRvdBIakTz2GI_qC4U1EqVVgmq4nrRDSc5XX73iY
PORT=8000
```

## Backend Configuration Files
All files are ready in the repo:

**Backend/Procfile:**
```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Backend/runtime.txt:**
```
python-3.10.15
```

**Backend/requirements.txt:** (7 minimal dependencies)
```
fastapi==0.110.1
uvicorn[standard]==0.27.0
pydantic==2.7.1
pymongo==4.7.0
email-validator==2.1.0
python-multipart==0.0.6
requests==2.31.0
```

## Deployment Steps on Render

### Step 1: Delete Old Service (if exists)
- Go to Render Dashboard
- Find `raga-rasa-backend` service
- Click Settings → Delete Service

### Step 2: Create New Service
1. Click **New +** → **Web Service**
2. Select **Connect a repository** → Choose `raga-rasa-laya`
3. Set these values exactly:
   - **Name**: `raga-rasa-backend`
   - **Environment**: Python 3
   - **Region**: Ohio (or closest)
   - **Branch**: `main`
   - **Root Directory**: (LEAVE EMPTY)
   - **Build Command**: `pip install -r Backend/requirements.txt`
   - **Start Command**: `cd Backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Plan**: Free

### Step 3: Add Environment Variables
In the "Advanced" section, add 4 environment variables:
1. `MONGODB_URI` = `mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject`
2. `EMOTION_SERVICE_URL` = `https://raga-rasa-music.onrender.com`
3. `JWT_SECRET` = `dt_aRvdBIakTz2GI_qC4U1EqVVgmq4nrRDSc5XX73iY`
4. `PORT` = `8000`

### Step 4: Deploy
Click "Create Web Service" and wait 3-5 minutes for deployment.

## Testing

Once deployed, test these endpoints:

```bash
# Replace XXXX with your actual service ID from Render
BASE_URL=https://raga-rasa-backend-XXXX.onrender.com

# Test 1: Health check
curl $BASE_URL/health

# Test 2: Root endpoint
curl $BASE_URL/

# Test 3: Test endpoint
curl $BASE_URL/test
```

Expected responses:
- `/health` → `{"status": "ok", "service": "Raga-Rasa Soul API", "version": "1.0.0"}`
- `/` → `{"message": "Raga-Rasa Soul API is running", "status": "ok"}`
- `/test` → `{"test": "success"}`

## Important Notes

⚠️ **CRITICAL:**
1. **Root Directory MUST BE EMPTY** - Don't put "Backend" in this field!
2. Keep Start Command as shown (includes `cd Backend &&`)
3. Use exact environment variable values (copy-paste to avoid typos)
4. Wait full 3-5 minutes even if it seems stuck
5. The service URL will be shown in your Render dashboard

## Latest Changes
- ✅ Fixed emotion_client.py to use `EMOTION_SERVICE_URL` env var
- ✅ Committed and pushed to main branch
- ✅ Ready for deployment!

