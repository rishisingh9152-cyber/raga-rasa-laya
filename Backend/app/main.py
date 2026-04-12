import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.dropbox_service import init_dropbox_service
from app.config import CORS_ORIGINS

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

# Initialize services
init_dropbox_service()

# Add CORS middleware with configuration-based origins
# Uses config for production, allows all in development
cors_origins = CORS_ORIGINS if CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
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

# Import and register additional routes if available
try:
    from app.routes import songs_routes, song_management_routes, admin_routes
    app.include_router(songs_routes.router)
    app.include_router(song_management_routes.router)
    app.include_router(admin_routes.router)
except ImportError:
    pass

try:
    from app.routes import psychometric, session, hybrid_recommendation
    app.include_router(psychometric.router)
    app.include_router(session.router)
    app.include_router(hybrid_recommendation.router)
except ImportError:
    pass

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
