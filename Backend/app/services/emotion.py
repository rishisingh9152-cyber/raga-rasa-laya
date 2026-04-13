"""
Emotion detection service - lazy-loaded to avoid cv2 import errors in headless environments.
"""

import logging

logger = logging.getLogger(__name__)


def get_emotion_detector():
    """
    Lazy-load emotion detector.
    
    Returns the emotion detection function that will be called when needed.
    cv2 is only imported when this function is actually called, not at module load time.
    
    This pattern ensures the app can start in headless environments (containers)
    without libGL.so.1 errors.
    """
    def detect_emotion_from_image(image_bytes):
        """
        Detect emotion from image bytes.
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            dict: Emotion detection result
        """
        try:
            # cv2 is imported here (inside the function), not at module level
            # This ensures it only loads when emotion detection is actually needed
            import cv2
            import numpy as np
            
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return {"error": "Invalid image data"}
            
            # Convert to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Placeholder emotion detection
            # In production, use hsemotion, deepface, or fer library
            # For now, return a simple detection based on brightness
            brightness = np.mean(img_rgb)
            
            if brightness > 150:
                emotion = "happy"
            elif brightness < 80:
                emotion = "sad"
            else:
                emotion = "neutral"
            
            return {
                "emotion": emotion,
                "confidence": 0.75,
                "raw_dominant": emotion
            }
            
        except ImportError as e:
            logger.error(f"Failed to import cv2: {e}")
            return {"error": f"cv2 import failed: {str(e)}"}
        except Exception as e:
            logger.error(f"Emotion detection error: {e}")
            return {"error": f"Detection failed: {str(e)}"}
    
    return detect_emotion_from_image


# Create singleton instance
# NOTE: NOT initialized at module level to avoid cv2 import errors
_detector = None


def init_emotion_detector():
    """Initialize emotion detector on-demand."""
    global _detector
    if _detector is None:
        _detector = get_emotion_detector()
    return _detector


# DO NOT initialize at module level - causes libGL.so.1 errors in Docker
# _detector is initialized lazily when first needed
