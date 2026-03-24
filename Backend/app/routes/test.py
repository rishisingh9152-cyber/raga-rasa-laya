from fastapi import APIRouter, UploadFile, File
from fastapi.concurrency import run_in_threadpool
import os
import shutil
import uuid
import traceback

from app.services.rass_service import RassService

router = APIRouter()

UPLOAD_DIR = "app/storage/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = [".wav", ".mp3"]


@router.post("/test-rass")
async def test_rass(file: UploadFile = File(...)):
    file_path = None
    try:
        # Validate file type
        if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            return {"error": "Invalid file type"}

        # Unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run ML model (non-blocking)
        result = await run_in_threadpool(
            RassService.classify_song, file_path
        )

        return {
            "status": "success",
            "rass": result["rass"],
            "features_preview": result["features"][:5]
        }

    except Exception as e:
        print(traceback.format_exc())
        return {"error": "Internal Server Error"}

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


@router.get("/test")
def test():
    return {"status": "working"}