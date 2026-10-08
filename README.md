# AI-SKILLSYNC

AI-SKILLSYNC is an AI-powered career assistant that helps students understand their skill gaps, learn technical concepts, and generate resumes.

## 🚀 Live Demo

https://ai-skillsync-puswk6jngmxwcfa9frj4ty.streamlit.app/

## 💻 GitHub Repository

https://github.com/Renuka2338/AI-SKILLSYNC

## ✨ Features

### 💬 Chat with SkillSync
- AI-powered technical chatbot
- Uses RAG to retrieve relevant knowledge
- Provides answers based only on the user's question
- Supports programming, web, API, database, cloud and software concepts

### 🎯 Skill Gap Analysis
- Select current technical skills
- Choose a target career role
- Calculates skill match
- Identifies missing skills
- Generates a learning roadmap

### 📄 Resume Generator
- Enter education, skills, projects and certifications
- Generate a professional resume using AI
- Download the generated resume

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- ChromaDB
- FastEmbed
- Groq LLM
- Retrieval-Augmented Generation (RAG)

## 🧠 RAG Workflow

User Question  
↓  
LangChain  
↓  
ChromaDB Retrieval  
↓  
Relevant Knowledge  
↓  
Groq LLM  
↓  
AI Response

## 📁 Project Structure

```text
AI-SKILLSYNC/
│
├── data/
│   └── skills.txt
│
├── chroma_db/
├── app.py
├── chatbot.py
├── ingest.py
├── skill_gap.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md