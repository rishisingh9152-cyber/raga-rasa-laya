from fastapi import APIRouter, Query, HTTPException
from app.services.recommendation_service import RecommendationService

router = APIRouter()

VALID_EMOTIONS = ["sad", "happy", "angry", "brave"]


@router.get("/recommendations")
def get_recommendations(
    user_id: str = Query(default="default_user"),
    emotion: str = Query(...),
    limit: int = 5
):
    try:
        # ----------------------------
        # 🔥 NORMALIZE EMOTION
        # ----------------------------
        if not emotion:
            raise HTTPException(status_code=400, detail="Emotion is required")

        emotion = emotion.lower().strip()

        emotion_map = {
            "angry": "angry",
            "anger": "angry",
            "happy": "happy",
            "joy": "happy",
            "sad": "sad",
            "brave": "brave",
            "bravery": "brave"
        }

        emotion = emotion_map.get(emotion)

        if not emotion or emotion not in VALID_EMOTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid emotion. Choose from {VALID_EMOTIONS}"
            )

        # ----------------------------
        # 🎯 GET RECOMMENDATIONS
        # ----------------------------
        results = RecommendationService.get_recommendations(
            emotion=emotion,
            limit=limit
        )

        if not results:
            raise HTTPException(status_code=404, detail="No songs found")

        return {
            "status": "success",
            "user_id": user_id,
            "emotion": emotion,
            "count": len(results),
            "recommendations": results
        }

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))