import sys
import os
import shutil
from datetime import datetime

# Fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import songs_collection

# ----------------------------
# SOURCE DATASET
# ----------------------------
SOURCE_DIR = r"C:\Users\rishi\OneDrive\Desktop\raas"

# ----------------------------
# DESTINATION PATHS (PER RASS)
# ----------------------------
DEST_PATHS = {
    "shaant": r"C:\Users\rishi\OneDrive\Desktop\AI MUSIC PLAYER\Songs\shaant",
    "shok": r"C:\Users\rishi\OneDrive\Desktop\AI MUSIC PLAYER\Songs\shok",
    "shringar": r"C:\Users\rishi\OneDrive\Desktop\AI MUSIC PLAYER\Songs\shringar",
    "veer": r"C:\Users\rishi\OneDrive\Desktop\AI MUSIC PLAYER\Songs\veer"
}


def normalize_path(p):
    return os.path.normcase(os.path.normpath(p))


def seed_and_copy_songs():
    total_added = 0
    total_skipped = 0
    total_copied = 0

    for rass, dest_folder in DEST_PATHS.items():

        source_folder = os.path.join(SOURCE_DIR, rass)

        if not os.path.exists(source_folder):
            print(f"❌ Missing source folder: {source_folder}")
            continue

        os.makedirs(dest_folder, exist_ok=True)

        print(f"\n📂 Processing: {rass}")

        for file in os.listdir(source_folder):

            if not file.lower().endswith((".mp3", ".wav")):
                continue

            source_path = normalize_path(os.path.join(source_folder, file))
            dest_path = normalize_path(os.path.join(dest_folder, file))

            # ----------------------------
            # 📁 ALWAYS COPY FILE (FIXED LOGIC)
            # ----------------------------
            if not os.path.exists(dest_path):
                try:
                    shutil.copy2(source_path, dest_path)
                    print(f"📥 Copied: {file}")
                    total_copied += 1
                except Exception as e:
                    print(f"❌ Copy failed: {file} → {e}")
                    continue
            else:
                print(f"⚠️ Already exists in folder: {file}")

            # ----------------------------
            # 🚫 DUPLICATE CHECK (DB ONLY)
            # ----------------------------
            existing = songs_collection.find_one({
                "$or": [
                    {"file_path": dest_path},
                    {"song_name": file, "rass": rass}
                ]
            })

            if existing:
                print(f"⚠️ Skipped DB insert: {file}")
                total_skipped += 1
                continue

            # ----------------------------
            # 💾 INSERT INTO DB
            # ----------------------------
            song_doc = {
                "song_name": file,
                "rass": rass,
                "file_path": dest_path,
                "features": [],
                "confidence": 0.5,
                "ratings": {
                    "avg_rating": 0,
                    "num_users": 0
                },
                "created_at": datetime.utcnow()
            }

            songs_collection.insert_one(song_doc)

            print(f"✅ Added to DB: {file}")
            total_added += 1

    print("\n----------------------------")
    print(f"📥 Total Copied: {total_copied}")
    print(f"✅ Total Added to DB: {total_added}")
    print(f"⚠️ Total Skipped DB: {total_skipped}")
    print("----------------------------")


if __name__ == "__main__":
    seed_and_copy_songs()