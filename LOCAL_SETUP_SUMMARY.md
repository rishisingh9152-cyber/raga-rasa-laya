# Local Development Setup - Complete Summary

**Purpose:** Host and test the complete RagaRasa Music Therapy stack locally before cloud deployment.

**Status:** ✅ READY FOR LOCAL TESTING

---

## What Was Created

I've created a complete local development environment setup with comprehensive documentation.

### 📋 Documentation Files Created

1. **LOCAL_DEVELOPMENT_GUIDE.md** (🌟 START HERE)
   - Complete step-by-step setup instructions
   - 4 phases: Backend, Emotion Service, Frontend, Full-Stack Testing
   - Troubleshooting section for common issues
   - Environment variable checklist
   - ~400 lines of detailed guidance

2. **LOCAL_TESTING_CHECKLIST.md** (✅ USE AFTER SETUP)
   - 34-point verification checklist
   - Tests for each service independently
   - Full-stack integration tests
   - Error handling and edge case tests
   - Performance monitoring checks
   - Sign-off section for completion

3. **LOCAL_SETUP_SUMMARY.md** (THIS FILE)
   - Quick reference of what was done
   - Quick start options
   - Directory structure
   - Services overview
   - Next steps

### 🐳 Docker Support (Optional)

4. **docker-compose.yml**
   - Full stack in Docker containers
   - MongoDB, Backend, Emotion Service, Frontend
   - Pre-configured networking and health checks
   - Use if: You prefer Docker to native Python/Node

5. **Dockerfile.dev Files**
   - `Backend/Dockerfile.dev` - FastAPI service
   - `emotion_recognition/Dockerfile.dev` - Flask emotion service
   - `raga-rasa-soul-final-v2/Dockerfile.dev` - React frontend

### 🚀 Quick Start Scripts

6. **start_local_dev.bat** (Windows CMD)
   - Batch script to start all services
   - Opens 3 terminal windows
   - Automatic configuration checks

7. **start_local_dev.ps1** (Windows PowerShell)
   - PowerShell version of startup script
   - Better error handling
   - Color-coded output

---

## Quick Start Options

### Option A: Manual Setup (Recommended for Learning)

**Best for:** Understanding each component, debugging issues, learning the stack

```bash
# Terminal 1: Backend
cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\Backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
# Should start on http://localhost:8000

# Terminal 2: Emotion Service
cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\emotion_recognition"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python api.py
# Should start on http://localhost:5000

# Terminal 3: Frontend
cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\raga-rasa-soul-final-v2"
npm install
npm run dev
# Should start on http://localhost:5173
```

**Follow:** `LOCAL_DEVELOPMENT_GUIDE.md` for detailed steps

### Option B: Quick Start Script (Fastest)

**Best for:** Quick setup when you just want to run everything

```bash
# Windows CMD
start_local_dev.bat

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File start_local_dev.ps1
```

**Note:** Scripts will open 3 separate terminal windows

### Option C: Docker Compose (Easiest)

**Best for:** Isolated environment, no local Python/Node conflicts, consistent setup

```bash
cd "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya"
docker-compose up
```

**Requirements:** Docker Desktop installed

**Advantages:**
- ✅ No virtual environment setup needed
- ✅ Database included (MongoDB)
- ✅ All services networked automatically
- ✅ Logs in single terminal
- ✅ Easy cleanup: `docker-compose down`

**Access After Starting:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs
- Emotion Service: http://localhost:5000
- MongoDB: mongodb://root:root123@localhost:27017

---

## Project Structure

