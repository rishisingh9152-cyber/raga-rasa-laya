import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.dropbox_service import init_dropbox_service

# Initialize FastAPI app
app = FastAPI(
    title="Raga-Rasa Soul API",
    description="Music therapy with emotion detection",
    version="1.0.0"
)

# Initialize services
init_dropbox_service()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routes
try:
    from app.routes import songs_routes, song_management_routes, admin_routes
    app.include_router(songs_routes.router)
    app.include_router(song_management_routes.router)
    app.include_router(admin_routes.router)
except ImportError as e:
    print(f"Warning: Could not import routes: {e}")

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
