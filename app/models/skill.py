from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)