# MongoDB Local Setup Guide - RagaRasa Music Therapy

**Status:** ✅ MongoDB is already installed and running on your system!

---

## Current Setup Summary

### MongoDB Installation
- **Version:** 8.2.5
- **Status:** ✅ Running (Windows Service)
- **Connection:** mongodb://localhost:27017 (default)
- **Default Port:** 27017

### Databases
- **raga_rasa** - Main application database (✅ Ready to use)
  - 68 songs loaded
  - 7 collections ready
- **ai_music** - Alternative database (available)

### Collections in raga_rasa
1. `songs` - Music catalog (68 documents)
2. `users` - User accounts
3. `sessions` - User sessions
4. `ratings` - User ratings and feedback
5. `psychometric_tests` - Test results
6. `context_scores` - Recommendation scoring data
7. `images` - Image storage

---

## ✅ Quick Start - Everything is Ready!

### Step 1: Verify MongoDB is Running

```bash
# Check MongoDB service status
Get-Service -Name MongoDB | Select-Object Name, Status

# Should show: MongoDB  Running
```

### Step 2: Test Connection

```bash
# Test MongoDB connection
mongosh --eval "db.adminCommand('ping')"

# Should return: { ok: 1 }
```

### Step 3: Check Your Data

```bash
# Count songs in database
mongosh raga_rasa --eval "db.songs.countDocuments({})"

# Should return: 68
```

---

## Backend Configuration

### Backend/.env (Already Configured)

```env
# MONGODB CONFIGURATION
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=raga_rasa

# LOCAL Development
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# LOCAL Emotion Service
EMOTION_SERVICE_URL=http://localhost:5000/detect
```

**This is already set for local MongoDB development!** ✅

---

## How to Start the Stack

### All Three Services with Local MongoDB

**Terminal 1: Backend (Uses local MongoDB)**
```bash
cd Backend
.\venv\Scripts\Activate.ps1
python main.py
# Connects to: mongodb://localhost:27017/raga_rasa
```

**Terminal 2: Emotion Service**
```bash
cd emotion_recognition
.\venv\Scripts\Activate.ps1
python api.py
```

**Terminal 3: Frontend**
```bash
cd raga-rasa-soul-final-v2
npm run dev
```

---

## Verify MongoDB Connection in Backend

When you start the Backend, you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
Connecting to MongoDB: mongodb://localhost:27017...
✅ Database indexes created successfully
```

This confirms:
- ✅ Backend started
- ✅ Connected to local MongoDB
- ✅ Database indexes created

---

## Test Data Available

### Songs in Database
```bash
# See first song
mongosh raga_rasa --eval "db.songs.findOne()"

# Shows: Title, Rass, Composer, etc.
```

### Example Query
```bash
# Count songs by Rass (Emotion)
mongosh raga_rasa --eval "db.songs.aggregate([{$group: {_id: '$rass', count: {$sum: 1}}}])"
```

---

## Using MongoDB with Your Application

### Backend Automatically Uses Local MongoDB

The Backend code connects like this:

```python
# Backend/app/database.py
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
db = client["raga_rasa"]  # Uses raga_rasa database
```

**Your .env has:** `MONGODB_URI=mongodb://localhost:27017`

**Result:** Connects to local MongoDB automatically ✅

---

## Common MongoDB Commands

### Check Connection
```bash
mongosh --eval "db.adminCommand('ping')"
```

### List All Databases
```bash
mongosh --eval "db.adminCommand('listDatabases')"
```

### Connect to raga_rasa Database
```bash
mongosh raga_rasa
```

### Count Documents
```bash
mongosh raga_rasa --eval "db.songs.countDocuments({})"
mongosh raga_rasa --eval "db.users.countDocuments({})"
mongosh raga_rasa --eval "db.ratings.countDocuments({})"
```

### View Sample Song
```bash
mongosh raga_rasa --eval "db.songs.findOne()" | more
```

### Delete All Documents (⚠️ WARNING)
```bash
mongosh raga_rasa --eval "db.songs.deleteMany({})"
```

---

## MongoDB Management Tools

### Option 1: MongoDB Compass (GUI - Recommended)

**Install:**
1. Download from: https://www.mongodb.com/products/compass
2. Install and run
3. It auto-detects local MongoDB
4. Browse databases visually

**Features:**
- Visual database explorer
- Create/edit documents
- Run queries
- View indexes
- Monitor performance

### Option 2: mongosh (CLI - Already installed)

```bash
# Interactive MongoDB shell
mongosh raga_rasa

# See databases
show dbs

# See collections
show collections

# Query
db.songs.find().limit(1)
```

### Option 3: MongoDB Atlas (Cloud - Optional)

Use MongoDB Atlas for cloud backups:
```
Connection: mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/raga_rasa
```

---

## Troubleshooting

### MongoDB Won't Start

**Check Service:**
```bash
Get-Service -Name MongoDB
```

**Start Service (if stopped):**
```bash
Start-Service -Name MongoDB
```

