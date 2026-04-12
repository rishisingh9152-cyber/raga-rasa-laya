import requests
import base64
import os
import logging

logger = logging.getLogger(__name__)

# Render emotion service URL configuration
# Priority: Environment variable > Render default > Local fallback
RENDER_EMOTION_SERVICE = "https://raga-rasa-music.onrender.com/detect"
LOCAL_EMOTION_SERVICE = "http://127.0.0.1:5000/detect"

EMOTION_API_URL = os.getenv("EMOTION_SERVICE_URL", RENDER_EMOTION_SERVICE)

logger.info(f"Emotion Service URL configured: {EMOTION_API_URL}")


def get_emotion(image_bytes):
    """
    Send image to emotion recognition service for analysis.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        dict with emotion data or error message
        
    Expected Response:
        {
            "emotion": "happy",
            "confidence": 0.95,
            ...other fields
        }
    """
    try:
        # Encode image to base64
        img_base64 = base64.b64encode(image_bytes).decode()
        
        logger.debug(f"Sending image to emotion service: {EMOTION_API_URL}")

        # Call emotion service with timeout
        response = requests.post(
            EMOTION_API_URL,
            json={"image": img_base64},
            timeout=30  # 30 second timeout for Render service
        )
        
        # Check response status
        if response.status_code != 200:
            error_msg = f"Emotion service returned status {response.status_code}"
            logger.error(f"{error_msg}: {response.text}")
            return {
                "error": error_msg,
                "status_code": response.status_code
            }

        # Parse response
        data = response.json()
        logger.info(f"Emotion service response: {data}")
        
        return data

    except requests.exceptions.Timeout:
        error_msg = f"Emotion service timeout (30s) - {EMOTION_API_URL}"
        logger.error(error_msg)
        return {"error": error_msg}
    
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Cannot connect to emotion service - {EMOTION_API_URL}"
        logger.error(f"{error_msg}: {str(e)}")
        return {"error": error_msg}

    except requests.exceptions.RequestException as e:
        error_msg = f"Emotion service request error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}
    
    except Exception as e:
        error_msg = f"Unexpected error in emotion detection: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}