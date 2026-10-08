from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillResponse
from app.routes.auth import get_current_user


router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


# CREATE SKILL
@router.post("/", response_model=SkillResponse)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_skill = Skill(
        name=skill.name,
        level=skill.level,
        user_id=current_user["user_id"]
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


# GET ALL SKILLS OF LOGGED-IN USER
@router.get("/", response_model=list[SkillResponse])
def get_skills(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    skills = db.query(Skill).filter(
        Skill.user_id == current_user["user_id"]
    ).all()

    return skills


# DELETE SKILL
@router.delete("/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == current_user["user_id"]
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    db.delete(skill)
    db.commit()

    return {"message": "Skill deleted successfully"}


# UPDATE SKILL
@router.put("/{skill_id}", response_model=SkillResponse)
def update_skill(
    skill_id: int,
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == current_user["user_id"]
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    skill.name = skill_data.name
    skill.level = skill_data.level

    db.commit()
    db.refresh(skill)

    return skill