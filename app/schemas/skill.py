from pydantic import BaseModel


class SkillCreate(BaseModel):
    name: str
    level: str


class SkillResponse(BaseModel):
    id: int
    name: str
    level: str
    user_id: int

    class Config:
        from_attributes = True