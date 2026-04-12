"""
Direct test of recommendation service
"""
import os
import sys

# Set environment variables
os.environ["MONGODB_URI"] = "mongodb+srv://Rishi123:Rishi_123@majorproject.lpwzhzc.mongodb.net/?appName=MajorProject"

# Add backend to path
sys.path.insert(0, "C:\\Users\\rishi\\raga-rasa-laya\\Backend")

from app.services.recommendation_service import RecommendationService

print("\n" + "="*70)
print("TESTING RECOMMENDATION SERVICE DIRECTLY")
print("="*70 + "\n")

# Test the service
print("Getting recommendations for emotion: 'happy'")
print("-" * 70)

results = RecommendationService.get_recommendations(emotion="happy", limit=5)

print(f"Number of results: {len(results)}\n")

if results:
    print("First recommendation:")
    first = results[0]
    for key, val in first.items():
        if isinstance(val, str) and len(val) > 100:
            print(f"  {key}: {val[:100]}...")
        else:
            print(f"  {key}: {val}")

print("\n" + "="*70 + "\n")
