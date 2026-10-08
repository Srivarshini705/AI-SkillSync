from pydantic import BaseModel, Field


class ATSAnalyzeRequest(BaseModel):
    """
    Request for general ATS analysis.
    """

    resume_text: str = Field(
        ...,
        min_length=1,
        description="Plain text extracted from the resume.",
    )

    skills: list[str] = Field(
        default_factory=list,
        description="Skills extracted from the resume.",
    )

    experience: list[str] = Field(
        default_factory=list,
        description="Work experience entries.",
    )

    projects: list[str] = Field(
        default_factory=list,
        description="Project entries.",
    )

    education: list[str] = Field(
        default_factory=list,
        description="Education entries.",
    )

    achievements: list[str] = Field(
        default_factory=list,
        description="Achievement entries.",
    )


class ATSJobAnalyzeRequest(ATSAnalyzeRequest):
    """
    Request for ATS analysis against a specific job description.
    """

    job_description: str = Field(
        ...,
        min_length=1,
        description="Target job description.",
    )


class ATSComponentScores(BaseModel):
    """
    Individual ATS component scores.
    """

    skills: float = Field(ge=0, le=100)
    keywords: float = Field(ge=0, le=100)
    experience: float = Field(ge=0, le=100)
    projects: float = Field(ge=0, le=100)
    education: float = Field(ge=0, le=100)
    achievements: float = Field(ge=0, le=100)
    formatting: float = Field(ge=0, le=100)


class ATSAnalyzeResponse(BaseModel):
    """
    Structured ATS analysis returned by the API.
    """

    ats_score: float = Field(ge=0, le=100)

    component_scores: ATSComponentScores

    matched_keywords: list[str] = Field(
        default_factory=list
    )

    missing_keywords: list[str] = Field(
        default_factory=list
    )

    missing_skills: list[str] = Field(
        default_factory=list
    )

    suggestions: list[str] = Field(
        default_factory=list
    )

    summary: str = ""


class ATSJobAnalyzeResponse(ATSAnalyzeResponse):
    """
    Job-specific ATS response.

    Kept separate so the API contract can evolve independently
    from general ATS analysis.
    """

    job_match_summary: str = ""