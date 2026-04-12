"""
Configuration settings for the RagaRasa Music Therapy application.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dropbox Configuration
DROPBOX_FOLDER_ID = "2je1qltlw5zuhosbd96zf"
DROPBOX_SHARED_FOLDER_URL = "https://www.dropbox.com/scl/fo/2je1qltlw5zuhosbd96zf/"
DROPBOX_STREAMING_ENABLED = True

# Data files
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DROPBOX_SONGS_MAPPING_PATH = str(DATA_DIR / "dropbox_songs_mapping.json")

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "ai_music"
SONGS_COLLECTION = "songs"

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://raga-rasa-music-52.vercel.app",
]

# Feature Flags
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": True,
        }
    }
}
