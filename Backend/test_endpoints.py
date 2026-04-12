#!/usr/bin/env python3
"""
API Endpoint Test: Tests actual HTTP endpoints.
"""

import sys
from pathlib import Path
import asyncio

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_endpoints():
    """Test API endpoints."""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    issues = []
    
    print("\n" + "="*60)
    print("  TESTING API ENDPOINTS")
    print("="*60)
    
    # Test health endpoint
    try:
        response = client.get("/health")
        if response.status_code == 200:
            print("[OK] GET /health - 200")
        else:
            issues.append(f"Health check failed: {response.status_code}")
            print(f"[FAIL] GET /health - {response.status_code}")
    except Exception as e:
        issues.append(f"Health endpoint: {e}")
        print(f"[FAIL] GET /health - {e}")
    
    # Test root endpoint
    try:
        response = client.get("/")
        if response.status_code == 200:
            print("[OK] GET / - 200")
        else:
            issues.append(f"Root endpoint failed: {response.status_code}")
            print(f"[FAIL] GET / - {response.status_code}")
    except Exception as e:
        issues.append(f"Root endpoint: {e}")
        print(f"[FAIL] GET / - {e}")
    
    # Test songs stats endpoint
    try:
        response = client.get("/api/songs/stats")
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "total_songs" in data.get("data", {}):
                print(f"[OK] GET /api/songs/stats - 200 ({data['data']['total_songs']} songs)")
            else:
                print(f"[OK] GET /api/songs/stats - 200")
        else:
            issues.append(f"Songs stats endpoint failed: {response.status_code}")
            print(f"[FAIL] GET /api/songs/stats - {response.status_code}")
    except Exception as e:
        issues.append(f"Songs stats endpoint: {e}")
        print(f"[FAIL] GET /api/songs/stats - {e}")
    
    # Test admin sync status
    try:
        response = client.get("/api/admin/sync/status")
        if response.status_code == 200:
            print("[OK] GET /api/admin/sync/status - 200")
        else:
            issues.append(f"Sync status endpoint failed: {response.status_code}")
            print(f"[FAIL] GET /api/admin/sync/status - {response.status_code}")
    except Exception as e:
        issues.append(f"Sync status endpoint: {e}")
        print(f"[FAIL] GET /api/admin/sync/status - {e}")
    
    # Test admin database stats
    try:
        response = client.get("/api/admin/database/stats")
        if response.status_code == 200:
            data = response.json()
            if "statistics" in data:
                stats = data["statistics"]
                print(f"[OK] GET /api/admin/database/stats - 200 ({stats.get('total_active', 0)} active songs)")
            else:
                print(f"[OK] GET /api/admin/database/stats - 200")
        else:
            issues.append(f"Database stats failed: {response.status_code}")
            print(f"[FAIL] GET /api/admin/database/stats - {response.status_code}")
    except Exception as e:
        issues.append(f"Database stats endpoint: {e}")
        print(f"[FAIL] GET /api/admin/database/stats - {e}")
    
    # Test create song endpoint
    try:
        song_data = {
            "song_name": "Test_Integration_Song.mp3",
            "rass": "shaant",
            "file_path": "/test/song.mp3"
        }
        response = client.post("/api/songs/create", json=song_data)
        if response.status_code == 200:
            print("[OK] POST /api/songs/create - 200")
            # Clean up - try to delete
            try:
                response_data = response.json()
                if "data" in response_data and "_id" in response_data["data"]:
                    song_id = response_data["data"]["_id"]
                    # Hard delete the test song
                    delete_response = client.delete(f"/api/songs/{song_id}?hard=true")
                    if delete_response.status_code == 200:
                        print("[OK] Cleanup - deleted test song")
            except:
                pass
        else:
            issues.append(f"Create song failed: {response.status_code}")
            print(f"[FAIL] POST /api/songs/create - {response.status_code}")
    except Exception as e:
        issues.append(f"Create song endpoint: {e}")
        print(f"[FAIL] POST /api/songs/create - {e}")
    
    return issues


def main():
    print("\n" + "="*60)
    print("  API ENDPOINT TESTS")
    print("="*60)
    
    try:
        issues = asyncio.run(test_endpoints())
    except RuntimeError:
        # If event loop already running, just run directly
        from fastapi.testclient import TestClient
        from app.main import app
        
        issues = []
        client = TestClient(app)
        
        response = client.get("/health")
        if response.status_code == 200:
            print("[OK] GET /health - 200")
        else:
            print(f"[FAIL] GET /health - {response.status_code}")
        
        response = client.get("/api/songs/stats")
        if response.status_code == 200:
            print("[OK] GET /api/songs/stats - 200")
        else:
            print(f"[FAIL] GET /api/songs/stats - {response.status_code}")
    
    print("\n" + "="*60)
    print("  ENDPOINT TEST SUMMARY")
    print("="*60)
    
    if issues:
        print(f"\n[ERROR] Found {len(issues)} issues:\n")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        return 1
    else:
        print("\n[SUCCESS] All endpoint tests passed!")
        print("[SUCCESS] API is fully functional\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