```
Raga Rasa Laya/
├── LOCAL_DEVELOPMENT_GUIDE.md          ⭐ START HERE
├── LOCAL_TESTING_CHECKLIST.md          ✅ VERIFY WITH THIS
├── LOCAL_SETUP_SUMMARY.md              📄 THIS FILE
├── docker-compose.yml                  🐳 DOCKER SETUP
│
├── Backend/                            🔧 API SERVER
│   ├── main.py
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── routes/
│   ├── requirements.txt
│   ├── .env                            (Configure here)
│   ├── .env.example
│   ├── Dockerfile.dev                  (For Docker)
│   └── venv/                           (Created during setup)
│
├── emotion_recognition/                🎭 EMOTION SERVICE
│   ├── api.py
│   ├── emotion_detector.py
│   ├── requirements.txt
│   ├── .env                            (Configure here)
│   ├── Dockerfile.dev                  (For Docker)
│   └── venv/                           (Created during setup)
│
├── raga-rasa-soul-final-v2/            🎨 FRONTEND
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   ├── .env.local                      (Configure here)
│   ├── Dockerfile.dev                  (For Docker)
│   └── node_modules/                   (Created during setup)
│
├── start_local_dev.bat                 🚀 QUICK START (CMD)
├── start_local_dev.ps1                 🚀 QUICK START (PowerShell)
│
└── [other project files and docs]
```

---

## Services Overview

### 1. Backend API (FastAPI) - Port 8000

**Purpose:** Main API server handling recommendations, emotions, songs, users

**Technologies:**
- FastAPI (Python async web framework)
- MongoDB (database)
- Uvicorn (ASGI server)

**Key Endpoints:**
- `GET /api/health` - Health check
- `GET /api/songs` - List all songs
- `POST /api/emotion/detect` - Detect emotion from text
- `POST /api/recommendations/generate` - Generate recommendations
- `GET /docs` - Swagger API documentation

**Environment Variables:**
```env
EMOTION_SERVICE_URL=http://localhost:5000/detect
MONGODB_URI=mongodb://localhost:27017
API_BASE_URL=http://localhost:8000
PORT=8000
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

### 2. Emotion Recognition Service (Flask) - Port 5000

**Purpose:** Emotion detection from text using HSEmotion model

**Technologies:**
- Flask (Python web framework)
- HSEmotion (emotion classification model)
- PyTorch (deep learning framework)

**Key Endpoints:**
- `GET /health` - Health check
- `POST /detect` - Detect emotion from text
- `GET /test` - Test endpoint

**Environment Variables:**
```env
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
```

**Note:** First request may be slow (~10 seconds) while model loads

### 3. Frontend (React + Vite) - Port 5173

**Purpose:** User interface for emotion detection and recommendations

**Technologies:**
- React (JavaScript UI library)
- TypeScript (type-safe JavaScript)
- Vite (build tool)
- Tailwind CSS (styling)

**Key Features:**
- Emotion detection UI
- Music recommendation display
- User authentication
- Responsive design

**Environment Variables:**
```env
VITE_API_URL=http://127.0.0.1:8000
VITE_APP_NAME=RagaRasa Music Therapy
VITE_ENV=development
```

### 4. Database (MongoDB)

**Purpose:** Persistent data storage

**Connection:**
- **Local:** `mongodb://localhost:27017`
- **Atlas:** `mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject`

**Collections:**
- `users` - User accounts
- `songs` - Music catalog
- `sessions` - User sessions
- `ratings` - User ratings

**Setup Tip:** Use MongoDB Atlas for local testing if you don't have MongoDB installed locally

---

## Step-by-Step Execution

### Choose Your Path:

**Path A: Manual Setup (Recommended)**
1. Read: `LOCAL_DEVELOPMENT_GUIDE.md` (15 minutes reading)
2. Execute: Follow Phase 1-4 step by step (30-40 minutes)
3. Verify: Use `LOCAL_TESTING_CHECKLIST.md` (20 minutes)
4. Debug: Refer to troubleshooting sections if needed
5. Total Time: ~1.5-2 hours

**Path B: Quick Script (Fast)**
1. Run: `start_local_dev.bat` or `start_local_dev.ps1` (1 minute)
2. Wait: 10-15 seconds for all services to start
3. Verify: Open http://localhost:5173 in browser
4. Check: No errors in console (F12)
5. Test: Follow `LOCAL_TESTING_CHECKLIST.md`
6. Total Time: ~30 minutes

**Path C: Docker Compose (Easiest)**
1. Install: Docker Desktop (if not already installed)
2. Run: `docker-compose up` from project root (5 minutes)
3. Wait: Services start automatically (~20 seconds)
4. Access: http://localhost:5173
5. Verify: Follow `LOCAL_TESTING_CHECKLIST.md`
6. Total Time: ~30 minutes (minus Docker install time)

