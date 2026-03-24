from fastapi import APIRouter, Body, HTTPException
from app.database import songs_collection
from bson import ObjectId

router = APIRouter()


@router.post("/songs/rate")
def rate_song(
    song_id: str = Body(...),
    rating: float = Body(...)
):
    try:
        # ----------------------------
        # ✅ VALIDATION
        # ----------------------------
        if rating < 1 or rating > 5:
            raise HTTPException(
                status_code=400,
                detail="Rating must be between 1 and 5"
            )

        # ----------------------------
        # ✅ FIND SONG
        # ----------------------------
        song = songs_collection.find_one({"_id": ObjectId(song_id)})

        if not song:
            raise HTTPException(status_code=404, detail="Song not found")

        # ----------------------------
        # ✅ GET OLD VALUES
        # ----------------------------
        ratings = song.get("ratings", {})

        old_avg = ratings.get("avg_rating", 0)
        old_users = ratings.get("num_users", 0)

        # ----------------------------
        # ✅ UPDATE FORMULA
        # ----------------------------
        new_users = old_users + 1
        new_avg = ((old_avg * old_users) + rating) / new_users

        # ----------------------------
        # ✅ UPDATE DB
        # ----------------------------
        songs_collection.update_one(
            {"_id": song["_id"]},
            {
                "$set": {
                    "ratings.avg_rating": round(new_avg, 2),
                    "ratings.num_users": new_users,
                    "is_new": False  # 🔥 IMPORTANT
                },
                "$inc": {
                    "num_users": 1  # 🔥 sync with recommendation exposure
                }
            }
        )

        return {
            "status": "success",
            "song_id": song_id,
            "new_avg_rating": round(new_avg, 2),
            "total_ratings": new_users
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))