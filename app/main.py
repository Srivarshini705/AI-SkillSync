from fastapi import FastAPI

from app.api.ats_routes import router as ats_router
from app.api.resume_routes import router as resume_router


app = FastAPI(
    title="AI SkillSync - Resume & ATS AI Module",
    description="Member 3 Resume Creation and ATS Analysis Service",
    version="1.0.0",
)


app.include_router(ats_router)
app.include_router(resume_router)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "member3-resume-ats",
        "version": "1.0.0",
    }