---

## Environment Variables Checklist

Before running services, verify these files exist and are configured:

### Backend/.env
```
EMOTION_SERVICE_URL=http://localhost:5000/detect
MONGODB_URI=mongodb://localhost:27017
API_BASE_URL=http://localhost:8000
PORT=8000
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

### emotion_recognition/.env
```
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
```

### raga-rasa-soul-final-v2/.env.local
```
VITE_API_URL=http://127.0.0.1:8000
VITE_APP_NAME=RagaRasa Music Therapy
VITE_APP_VERSION=1.0.0
VITE_ENV=development
```

---

## Testing Flow

### Level 1: Individual Service Testing
- [ ] Backend starts and responds to `/api/health`
- [ ] Emotion Service starts and responds to `/health`
- [ ] Frontend loads without errors in browser

### Level 2: Service Communication
- [ ] Frontend can call Backend API
- [ ] Backend can call Emotion Service
- [ ] Database connections work

### Level 3: Feature Testing
- [ ] Emotion detection flow works end-to-end
- [ ] Recommendations are generated correctly
- [ ] Songs display properly

### Level 4: Error Handling
- [ ] App doesn't crash when services are unavailable
- [ ] Proper error messages shown to user
- [ ] No unhandled exceptions in logs

### Level 5: Performance
- [ ] Response times are acceptable (< 2 seconds)
- [ ] Memory usage is stable
- [ ] No resource leaks

---

## Troubleshooting Quick Links

| Problem | Solution | Reference |
|---------|----------|-----------|
| Port 8000 in use | Kill process or use different port | LOCAL_DEVELOPMENT_GUIDE.md → Troubleshooting |
| MongoDB connection error | Check MongoDB running or Atlas whitelist | LOCAL_DEVELOPMENT_GUIDE.md → Troubleshooting |
| CORS error in browser | Check backend CORS config, clear cache | LOCAL_DEVELOPMENT_GUIDE.md → Troubleshooting |
| Emotion service timeout | Wait for model download, check port 5000 | LOCAL_DEVELOPMENT_GUIDE.md → Troubleshooting |
| npm install failing | Check Node.js version, clear cache | LOCAL_DEVELOPMENT_GUIDE.md → Prerequisites |
| pip install failing | Check Python version, upgrade pip | LOCAL_DEVELOPMENT_GUIDE.md → Prerequisites |

---

## Common Commands Reference

```bash
# Python Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1              # Activate (PowerShell)
.\venv\Scripts\activate.bat              # Activate (CMD)
deactivate                               # Deactivate

# Python Package Management
pip install -r requirements.txt          # Install dependencies
pip install package_name                 # Install single package
pip list                                 # List installed packages

# Node Package Management
npm install                              # Install dependencies
npm install package_name                 # Install single package
npm run dev                              # Start dev server
npm run build                            # Build for production

# Python Service Commands
python main.py                           # Start Backend
python api.py                            # Start Emotion Service
python -c "code here"                    # Run Python code inline

# MongoDB
mongod                                   # Start local MongoDB (if installed)
mongo mongodb://connection_string        # Connect to MongoDB

# Process Management
netstat -ano | findstr :8000             # Find process on port 8000
taskkill /PID <PID> /F                   # Kill process
taskkill /F /IM python.exe               # Kill all Python processes
taskkill /F /IM node.exe                 # Kill all Node processes

# Git
git status                               # Check git status
git add .                                # Stage all changes
git commit -m "message"                  # Commit changes
git push                                 # Push to remote

