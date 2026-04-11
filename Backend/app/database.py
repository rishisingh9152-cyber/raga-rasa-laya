from pymongo import MongoClient
from datetime import datetime
import os

# Connect to MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
db = client["ai_music"]

# ==============================
# CORE COLLECTIONS
# ==============================
users_collection = db["users"]
songs_collection = db["songs"]
images_collection = db["images"]

# ==============================
# NEW: LEARNING SYSTEM COLLECTIONS
# ==============================
psychometric_tests_collection = db["psychometric_tests"]
ratings_collection = db["ratings"]
sessions_collection = db["sessions"]
context_scores_collection = db["context_scores"]

# ==============================
# CREATE INDEXES FOR PERFORMANCE
# ==============================
def create_indexes():
    """
    Create necessary indexes for queries.
    Indexes improve query performance, especially for large datasets.
    Call this once on application startup.
    """
    
    # ==============================
    # RATINGS INDEXES
    # ==============================
    # Find ratings by song_id (used in get_song_ratings)
    ratings_collection.create_index("song_id")
    
    # Find ratings by user_id (track user's feedback)
    ratings_collection.create_index("user_id")
    
    # Find ratings by session_id (link to session)
    ratings_collection.create_index("session_id")
    
    # Find ratings by (song, emotion) for analytics
    ratings_collection.create_index([("song_id", 1), ("emotion_feedback", 1)])
    
    # Find recent ratings efficiently
    ratings_collection.create_index("timestamp")
    
    # ==============================
    # PSYCHOMETRIC TESTS INDEXES
    # ==============================
    # Find tests by user_id
    psychometric_tests_collection.create_index("user_id")
    
    # Find tests by session_id
    psychometric_tests_collection.create_index("session_id")
    
    # Find recent tests
    psychometric_tests_collection.create_index("timestamp")
    
    # ==============================
    # SESSIONS INDEXES
    # ==============================
    # Find sessions by user_id
    sessions_collection.create_index("user_id")
    
    # Find sessions by status (completed/in_progress)
    sessions_collection.create_index("status")
    
    # Find sessions by time range
    sessions_collection.create_index("start_time")
    
    # ==============================
    # CONTEXT SCORES INDEXES
    # ==============================
    # Find context by (song, emotion) for recommendation scoring
    context_scores_collection.create_index([("song_id", 1), ("emotion", 1)])
    
    # Find all contexts for a song
    context_scores_collection.create_index("song_id")
    
    # ==============================
    # SONGS INDEXES
    # ==============================
    # Find songs by rass (used in recommendation)
    songs_collection.create_index("rass")
    
    # Find songs by recommendation count (fairness)
    songs_collection.create_index("recommendation_count")
    
    print("✅ Database indexes created successfully")


# ==============================
# HELPER FUNCTIONS
# ==============================

def reset_learning_data():
    """
    WARNING: This deletes all learning data (ratings, context scores, sessions).
    Used for testing/development only.
    """
    ratings_collection.delete_many({})
    context_scores_collection.delete_many({})
    sessions_collection.delete_many({})
    psychometric_tests_collection.delete_many({})
    print("⚠️  All learning data has been cleared")


def get_database_stats():
    """
    Get statistics about the database
    """
    return {
        "songs": songs_collection.count_documents({}),
        "ratings": ratings_collection.count_documents({}),
        "sessions": sessions_collection.count_documents({}),
        "psychometric_tests": psychometric_tests_collection.count_documents({}),
        "context_scores": context_scores_collection.count_documents({})
    }


# ==============================
# STARTUP
# ==============================
# Call create_indexes() once when your application starts
# Example in main.py:
# @app.on_event("startup")
# def startup():
#     create_indexes()
