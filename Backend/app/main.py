import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routes
from app.routes.recommendation import router as recommendation_router
from app.routes.emotion import router as emotion_router
from app.routes.rating import router as rating_router
from app.routes.songs import router as songs_router
from app.routes.test import router as test_router

# Initialize FastAPI app
app = FastAPI(
    title="Raga-Rasa Soul API",
    description="Music therapy with emotion detection",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(recommendation_router, tags=["recommendations"])
app.include_router(emotion_router, tags=["emotion"])
app.include_router(rating_router, tags=["ratings"])
app.include_router(songs_router, tags=["songs"])
app.include_router(test_router, tags=["test"])

# Health check endpoint
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "Raga-Rasa Soul API",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Raga-Rasa Soul API is running",
        "status": "ok"
    }

# Test endpoint
@app.get("/test")
async def test():
    return {"test": "success"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
