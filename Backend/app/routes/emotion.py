import os
from datetime import datetime
from fastapi import APIRouter

# Try to import from emotion_client first (new pattern)
# Fall back to emotion service if it exists (backward compatibility)
try:
    from app.services.emotion_client import get_emotion
except ImportError:
    # Fallback for older deployments
    from app.services.emotion import get_emotion_detector
    get_emotion = lambda img: get_emotion_detector()(img)

from app.database import images_collection

router = APIRouter()

BASE_DIR = os.path.join("app", "storage", "images")


@router.get("/emotion/live")
def detect_from_camera():
    # Lazy-load cv2 to avoid import errors in headless environments
    import cv2

    # Initialize camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        return {"error": "Camera not accessible"}

    # Capture frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return {"error": "Failed to capture image"}

    # 🔥 Improve frame quality
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to bytes
    success, buffer = cv2.imencode(".jpg", frame)
    if not success:
        return {"error": "Image encoding failed"}

    image_bytes = buffer.tobytes()

    # 🔥 CALL EMOTION SERVICE
    result = get_emotion(image_bytes)

    print("\n======================")
    print("RAW RESPONSE:", result)
    print("======================\n")

    if not isinstance(result, dict):
        return {"error": "Invalid response from emotion service"}

    if "error" in result:
        return result

    # 🔥 HANDLE ALL POSSIBLE KEYS
    emotion = (
        result.get("raw_dominant")   # ✅ preferred
        or result.get("dominant")
        or result.get("emotion")
        or result.get("dominant_emotion")
        or result.get("label")
        or result.get("prediction")
        or "unknown"
    )

    # Normalize safely
    emotion = str(emotion).lower().strip()

    print("FINAL EMOTION:", emotion)

    # SAVE IMAGE
    folder = os.path.join(BASE_DIR, emotion)
    os.makedirs(folder, exist_ok=True)

    filename = f"{datetime.utcnow().timestamp()}.jpg"
    file_path = os.path.join(folder, filename)

    try:
        with open(file_path, "wb") as f:
            f.write(image_bytes)
    except Exception as e:
        return {"error": f"Failed to save image: {str(e)}"}

    # SAVE TO DB
    try:
        images_collection.insert_one({
            "user_id": "default_user",
            "emotion": emotion,
            "file_path": file_path,
            "timestamp": datetime.utcnow()
        })
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}

    # RESPONSE
    return {
        "emotion": emotion,
        "image_path": file_path
    }