"""
Test script to verify MongoDB connection from Backend
Run this in the Backend directory with venv activated
"""

import os
import sys
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

# Load .env file
def load_env():
    """Load environment variables from .env file"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip()

def test_mongodb_connection():
    """Test connection to local MongoDB"""
    
    print("\n" + "="*60)
    print("MongoDB Connection Test for RagaRasa Backend")
    print("="*60 + "\n")
    
    # Get connection string from .env or use default
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    database_name = os.getenv("DATABASE_NAME", "raga_rasa")
    
    print("[*] Connection String: " + mongodb_uri)
    print("[*] Database Name: " + database_name + "\n")
    
    try:
        print("[+] Connecting to MongoDB...")
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection with ping
        print("[+] Sending ping command...")
        result = client.admin.command('ping')
        print("[OK] Ping successful: " + str(result) + "\n")
        
        # Get list of databases
        print("[*] Available Databases:")
        admin = client['admin']
        databases = admin.command('listDatabases')
        for db in databases['databases']:
            print("    - " + db['name'])
        print()
        
        # Connect to specific database
        print("[*] Connecting to database: " + database_name)
        db = client[database_name]
        
        # List collections
        print("[*] Collections in " + database_name + ":")
        collections = db.list_collection_names()
        for col in collections:
            count = db[col].count_documents({})
            print("    - " + col + ": " + str(count) + " documents")
        print()
        
        # Check songs collection specifically
        if 'songs' in collections:
            songs_count = db['songs'].count_documents({})
            print("[*] Songs Collection: " + str(songs_count) + " songs loaded")
            
            if songs_count > 0:
                sample_song = db['songs'].find_one()
                print("\n[*] Sample Song:")
                for key, value in list(sample_song.items())[:5]:
                    print("    " + key + ": " + str(value))
            print()
        
        # Check users collection
        if 'users' in collections:
            users_count = db['users'].count_documents({})
            print("[*] Users Collection: " + str(users_count) + " users")
        
        # Check sessions collection
        if 'sessions' in collections:
            sessions_count = db['sessions'].count_documents({})
            print("[*] Sessions Collection: " + str(sessions_count) + " sessions")
        
        # Check ratings collection
        if 'ratings' in collections:
            ratings_count = db['ratings'].count_documents({})
            print("[*] Ratings Collection: " + str(ratings_count) + " ratings")
        
        print("\n" + "="*60)
        print("[OK] All Tests Passed! MongoDB is Ready!")
        print("="*60 + "\n")
        
        return True
        
    except ServerSelectionTimeoutError as e:
        print("\n[ERROR] Connection Timeout Error:")
        print("    " + str(e))
        print("\n    Possible causes:")
        print("    - MongoDB service is not running")
        print("    - MongoDB is not on port 27017")
        print("    - Firewall is blocking the connection")
        print("\n    Solution:")
        print("    - Check MongoDB service: Get-Service MongoDB")
        print("    - Start MongoDB if needed: Start-Service MongoDB")
        return False
        
    except ConnectionFailure as e:
        print("\n[ERROR] Connection Failed:")
        print("    " + str(e))
        print("\n    Possible causes:")
        print("    - Invalid connection string format")
        print("    - MongoDB credentials incorrect (if using authentication)")
        print("    - MongoDB not installed")
        return False
        
    except Exception as e:
        print("\n[ERROR] Unexpected Error:")
        print("    " + type(e).__name__ + ": " + str(e))
        return False
    
    finally:
        try:
            client.close()
            print("    (Connection closed)")
        except:
            pass


def test_environment():
    """Check environment variables"""
    
    print("\n" + "="*60)
    print("Environment Variables Check")
    print("="*60 + "\n")
    
    mongodb_uri = os.getenv("MONGODB_URI", "NOT SET (using default)")
    database_name = os.getenv("DATABASE_NAME", "NOT SET (using default: raga_rasa)")
    emotion_url = os.getenv("EMOTION_SERVICE_URL", "NOT SET")
    api_base = os.getenv("API_BASE_URL", "NOT SET")
    
    print("MONGODB_URI: " + str(mongodb_uri))
    print("DATABASE_NAME: " + str(database_name))
    print("EMOTION_SERVICE_URL: " + str(emotion_url))
    print("API_BASE_URL: " + str(api_base))
    print()


if __name__ == "__main__":
    print("\n")
    
    # Load .env file
    load_env()
    
    # Check environment
    test_environment()
    
    # Test MongoDB connection
    success = test_mongodb_connection()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