# Docker (if using docker-compose)
docker-compose up                        # Start all services
docker-compose down                      # Stop all services
docker-compose logs -f                   # View logs
```

---

## Files Created Summary

| File | Purpose | Type |
|------|---------|------|
| LOCAL_DEVELOPMENT_GUIDE.md | Complete setup instructions | 📋 Doc |
| LOCAL_TESTING_CHECKLIST.md | Verification checklist | ✅ Doc |
| LOCAL_SETUP_SUMMARY.md | This file - quick reference | 📄 Doc |
| docker-compose.yml | Docker full-stack setup | 🐳 Config |
| Backend/Dockerfile.dev | Backend Docker image | 🐳 Config |
| emotion_recognition/Dockerfile.dev | Emotion service Docker image | 🐳 Config |
| raga-rasa-soul-final-v2/Dockerfile.dev | Frontend Docker image | 🐳 Config |
| start_local_dev.bat | Windows CMD quick start | 🚀 Script |
| start_local_dev.ps1 | Windows PowerShell quick start | 🚀 Script |

---

## Next Steps

### Immediate (Now)
1. Choose setup method (Manual / Quick Script / Docker)
2. Follow corresponding setup instructions
3. Verify all services are running
4. Check http://localhost:5173 loads without errors

### Short Term (After Setup)
1. Use `LOCAL_TESTING_CHECKLIST.md` to verify everything works
2. Test emotion detection flow
3. Test recommendations generation
4. Document any issues found

### Medium Term (When Ready for Cloud)
1. Commit all changes to GitHub
2. Deploy Emotion Service to HF Spaces
3. Deploy Backend to Google Cloud Run
4. Update Frontend with production URLs
5. Run production testing

### Long Term (Post-Deployment)
1. Monitor cloud services
2. Collect user feedback
3. Iterate and improve
4. Scale as needed

---

## Support Resources

### If You Get Stuck:
1. **Check Troubleshooting Section** in `LOCAL_DEVELOPMENT_GUIDE.md`
2. **Review Checklist** in `LOCAL_TESTING_CHECKLIST.md`
3. **Check Terminal Output** - Error messages usually tell you what's wrong
4. **Check Browser Console** (F12 → Console tab)
5. **Check Browser Network Tab** (F12 → Network tab)

### Key Documents to Reference:
- 📖 `LOCAL_DEVELOPMENT_GUIDE.md` - Detailed setup
- ✅ `LOCAL_TESTING_CHECKLIST.md` - Verification
- 🔗 `docker-compose.yml` - Docker setup (if using)
- 🚀 Quick start scripts - Fast setup

### Questions to Ask Yourself:
- Is the service running? (Check terminal window)
- Is the service on the right port? (Check .env files)
- Is the database connected? (Check MongoDB)
- Are environment variables correct? (Check .env files)
- Does the error message give a clue? (Read carefully)

---

## Success Criteria

Once you complete local setup, you'll have:

✅ Backend API running on http://localhost:8000
✅ Emotion Service running on http://localhost:5000
✅ Frontend running on http://localhost:5173
✅ All services communicating with each other
✅ No CORS errors in browser console
✅ API endpoints responding correctly
✅ Database connections working
✅ Ready for production deployment

---

## Important Notes

1. **First Time Emotion Model Load:** The first emotion detection request will take 5-10 seconds as the model is loaded into memory. Subsequent requests will be instant.

2. **MongoDB Connection:** If using MongoDB Atlas, ensure your IP address is whitelisted (0.0.0.0/0 for development).

3. **Port Conflicts:** If any service fails to start due to "port already in use", check what's using that port and either close it or change the port in the .env file.

4. **Virtual Environments:** Always activate the virtual environment (venv) before running Python commands. You should see `(venv)` prefix in your terminal.

5. **Git Commits:** After local testing is complete, commit your changes before deploying to the cloud.

---

## Quick Reference Diagram

```
Your Browser
    │
    ├─→ http://localhost:5173  ──→  Frontend (React)
    │                                    │
    │                                    ├─→ http://localhost:8000 ──→ Backend (FastAPI)
    │                                    │                                 │
    │                                    │                                 ├─→ MongoDB
    │                                    │                                 └─→ http://localhost:5000 ──→ Emotion Service
    │                                    │                                                                  │
    │                                    └─→ http://localhost:5000 ──→ (via Backend API)                   └─→ HSEmotion Model
    │
    └─ All connected, testing complete! ✅
```

---

**Status:** ✅ Local Development Environment Ready
**Total Setup Time:** 30-120 minutes (depending on method)
**Ready to Deploy:** After passing LOCAL_TESTING_CHECKLIST.md

Good luck with local testing! 🎉
