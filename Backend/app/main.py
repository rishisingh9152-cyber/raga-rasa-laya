import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.dropbox_service import init_dropbox_service
from app.config import CORS_ORIGINS

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

# Import and register routes
try:
    # Core routes (Priority 1)
    from app.routes import songs_routes, song_management_routes, admin_routes
    app.include_router(songs_routes.router)
    app.include_router(song_management_routes.router)
    app.include_router(admin_routes.router)
    
    # Feature routes (Priority 2)
    from app.routes import emotion, psychometric, session, recommendation, hybrid_recommendation
    app.include_router(emotion.router)
    app.include_router(psychometric.router)
    app.include_router(session.router)
    app.include_router(recommendation.router)
    app.include_router(hybrid_recommendation.router)
    
    # Optional routes (Priority 3)
    try:
        from app.routes import songs, rating
        app.include_router(songs.router)
        app.include_router(rating.router)
    except ImportError as e:
        print(f"Note: Optional routes not available: {e}")
        
except ImportError as e:
    print(f"Error: Could not import routes: {e}")

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
