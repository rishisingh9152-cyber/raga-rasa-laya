"""
UPLOAD SONGS TO CLOUDINARY AND UPDATE MONGODB

This script:
1. Scans all songs in the Dropbox/raga-rasa/Songs folder
2. Uploads them to Cloudinary
3. Updates MongoDB with the Cloudinary URLs

Requirements:
- cloudinary package: pip install cloudinary
- Cloudinary account with API credentials
"""

import os
import sys
import io

# Force UTF-8 encoding for stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from pathlib import Path
from pymongo import MongoClient
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ==============================
# CLOUDINARY CONFIGURATION
# ==============================
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    print("\nERROR: Cloudinary credentials not set!")
    print("\nSet environment variables:")
    print("  CLOUDINARY_CLOUD_NAME = your_cloud_name")
    print("  CLOUDINARY_API_KEY = your_api_key")
    print("  CLOUDINARY_API_SECRET = your_api_secret")
    print("\nGet credentials from: https://cloudinary.com/console/settings/api")
    sys.exit(1)

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# ==============================
# MONGODB CONFIGURATION
# ==============================
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
db = client["ai_music"]
songs_collection = db["songs"]

# ==============================
# DROPBOX FOLDER CONFIGURATION
# ==============================
DROPBOX_FOLDER = os.path.expanduser("~") + r"\Dropbox\raga-rasa\Songs"

# ==============================
# UPLOAD TO CLOUDINARY
# ==============================
def upload_song_to_cloudinary(file_path, song_name, rass):
    """Upload a single song to Cloudinary"""
    
    try:
        # Create a unique public ID for the song
        # Sanitize special characters to prevent Cloudinary errors
        song_title = os.path.splitext(song_name)[0]
        # Replace special characters with underscores
        safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in song_title)
        public_id = f"raga-rasa/{rass}/{safe_title}"
        
        # Truncate if too long (Cloudinary has limits)
        if len(public_id) > 100:
            public_id = public_id[:100]
        
        try:
            display_name = song_name[:50]
        except:
            display_name = "[song with special chars]"
        
        print(f"  Uploading: {display_name}", end="...", flush=True)
        
        # Upload the audio file
        result = cloudinary.uploader.upload(
            file_path,
            resource_type="video",  # Use "video" for audio files
            public_id=public_id,
            overwrite=True,
            eager=[
                {
                    "resource_type": "video",
                    "format": "mp3"
                }
            ],
            eager_async=True
        )
        
        # Get the streaming URL (converted to mp3)
        cloudinary_url = result.get("url")
        secure_url = result.get("secure_url", cloudinary_url)
        
        # For audio streaming, use the mp3 format
        if "mp3" in secure_url:
            streaming_url = secure_url
        else:
            # Convert URL to mp3 format for consistent streaming
            streaming_url = secure_url.replace(
                f"/{safe_title}",
                f"/mp3/{safe_title}"
            )
        
        print(f" OK")
        return streaming_url
    
    except Exception as e:
        try:
            error_msg = str(e)[:50]
        except:
            error_msg = "encoding error"
        print(f" FAIL - {error_msg}")
        return None


# ==============================
# GET SONGS FROM DROPBOX
# ==============================
def get_songs_from_dropbox():
    """Scan Dropbox and collect song information"""
    
    songs = []
    rass_folders = {
        "shaant": os.path.join(DROPBOX_FOLDER, "shaant"),
        "shok": os.path.join(DROPBOX_FOLDER, "shok"),
        "shringar": os.path.join(DROPBOX_FOLDER, "shringar"),
        "veer": os.path.join(DROPBOX_FOLDER, "veer")
    }
    
    for rass, folder_path in rass_folders.items():
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue
        
        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".mp3", ".wav")):
                file_path = os.path.join(folder_path, filename)
                songs.append({
                    "filename": filename,
                    "file_path": file_path,
                    "rass": rass
                })
    
    return songs


# ==============================
# UPDATE MONGODB WITH CLOUDINARY URLS
# ==============================
def update_mongodb_with_cloudinary_urls(song_info, cloudinary_url):
    """Update or insert song in MongoDB with Cloudinary URL"""
    
    try:
        result = songs_collection.update_one(
            {"song_name": song_info["filename"]},
            {
                "$set": {
                    "cloudinary_url": cloudinary_url,
                    "streaming_url": cloudinary_url,
                    "rass": song_info["rass"],
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        return result.matched_count > 0 or result.upserted_id is not None
    
    except Exception as e:
        print(f"  ERROR updating MongoDB: {e}")
        return False


# ==============================
# MAIN
# ==============================
def main():
    
    print(f"\n{'='*70}")
    print(f"UPLOADING SONGS TO CLOUDINARY AND UPDATING MONGODB")
    print(f"{'='*70}\n")
    
    # Step 1: Get songs from Dropbox
    print("Step 1: Scanning Dropbox folders...")
    songs = get_songs_from_dropbox()
    print(f"Found {len(songs)} songs\n")
    
    if not songs:
        print("ERROR: No songs found in Dropbox!")
        sys.exit(1)
    
    # Step 2: Upload to Cloudinary
    print("Step 2: Uploading songs to Cloudinary...")
    print("-" * 70)
    
    uploaded_count = 0
    error_count = 0
    
    for i, song_info in enumerate(songs, 1):
        try:
            display_name = song_info['filename'][:50]
        except:
            display_name = "[song]"
        print(f"[{i}/{len(songs)}] {display_name}")
        
        cloudinary_url = upload_song_to_cloudinary(
            song_info["file_path"],
            song_info["filename"],
            song_info["rass"]
        )
        
        if cloudinary_url:
            # Step 3: Update MongoDB
            if update_mongodb_with_cloudinary_urls(song_info, cloudinary_url):
                uploaded_count += 1
            else:
                error_count += 1
        else:
            error_count += 1
    
    # ==============================
    # SUMMARY
    # ==============================
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Total songs:     {len(songs)}")
    print(f"Uploaded:        {uploaded_count}")
    print(f"Errors:          {error_count}")
    print(f"In MongoDB:      {songs_collection.count_documents({})}")
    print(f"{'='*70}\n")
    
    # Verify
    print("Sample songs with Cloudinary URLs:\n")
    sample = list(songs_collection.find().limit(3))
    for i, song in enumerate(sample, 1):
        print(f"{i}. {song.get('song_name', 'Unknown')}")
        print(f"   Rass: {song.get('rass', 'N/A')}")
        url = song.get('cloudinary_url') or song.get('streaming_url', 'NOT SET')
        print(f"   URL: {url[:80]}...")
        print()
    
    return uploaded_count == len(songs)


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("SUCCESS! All songs uploaded and MongoDB updated\n")
            sys.exit(0)
        else:
            print("Some songs failed to upload. Check errors above.\n")
            sys.exit(1)
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
