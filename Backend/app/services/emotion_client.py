import requests
import base64

EMOTION_API_URL = "http://127.0.0.1:5000/detect"


def get_emotion(image_bytes):

    try:
        img_base64 = base64.b64encode(image_bytes).decode()

        response = requests.post(
            EMOTION_API_URL,
            json={"image": img_base64}
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}