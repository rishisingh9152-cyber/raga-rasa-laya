import random
from app.database import songs_collection


class RecommendationService:

    # ----------------------------
    # 🎯 EMOTION → RASS (FINAL)
    # ----------------------------
    @staticmethod
    def map_emotion_to_rass(emotion: str) -> str:
        if not emotion:
            return "shaant"

        emotion = emotion.lower().strip()

        mapping = {
            "sad": "shringar",
            "angry": "shaant",
            "happy": "shringar",
            "brave": "veer",
            "bravery": "veer"
        }

        return mapping.get(emotion, "shaant")

    # ----------------------------
    # TOTAL INTERACTIONS (OPTIMIZED)
    # ----------------------------
    @staticmethod
    def get_total_interactions():
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$num_users"}
                }
            }
        ]

        result = list(songs_collection.aggregate(pipeline))

        return result[0]["total"] if result else 0

    # ----------------------------
    # 🎯 SCORING FUNCTION
    # ----------------------------
    @staticmethod
    def calculate_score(song):
        rating = float(song.get("avg_rating", 0))
        users = int(song.get("num_users", 0))

        # Normalize users to avoid domination
        normalized_users = users / 100 if users else 0

        return (0.7 * rating) + (0.3 * normalized_users)

    # ----------------------------
    # MAIN RECOMMENDATION FUNCTION
    # ----------------------------
    @staticmethod
    def get_recommendations(emotion: str, limit=5):

        mapped_rass = RecommendationService.map_emotion_to_rass(emotion)

        # Fetch songs
        songs = list(songs_collection.find({"rass": mapped_rass}))

        if not songs:
            return []

        # ----------------------------
        # 🎯 COLD START LOGIC
        # ----------------------------
        total_interactions = RecommendationService.get_total_interactions()

        if total_interactions < 100:
            selected = random.sample(songs, min(limit, len(songs)))

        else:
            # ----------------------------
            # 🎯 SMART RANKING
            # ----------------------------
            selected = sorted(
                songs,
                key=RecommendationService.calculate_score,
                reverse=True
            )[:limit]

        # ----------------------------
        # FORMAT RESPONSE (SAFE)
        # ----------------------------
        response = []
        for s in selected:
            response.append({
                "song_name": s.get("song_name", "Unknown"),
                "rass": s.get("rass", "unknown"),
                "file_path": s.get("file_path", ""),
                "avg_rating": float(s.get("avg_rating", 0)),
                "num_users": int(s.get("num_users", 0))
            })

        return response