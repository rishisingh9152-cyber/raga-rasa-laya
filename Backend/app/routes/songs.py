from fastapi import APIRouter, UploadFile, File
import os
import shutil
from datetime import datetime
from pathlib import Path

from app.services.rass_service import RassService
from app.database import songs_collection

router = APIRouter()

# ----------------------------
# BASE DIRECTORY
# ----------------------------
BASE_DIR = r"C:\Users\rishi\OneDrive\Desktop\AI MUSIC PLAYER\Songs"
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# ----------------------------
# RASS FOLDERS
# ----------------------------
RASS_FOLDERS = {
    "shaant": os.path.join(BASE_DIR, "shaant"),
    "shok": os.path.join(BASE_DIR, "shok"),
    "shringar": os.path.join(BASE_DIR, "shringar"),
    "veer": os.path.join(BASE_DIR, "veer")
}

# ----------------------------
# CREATE DIRECTORIES
# ----------------------------
os.makedirs(TEMP_DIR, exist_ok=True)
for folder in RASS_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

# ----------------------------
# FILE VALIDATION
# ----------------------------
ALLOWED_EXTENSIONS = [".mp3", ".wav"]

def is_valid_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


# ----------------------------
# 🎯 UPLOAD API
# ----------------------------
@router.post("/songs/upload")
async def upload_song(file: UploadFile = File(...)):
    temp_path = None

    try:
        # ----------------------------
        # STEP 1: SAFE FILE NAME
        # ----------------------------
        safe_filename = Path(file.filename).name

        if not is_valid_file(safe_filename):
            return {"status": "error", "message": "Invalid file type"}

        # ----------------------------
        # STEP 2: DUPLICATE CHECK
        # ----------------------------
        existing = songs_collection.find_one({"song_name": safe_filename})
        if existing:
            return {"status": "error", "message": "Song already exists"}

        # ----------------------------
        # STEP 3: SAVE TEMP FILE
        # ----------------------------
        temp_path = os.path.join(TEMP_DIR, safe_filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("📥 FILE SAVED TO TEMP:", temp_path)

        # ----------------------------
        # STEP 4: RASS CLASSIFICATION
        # ----------------------------
        result = RassService.classify_song(temp_path)

        rass = result.get("rass", "unknown").lower()
        confidence = result.get("confidence", 0)

        print("🎯 FINAL RASS:", rass, "| CONF:", confidence)

        if rass not in RASS_FOLDERS:
            raise Exception(f"Invalid RASS category: {rass}")

        # ----------------------------
        # STEP 5: FINAL PATH
        # ----------------------------
        final_filename = safe_filename
        final_path = os.path.join(RASS_FOLDERS[rass], final_filename)

        # Handle duplicate filename
        if os.path.exists(final_path):
            name, ext = os.path.splitext(safe_filename)
            final_filename = f"{name}_{int(datetime.utcnow().timestamp())}{ext}"
            final_path = os.path.join(RASS_FOLDERS[rass], final_filename)

        print("📂 FINAL PATH:", final_path)

        # ----------------------------
        # STEP 6: STORE FILE (COPY + DELETE)
        # ----------------------------
        if not os.path.exists(temp_path):
            raise Exception("Temp file missing before copy")

        shutil.copy2(temp_path, final_path)
        print("✅ FILE COPIED TO FINAL LOCATION")

        os.remove(temp_path)
        print("🗑️ TEMP FILE REMOVED")

        # VERIFY
        if not os.path.exists(final_path):
            raise Exception("File not found after saving")

        print("✅ FILE VERIFIED IN FINAL FOLDER")

        # ----------------------------
        # STEP 7: SAVE TO DATABASE
        # ----------------------------
        song_doc = {
            "song_name": final_filename,
            "rass": rass,
            "file_path": final_path,
            "confidence": float(confidence),
            "avg_rating": 0,
            "num_users": 0,
            "is_new": True,
            "created_at": datetime.utcnow()
        }

        songs_collection.insert_one(song_doc)

        print("💾 SAVED TO DATABASE")

        # ----------------------------
        # RESPONSE
        # ----------------------------
        return {
            "status": "success",
            "song_name": final_filename,
            "rass": rass,
            "confidence": confidence
        }

    except Exception as e:

        print("❌ ERROR:", str(e))

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            print("🧹 TEMP CLEANED")

        return {
            "status": "error",
            "message": str(e)
        }