**Or restart:**
```bash
Restart-Service -Name MongoDB
```

### Can't Connect to MongoDB

**Check if running:**
```bash
netstat -ano | findstr :27017
```

**If port 27017 is in use but not MongoDB:**
```bash
# Find what's using port 27017
netstat -ano | findstr :27017

# Kill the process
taskkill /PID <PID> /F

# Restart MongoDB service
Restart-Service -Name MongoDB
```

### Backend Can't Connect to MongoDB

**Error:** `MongoServerSelectionError: connect ECONNREFUSED`

**Solution:**
```bash
# Check MongoDB is running
Get-Service -Name MongoDB

# Verify connection string in Backend/.env
MONGODB_URI=mongodb://localhost:27017

# Test connection
mongosh --eval "db.adminCommand('ping')"
```

### Collections Missing

**Check what's in your database:**
```bash
mongosh raga_rasa
show collections
```

**If collections are missing, they'll be created automatically when:**
- Backend starts and calls `create_indexes()`
- Or when data is first inserted

---

## Database Backup & Restore

### Backup Local Database

```bash
# Export to file
mongodump --db raga_rasa --out "C:\MongoDB\Backups\raga_rasa_backup"

# Restore from file
mongorestore "C:\MongoDB\Backups\raga_rasa_backup"
```

### Export Collection to JSON

```bash
mongoexport --db raga_rasa --collection songs --out songs.json
```

---

## Performance Tips

### Create Indexes (Automatic)
Backend automatically creates these indexes on startup:

```python
# Query optimization
ratings_collection.create_index("song_id")
ratings_collection.create_index("user_id")
sessions_collection.create_index("user_id")
songs_collection.create_index("rass")
```

### Monitor Performance

```bash
# Check database stats
mongosh raga_rasa --eval "db.stats()"

# Check index usage
mongosh raga_rasa --eval "db.collection.aggregate([{$indexStats: {}}])"
```

---

## Switching Databases

If you want to use `ai_music` instead of `raga_rasa`:

### Option 1: Change Backend/.env
```env
# Change this:
DATABASE_NAME=raga_rasa

# To this:
DATABASE_NAME=ai_music
```

Then restart Backend.

### Option 2: Change database.py
```python
# In Backend/app/database.py, line 10
db = client["ai_music"]  # Change from "ai_music" to desired database
```

---

## Network Connections

### Local Development (Current Setup)
```
MongoDB (port 27017) ← Backend (port 8000) ← Frontend (port 5173)
```

**Connection string:** `mongodb://localhost:27017`

### Production Setup (Later)
```
MongoDB Atlas (cloud) ← Cloud Backend ← Frontend
```

**Connection string:** `mongodb+srv://user:pass@cluster.mongodb.net/db`

---

## MongoDB Atlas (Optional)

If you want to use MongoDB Atlas for cloud backups:

```bash
# Replace connection string in Backend/.env
MONGODB_URI=mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject

# Test connection
mongosh "mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/raga_rasa"
```

---

## File Locations

### MongoDB Installation
```
C:\Program Files\MongoDB\Server\8.2\
```

### MongoDB Data
```
C:\Data\db\
```

### MongoDB Configuration
```
C:\Program Files\MongoDB\Server\8.2\mongod.cfg
```

### MongoDB Service
- **Service Name:** MongoDB
- **Status:** View in Services.msc

---

## Summary - Everything Ready

✅ **MongoDB Status:**
- Version: 8.2.5
- Status: Running
- Data: 68 songs in raga_rasa database
- Collections: 7 (songs, users, sessions, ratings, psychometric_tests, context_scores, images)

✅ **Backend Configuration:**
- Connection string: mongodb://localhost:27017
- Database: raga_rasa
- DEBUG: Enabled for development
- Emotion service: http://localhost:5000/detect

✅ **Ready to Start:**
1. Run Backend (connects to local MongoDB)
2. Run Emotion Service
3. Run Frontend
4. Open http://localhost:5173

✅ **Your Data is Safe:**
- 68 songs already loaded
- Can query with mongosh
- Can visualize with MongoDB Compass
- Can backup anytime

---

## Next Steps

1. **Start all services** (Backend, Emotion, Frontend)
2. **Test the application** - Use LOCAL_TESTING_CHECKLIST.md
3. **Verify MongoDB connection** - Check Backend logs for "✅ Database indexes created"
4. **Browse data** - Use mongosh or MongoDB Compass
5. **Test recommendations** - Should pull from your local database

---

## Support

**Command Reference:**
```bash
# Check service status
Get-Service MongoDB

# Check connection
mongosh --eval "db.adminCommand('ping')"

# List databases
mongosh --eval "db.adminCommand('listDatabases')"

# Count songs
mongosh raga_rasa --eval "db.songs.countDocuments({})"

# View sample song
mongosh raga_rasa --eval "db.songs.findOne()"
```

---

**Everything is set up and ready to go! Your local MongoDB instance is connected and ready for testing.** 🎉
