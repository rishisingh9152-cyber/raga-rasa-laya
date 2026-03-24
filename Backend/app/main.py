from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import songs
from app.routes import test, emotion, recommendation, rating

app = FastAPI()

# 🔥 MOVE THIS TO TOP (BEFORE ANYTHING ELSE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 👈 more reliable than "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(songs.router)
# 🔥 THEN MOUNT
app.mount(
    "/songs",
    StaticFiles(directory=r"C:\Users\rishi\OneDrive\Desktop\AI MUSIC PLAYER\Songs"),
    name="songs"
)

# 🔥 THEN ROUTES
app.include_router(test.router)
app.include_router(emotion.router)
app.include_router(recommendation.router)
app.include_router(rating.router)

@app.get("/")
def home():
    return {"message": "Backend is running"}