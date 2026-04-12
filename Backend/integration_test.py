#!/usr/bin/env python3
"""
Integration Test Suite: Comprehensive testing of all system components.
Identifies and reports all integration issues.
"""

import sys
import json
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all imports work correctly."""
    print("\n" + "="*60)
    print("  TESTING IMPORTS")
    print("="*60)
    
    issues = []
    
    try:
        from app.main import app
        print("[OK] app.main imported successfully")
    except Exception as e:
        issues.append(f"app.main: {e}")
        print(f"[FAIL] app.main failed: {e}")
    
    try:
        from app.services.dropbox_service import DropboxService
        print("[OK] DropboxService imported")
    except Exception as e:
        issues.append(f"DropboxService: {e}")
        print(f"[FAIL] DropboxService failed: {e}")
    
    try:
        from app.services.song_management_service import SongManagementService
        print("[OK] SongManagementService imported")
    except Exception as e:
        issues.append(f"SongManagementService: {e}")
        print(f"[FAIL] SongManagementService failed: {e}")
    
    try:
        from app.services.dropbox_sync_service import DropboxSyncService
        print("[OK] DropboxSyncService imported")
    except Exception as e:
        issues.append(f"DropboxSyncService: {e}")
        print(f"[FAIL] DropboxSyncService failed: {e}")
    
    try:
        from app.routes import songs_routes
        print("[OK] songs_routes imported")
    except Exception as e:
        issues.append(f"songs_routes: {e}")
        print(f"[FAIL] songs_routes failed: {e}")
    
    try:
        from app.routes import song_management_routes
        print("[OK] song_management_routes imported")
    except Exception as e:
        issues.append(f"song_management_routes: {e}")
        print(f"[FAIL] song_management_routes failed: {e}")
    
    try:
        from app.routes import admin_routes
        print("[OK] admin_routes imported")
    except Exception as e:
        issues.append(f"admin_routes: {e}")
        print(f"[FAIL] admin_routes failed: {e}")
    
    try:
        from app.database import songs_collection
        print("[OK] database imported")
    except Exception as e:
        issues.append(f"database: {e}")
        print(f"[FAIL] database failed: {e}")
    
    return issues


def test_database():
    """Test database connectivity."""
    print("\n" + "="*60)
    print("  TESTING DATABASE")
    print("="*60)
    
    issues = []
    
    try:
        from app.database import songs_collection
        count = songs_collection.count_documents({})
        print(f"[OK] Database connected: {count} songs found")
    except Exception as e:
        issues.append(f"Database connection: {e}")
        print(f"[FAIL] Database connection failed: {e}")
        return issues
    
    try:
        from app.database import ratings_collection
        rating_count = ratings_collection.count_documents({})
        print(f"[OK] Ratings collection accessible: {rating_count} ratings")
    except Exception as e:
        issues.append(f"Ratings collection: {e}")
        print(f"[FAIL] Ratings collection failed: {e}")
    
    try:
        from app.database import sessions_collection
        session_count = sessions_collection.count_documents({})
        print(f"[OK] Sessions collection accessible: {session_count} sessions")
    except Exception as e:
        issues.append(f"Sessions collection: {e}")
        print(f"[FAIL] Sessions collection failed: {e}")
    
    return issues


def test_services():
    """Test all service operations."""
    print("\n" + "="*60)
    print("  TESTING SERVICES")
    print("="*60)
    
    issues = []
    
    try:
        from app.services.song_management_service import SongManagementService
        from app.database import songs_collection
        
        # Test fetching a song
        song = songs_collection.find_one({})
        if song:
            song_id = str(song['_id'])
            fetched = SongManagementService.get_song_by_id(song_id)
            if fetched:
                print(f"[OK] SongManagementService.get_song_by_id() works")
            else:
                issues.append("SongManagementService.get_song_by_id() returned None")
                print(f"[FAIL] get_song_by_id() returned None for {song_id}")
        else:
            print("[WARN] No songs in database to test")
    except Exception as e:
        issues.append(f"SongManagementService: {e}")
        print(f"[FAIL] SongManagementService failed: {e}")
    
    try:
        from app.services.dropbox_sync_service import DropboxSyncService
        
        # Test building URL
        url = DropboxSyncService.build_dropbox_download_url("/Shaant/test.mp3")
        if url and "dropbox" in url.lower():
            print(f"[OK] DropboxSyncService.build_dropbox_download_url() works")
        else:
            issues.append(f"build_dropbox_download_url() returned invalid URL: {url}")
            print(f"[FAIL] build_dropbox_download_url() returned: {url}")
    except Exception as e:
        issues.append(f"DropboxSyncService: {e}")
        print(f"[FAIL] DropboxSyncService failed: {e}")
    
    return issues


def test_routes():
    """Test route registration."""
    print("\n" + "="*60)
    print("  TESTING ROUTES")
    print("="*60)
    
    issues = []
    
    try:
        from app.main import app
        
        routes_found = {}
        for route in app.routes:
            path = getattr(route, 'path', 'unknown')
            methods = getattr(route, 'methods', set())
            if path not in routes_found:
                routes_found[path] = []
            routes_found[path].extend(methods)
        
        expected_routes = {
            '/api/songs/stream': ['GET'],
            '/api/songs/rass': ['GET'],
            '/api/songs/stats': ['GET'],
            '/api/songs/create': ['POST'],
            '/api/admin/sync/dropbox': ['POST'],
        }
        
        for expected_path, expected_methods in expected_routes.items():
            found = False
            for path in routes_found:
                if expected_path in path or path in expected_path:
                    found = True
                    print(f"[OK] Route {expected_path} registered")
                    break
            if not found:
                issues.append(f"Route {expected_path} not found")
                print(f"[FAIL] Route {expected_path} missing")
        
        print(f"[OK] Total routes registered: {len(routes_found)}")
        
    except Exception as e:
        issues.append(f"Route testing: {e}")
        print(f"[FAIL] Route testing failed: {e}")
    
    return issues


def test_api_models():
    """Test Pydantic models."""
    print("\n" + "="*60)
    print("  TESTING API MODELS")
    print("="*60)
    
    issues = []
    
    try:
        from app.routes.song_management_routes import SongCreate
        
        # Test model creation
        song_data = SongCreate(
            song_name="test.mp3",
            rass="shaant",
            file_path="/test/test.mp3"
        )
        print(f"[OK] SongCreate model works")
    except Exception as e:
        issues.append(f"SongCreate model: {e}")
        print(f"[FAIL] SongCreate model failed: {e}")
    
    try:
        from app.routes.admin_routes import DropboxSyncRequest
        
        # Test model creation
        sync_request = DropboxSyncRequest(
            dropbox_folder_path="/test/path"
        )
        print(f"[OK] DropboxSyncRequest model works")
    except Exception as e:
        issues.append(f"DropboxSyncRequest model: {e}")
        print(f"[FAIL] DropboxSyncRequest model failed: {e}")
    
    return issues


def test_config():
    """Test configuration."""
    print("\n" + "="*60)
    print("  TESTING CONFIGURATION")
    print("="*60)
    
    issues = []
    
    try:
        from app.config import (
            DROPBOX_FOLDER_ID,
            MONGODB_URL,
            DATABASE_NAME,
            API_BASE_URL
        )
        
        print(f"[OK] Config loaded:")
        print(f"  - Database: {DATABASE_NAME}")
        print(f"  - Dropbox Folder ID: {DROPBOX_FOLDER_ID}")
        print(f"  - API Base URL: {API_BASE_URL}")
    except ImportError:
        print("[WARN] config.py file not imported (optional)")
    except Exception as e:
        issues.append(f"Configuration: {e}")
        print(f"[FAIL] Configuration failed: {e}")
    
    return issues


def main():
    print("\n" + "="*60)
    print("  RAGA-RASA INTEGRATION TEST SUITE")
    print("="*60)
    
    all_issues = []
    
    # Run all tests
    all_issues.extend(test_imports())
    all_issues.extend(test_database())
    all_issues.extend(test_config())
    all_issues.extend(test_services())
    all_issues.extend(test_api_models())
    all_issues.extend(test_routes())
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    if all_issues:
        print(f"\n[ERROR] Found {len(all_issues)} issues:\n")
        for i, issue in enumerate(all_issues, 1):
            print(f"{i}. {issue}")
        print("\n[WARNING] Please fix the above issues before deployment\n")
        return 1
    else:
        print("\n[SUCCESS] All integration tests passed!")
        print("[SUCCESS] System is ready for deployment\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
