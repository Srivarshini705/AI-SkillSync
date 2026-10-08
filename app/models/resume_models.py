from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ResumeData(BaseModel):
    """
    Structured representation of information extracted from a resume.
    """

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    summary: str | None = None

    education: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)