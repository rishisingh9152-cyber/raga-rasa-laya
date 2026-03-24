from pymongo import MongoClient

# connect to local MongoDB
client = MongoClient("mongodb://localhost:27017")

db = client["ai_music"]

# collections
users_collection = db["users"]
songs_collection = db["songs"]
images_collection = db["images"]