# AI SkillSync — Member 3 Resume + ATS AI Module

## Overview

This module is the Resume + ATS AI component of the AI SkillSync career platform.

Member 3 is responsible for:

- Resume creation
- Resume PDF processing
- Resume text extraction
- Resume parsing
- ATS analysis
- Deterministic ATS scoring
- Keyword matching
- Missing skill detection
- ATS improvement suggestions
- Job-description-based resume matching

The module is implemented as a modular FastAPI service so that the other team members can integrate with it through clean JSON APIs.

---

## Architecture

`	ext
                    AI SkillSync
                         |
                  Member 3 Module
                         |
          +--------------+--------------+
          |                             |
     Resume APIs                    ATS APIs
          |                             |
    +-----+------+                +-----+------+
    |            |                |            |
 Create       Upload          General ATS   Job ATS
 Resume       PDF             Analysis      Matching
    |            |                |            |
    |        PyPDF Extraction      |            |
    |            |                |            |
    |       Resume Parser          |            |
    |            |                |            |
    +------------+----------------+------------+
                         |
                  ATS Analyzer
                         |
              +----------+----------+
              |                     |
       Deterministic Python       Groq LLM
          calculations         semantic analysis
              |                     |
              +----------+----------+
                         |
                  Structured JSON
                         |
                 Other Team Modules
 
## Project Structure

`	ext
member3_resume_ats/
+-- app/
¦   +-- main.py
¦   +-- api/
¦   ¦   +-- resume_routes.py
¦   ¦   +-- ats_routes.py
¦   +-- services/
¦   ¦   +-- pdf_service.py
¦   ¦   +-- resume_parser.py
¦   ¦   +-- resume_generator.py
¦   ¦   +-- ats_analyzer.py
¦   ¦   +-- llm_service.py
¦   +-- models/
¦   ¦   +-- resume_models.py
¦   ¦   +-- ats_models.py
¦   +-- prompts/
¦   ¦   +-- resume_prompts.py
¦   ¦   +-- ats_prompts.py
¦   +-- utils/
¦       +-- validators.py
+-- tests/
¦   +-- test_api.py
¦   +-- test_pdf.py
¦   +-- test_parser.py
¦   +-- test_ats.py
¦   +-- test_groq.py
+-- uploads/
+-- .env
+-- .env.example
+-- .gitignore
+-- requirements.txt
+-- README.md
Technology Stack
- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- PyPDF
- Groq API
- python-dotenv
- pytest
- HTTPX
API Endpoints
Health Check
GET /api/health

Create Resume
POST /api/resume/create
Content-Type: application/json

Accepts structured resume information and uses the Groq LLM service to improve the resume content.
Upload Resume
POST /api/resume/upload
Content-Type: multipart/form-data

Accepts a PDF resume.
Processing:
PDF
 ?
Validation
 ?
PyPDF text extraction
 ?
Resume parser
 ?
ResumeData

The temporary PDF is deleted after processing.
General ATS Analysis
POST /api/ats/analyze
Content-Type: application/json

Performs:
- ATS scoring
- Keyword matching
- Missing skill detection
- Semantic analysis
- ATS suggestions
Job-Specific ATS Analysis
POST /api/ats/analyze-job
Content-Type: application/json

Accepts resume information plus a job description.
Returns:
- ATS score
- Component scores
- Matched keywords
- Missing keywords
- Missing skills
- Suggestions
- Job match summary
ATS Scoring
Component    Weight
Skills    20%
Keywords    20%
Experience    15%
Projects    15%
Education    10%
Achievements    10%
Formatting    10%
Total    100%


Python performs deterministic scoring while Groq provides semantic analysis.
Security
The module includes:
- PDF-only validation
- Maximum upload-size validation
- PDF signature validation
- UUID-based temporary filenames
- Temporary file cleanup
- Pydantic validation
- Server-side Groq API key handling
- .env excluded from Git
Never expose the Groq API key to the frontend.
Testing
Run:
python -m pytest

The test suite covers:
- API endpoints
- PDF extraction
- Resume parsing
- ATS scoring
- Groq integration
- Invalid PDF handling
- Upload validation
Team Integration
Other team members can call:
POST /api/resume/create
POST /api/resume/upload
POST /api/ats/analyze
POST /api/ats/analyze-job

Recommended flow:
React Frontend
      |
      v
Main FastAPI Backend
      |
      v
Member 3 Resume + ATS Service
      |
      +---- Resume APIs
      |
      +---- ATS APIs
      |
      +---- Groq

Module Boundary
Member 3 does NOT implement:
- React frontend
- Authentication
- Jobs database
- Internships database
- RAG/ChromaDB
- Skill-gap roadmap
- Chatbot UI
- Mock interview/test system
Development Rules
- Keep API routes thin.
- Keep business logic inside services/.
- Keep schemas inside models/.
- Keep prompts inside prompts/.
- Never hard-code API keys.
- Never commit .env.
- Keep the module independently testable.
License
This module is developed as part of the AI SkillSync academic project.
