"""
Emotion Recognition Service using HSEmotion
Detects emotions from images and returns predictions
"""

import os
import base64
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import HSEmotion model
try:
    from hsemotion.facial_emotions import HSEmotionRecognizer
    model_name = "enet_b0_8_best_afew"
    device = "cpu"  # Use CPU for compatibility
    fer = HSEmotionRecognizer(model_name=model_name, device=device)
    MODEL_LOADED = True
except Exception as e:
    print(f"⚠️ Warning: Could not load HSEmotion model: {e}")
    MODEL_LOADED = False

app = Flask(__name__)
CORS(app)

# ==================== HELPER FUNCTIONS ====================

def decode_image(image_base64):
    """Decode base64 image to numpy array"""
    try:
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        image_np = np.array(image)
        
        # Convert RGB to BGR for OpenCV if needed
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        return image_np
    except Exception as e:
        return None, str(e)

def detect_emotion_hsemotion(image_np):
    """Detect emotion using HSEmotion model"""
    if not MODEL_LOADED:
        return None, "Model not loaded"
    
    try:
        # HSEmotion expects BGR image
        # Run prediction
        emotions, scores = fer.predict_emotions(image_np, logits=True)
        
        if emotions is None or len(emotions) == 0:
            return None, "No face detected"
        
        # Get dominant emotion for first detected face
        emotion = emotions[0]
        confidence = float(scores[0].max())
        
        return {
            "raw_dominant": emotion.lower(),
            "dominant": emotion.lower(),
            "emotion": emotion.lower(),
            "confidence": confidence,
            "all_emotions": {
                "angry": float(scores[0][0]) if len(scores[0]) > 0 else 0,
                "disgust": float(scores[0][1]) if len(scores[0]) > 1 else 0,
                "fear": float(scores[0][2]) if len(scores[0]) > 2 else 0,
                "happy": float(scores[0][3]) if len(scores[0]) > 3 else 0,
                "neutral": float(scores[0][4]) if len(scores[0]) > 4 else 0,
                "sad": float(scores[0][5]) if len(scores[0]) > 5 else 0,
                "surprise": float(scores[0][6]) if len(scores[0]) > 6 else 0,
            }
        }, None
    except Exception as e:
        return None, str(e)

# ==================== ROUTES ====================

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "emotion-recognition",
        "model_loaded": MODEL_LOADED
    }), 200

@app.route("/detect", methods=["POST"])
def detect_emotion():
    """
    Detect emotion from base64 encoded image
    
    Request JSON:
    {
        "image": "<base64_encoded_image>"
    }
    
    Response:
    {
        "raw_dominant": "happy",
        "dominant": "happy",
        "emotion": "happy",
        "confidence": 0.95,
        "all_emotions": {...}
    }
    """
    
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    if "image" not in data:
        return jsonify({"error": "Missing 'image' field"}), 400
    
    image_base64 = data["image"]
    
    # Decode image
    image_np = decode_image(image_base64)
    if image_np is None:
        return jsonify({"error": "Failed to decode image"}), 400
    
    # Detect emotion
    result, error = detect_emotion_hsemotion(image_np)
    
    if error:
        return jsonify({"error": error, "no_face_detected": True}), 400
    
    return jsonify(result), 200

@app.route("/", methods=["GET"])
def index():
    """Service info endpoint"""
    return jsonify({
        "service": "Emotion Recognition Service",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "POST /detect": "Detect emotion from base64 image",
            "GET /": "Service info"
        },
        "model": "HSEmotion (enet_b0_8_best_afew)",
        "emotions": ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
    }), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# ==================== MAIN ====================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    if not MODEL_LOADED:
        print("⚠️ Warning: HSEmotion model failed to load. Service will return errors.")
    
    print(f"🚀 Starting Emotion Recognition Service on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
