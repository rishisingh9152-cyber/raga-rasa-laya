"""
Verify Cloudinary uploads and MongoDB status
"""
import os
import sys
import cloudinary
import cloudinary.api
from pymongo import MongoClient

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

print("\n" + "="*70)
print("CLOUDINARY AND MONGODB STATUS")
print("="*70 + "\n")

# Check Cloudinary
print("CLOUDINARY STATUS:")
try:
    result = cloudinary.api.resources(type='upload', max_results=5, prefix='raga-rasa')
    print(f"  Total assets in Cloudinary: {result['total_count']}")
    print(f"  Sample assets:")
    for asset in result['resources'][:3]:
        print(f"    - {asset['public_id']}")
except Exception as e:
    print(f"  ERROR: {e}")

# Check MongoDB
print("\nMONGODB STATUS:")
try:
    total_songs = songs_collection.count_documents({})
    songs_with_urls = songs_collection.count_documents({"cloudinary_url": {"$exists": True, "$ne": None}})
    print(f"  Total songs in DB: {total_songs}")
    print(f"  Songs with Cloudinary URLs: {songs_with_urls}")
    
    print(f"\n  Sample songs from MongoDB:")
    for i, song in enumerate(songs_collection.find().limit(3), 1):
        print(f"    {i}. {song.get('song_name', 'Unknown')}")
        print(f"       Rass: {song.get('rass', 'N/A')}")
        url = song.get('cloudinary_url', 'NOT SET')
        if url:
            print(f"       URL: {url[:70]}...")
        else:
            print(f"       URL: NOT SET")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "="*70 + "\n")
