from fastapi import FastAPI

from app.database.database import Base, engine
from app.models import user
from app.models import skill
from app.routes.auth import router as auth_router
from app.routes.skill import router as skill_router

Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI SkillSync Backend")

# Connect authentication routes
app.include_router(auth_router)
app.include_router(skill_router)


@app.get("/")
def home():
    return {
        "message": "AI SkillSync Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }