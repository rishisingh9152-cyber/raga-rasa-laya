"""
Retry failed song upload
"""
import os
import sys
import cloudinary
import cloudinary.uploader
from pymongo import MongoClient
from datetime import datetime

# Cloudinary setup
cloudinary.config(
    cloud_name='dlx3ufj3t',
    api_key='255318353319693',
    api_secret='MKFvdiyfmNpzxbaGKBMFM6SlT2c'
)

# MongoDB setup
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
db = client["ai_music"]
songs_collection = db["songs"]

# Failed song info
FAILED_SONG = "darbarikanad_vilayatkhan_karuna.wav"
FAILED_PATH = os.path.expanduser("~") + r"\Dropbox\raga-rasa\Songs\shok\darbarikanad_vilayatkhan_karuna.wav"
RASS = "shok"

print(f"\nRetrying upload for: {FAILED_SONG}")
print(f"Path: {FAILED_PATH}")
print(f"Rass: {RASS}\n")

if not os.path.exists(FAILED_PATH):
    print(f"ERROR: File not found at {FAILED_PATH}")
    sys.exit(1)

try:
    # Sanitize title for Cloudinary
    song_title = os.path.splitext(FAILED_SONG)[0]
    safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in song_title)
    public_id = f"raga-rasa/{RASS}/{safe_title}"
    
    if len(public_id) > 100:
        public_id = public_id[:100]
    
    print(f"Uploading with public_id: {public_id}")
    
    # Upload
    result = cloudinary.uploader.upload(
        FAILED_PATH,
        resource_type="video",
        public_id=public_id,
        overwrite=True,
        eager=[{"resource_type": "video", "format": "mp3"}],
        eager_async=True
    )
    
    cloudinary_url = result.get("secure_url", result.get("url"))
    
    print(f"Upload successful!")
    print(f"URL: {cloudinary_url}")
    
    # Update MongoDB
    result = songs_collection.update_one(
        {"song_name": FAILED_SONG},
        {
            "$set": {
                "cloudinary_url": cloudinary_url,
                "streaming_url": cloudinary_url,
                "rass": RASS,
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )
    
    print(f"MongoDB updated!")
    print(f"\nSUCCESS: Song is now available in Cloudinary and MongoDB\n")
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
