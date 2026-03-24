import requests
import base64

EMOTION_API_URL = "http://127.0.0.1:5000/detect"


def get_emotion(image_bytes):
    try:
        # ----------------------------
        # ENCODE IMAGE
        # ----------------------------
        img_base64 = base64.b64encode(image_bytes).decode()

        # ----------------------------
        # CALL EMOTION SERVICE
        # ----------------------------
        res = requests.post(
            EMOTION_API_URL,
            json={"image": img_base64},
            timeout=5  # ⏱ prevents hanging
        )

        # ----------------------------
        # CHECK RESPONSE
        # ----------------------------
        if res.status_code != 200:
            return {
                "error": "Emotion service error",
                "status_code": res.status_code
            }

        data = res.json()

        # ----------------------------
        # VALIDATE OUTPUT
        # ----------------------------
        if "emotion" not in data:
            return {"error": "Invalid response from emotion service"}

        return data

    except requests.exceptions.ConnectionError:
        return {"error": "Emotion service not running"}

    except requests.exceptions.Timeout:
        return {"error": "Emotion service timeout"}

    except Exception as e:
        return {"error": str(e)}