"""
GET PROPER DROPBOX SHAREABLE LINKS USING DROPBOX API

This script requires:
1. Dropbox account access token (from https://www.dropbox.com/developers)
2. dropbox Python package installed

If you don't have API access, alternative methods:
- Manually right-click files in Dropbox and get share links
- Use Dropbox web interface to create shareable links
- Configure a cloud storage service with public sharing

For now, this creates placeholder URLs that you can update manually.
"""

import os
import sys
from pymongo import MongoClient
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================
DROPBOX_FOLDER = os.path.expanduser("~") + r"\Dropbox\raga-rasa\Songs"
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

client = MongoClient(MONGODB_URI)
db = client["ai_music"]
songs_collection = db["songs"]

# Dropbox API token (you need to generate this from Dropbox Developer Console)
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN", None)


# ==============================
# METHOD 1: USING DROPBOX API (if token available)
# ==============================
def get_dropbox_urls_via_api():
    """Get shareable links using Dropbox API"""
    
    if not DROPBOX_ACCESS_TOKEN:
        print("WARNING: DROPBOX_ACCESS_TOKEN not set")
        print("To use Dropbox API:")
        print("1. Go to https://www.dropbox.com/developers/apps")
        print("2. Create a new app and generate access token")
        print("3. Set environment variable: DROPBOX_ACCESS_TOKEN=<token>")
        print()
        return False
    
    try:
        import dropbox
    except ImportError:
        print("ERROR: dropbox package not installed")
        print("Install with: pip install dropbox")
        return False
    
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        
        # List files in the folder
        result = dbx.files_list_folder("/raga-rasa/Songs", recursive=True)
        
        print(f"\nFound {len(result.entries)} files in Dropbox")
        
        updated_count = 0
        
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                filename = entry.name
                
                try:
                    # Create shareable link
                    shared_link = dbx.sharing_create_shared_link_with_settings(
                        entry.path_display,
                        dropbox.sharing.SharedLinkSettings(
                            requested_visibility=dropbox.sharing.RequestedVisibility.public
                        )
                    )
                    
                    dropbox_url = shared_link.url.replace("dl=0", "dl=1")
                    
                    # Update MongoDB
                    result = songs_collection.update_one(
                        {"song_name": filename},
                        {
                            "$set": {
                                "dropbox_url": dropbox_url,
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                    
                    if result.modified_count > 0:
                        print(f"  Updated: {filename}")
                        updated_count += 1
                
                except dropbox.exceptions.ApiError as e:
                    # Link might already exist
                    if "already_exists" in str(e):
                        print(f"  Already shared: {filename}")
                    else:
                        print(f"  Error: {filename} - {e}")
        
        print(f"\nUpdated {updated_count} songs with Dropbox URLs\n")
        return True
    
    except Exception as e:
        print(f"ERROR with Dropbox API: {e}\n")
        return False


# ==============================
# METHOD 2: MANUAL INSTRUCTIONS
# ==============================
def provide_manual_instructions():
    """Provide instructions for manual URL creation"""
    
    print(f"\n{'='*70}")
    print(f"MANUAL METHOD: CREATE DROPBOX SHARING LINKS")
    print(f"{'='*70}\n")
    
    print("""
To get proper Dropbox shareable links for your songs:

OPTION A: Use Dropbox Web Interface
1. Go to https://www.dropbox.com
2. Navigate to: raga-rasa/Songs/[RASS_NAME]/
3. Right-click on a song file
4. Select "Share"
5. Click "Create link"
6. Copy the link (format: https://www.dropbox.com/s/[FILE_ID]/filename?dl=0)
7. Change ?dl=0 to ?dl=1 at the end for download/streaming

OPTION B: Use This Script Format
For each song file, get the share link and we'll update MongoDB.

OPTION C: Configure Public Folder
Make the raga-rasa folder public and use direct file paths:
https://dl.dropboxusercontent.com/s/[FILE_ID]/raga-rasa/Songs/rass/filename?dl=1

    """)
    
    # Count songs by rass
    rass_folders = {
        "shaant": os.path.join(DROPBOX_FOLDER, "shaant"),
        "shok": os.path.join(DROPBOX_FOLDER, "shok"),
        "shringar": os.path.join(DROPBOX_FOLDER, "shringar"),
        "veer": os.path.join(DROPBOX_FOLDER, "veer")
    }
    
    print("Songs to share:\n")
    for rass, folder in rass_folders.items():
        if os.path.exists(folder):
            songs = [f for f in os.listdir(folder) if f.lower().endswith((".mp3", ".wav"))]
            print(f"{rass.upper()}: {len(songs)} songs")
            for song in sorted(songs)[:3]:
                print(f"  - {song}")
            if len(songs) > 3:
                print(f"  ... and {len(songs) - 3} more")
        print()


# ==============================
# METHOD 3: GENERATE TEMPLATE URLs
# ==============================
def create_template_urls():
    """Create template URLs that users can fill in manually"""
    
    print(f"\n{'='*70}")
    print(f"GENERATING TEMPLATE FOR MANUAL URL FILLING")
    print(f"{'='*70}\n")
    
    template_file = "dropbox_urls_template.csv"
    
    with open(template_file, "w", encoding="utf-8") as f:
        f.write("song_name,rass,dropbox_url\n")
        
        rass_folders = {
            "shaant": os.path.join(DROPBOX_FOLDER, "shaant"),
            "shok": os.path.join(DROPBOX_FOLDER, "shok"),
            "shringar": os.path.join(DROPBOX_FOLDER, "shringar"),
            "veer": os.path.join(DROPBOX_FOLDER, "veer")
        }
        
        for rass, folder in rass_folders.items():
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    if filename.lower().endswith((".mp3", ".wav")):
                        f.write(f'"{filename}","{rass}","https://www.dropbox.com/s/[FILE_ID]/{filename}?dl=1"\n')
    
    print(f"Created template file: {template_file}")
    print("""
Instructions:
1. Open {0} in a text editor or Excel
2. For each song, replace [FILE_ID] with the actual Dropbox file ID
3. Get file IDs from: right-click file → Share → Copy link
   (the link format is: https://www.dropbox.com/s/[FILE_ID]/filename?dl=0)
4. Save the file
5. Run: python update_from_csv.py

    """.format(template_file))


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    print(f"\n{'='*70}")
    print(f"DROPBOX URL UPDATE METHODS")
    print(f"{'='*70}\n")
    
    # Try API method first
    if DROPBOX_ACCESS_TOKEN:
        print("Attempting to use Dropbox API...\n")
        if get_dropbox_urls_via_api():
            print("\nSUCCESS! All songs updated via Dropbox API\n")
            sys.exit(0)
    
    # Fall back to manual methods
    print("Dropbox API not available. Using manual methods...\n")
    provide_manual_instructions()
    create_template_urls()
    
    print(f"\n{'='*70}")
    print(f"NEXT STEPS:")
    print(f"{'='*70}")
    print("""
1. Get Dropbox shareable links for all songs
2. Update MongoDB with the URLs using one of these methods:
   - Use the Dropbox API with a valid access token
   - Fill in the template CSV and run update_from_csv.py
   - Use the MongoDB admin interface to update manually
3. Test with: python test_dropbox_urls.py

    """)
