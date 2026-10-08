# SkillSync AI 🎯

SkillSync AI is an AI-powered career assistant that helps students understand skill gaps, learn technical concepts, and generate resumes.

## 🚀 Features

### 1. 💬 Chat with SkillSync
An AI-powered technical chatbot that:
- Answers programming and software-related questions
- Uses RAG to retrieve relevant knowledge
- Uses ChromaDB for vector search
- Uses Groq LLM for responses
- Answers only what the user asks

### 2. 🎯 Skill Gap Analysis
Compare your current skills with the skills required for a target career.

Features:
- 80+ predefined technical skills
- Add custom skills manually
- Select a target career
- Calculate career skill match percentage
- Show matched skills
- Identify missing skills
- Generate a learning roadmap

### 3. 📄 Resume Generator
Generate a professional resume draft based on the information provided by the user.

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Groq
- ChromaDB
- FastEmbed
- RAG (Retrieval-Augmented Generation)
- Hugging Face Embeddings

## 📂 Project Structure

```text
SKILLSYNC-AI/
│
├── data/
│   └── skills.txt
│
├── chroma_db/
│
├── venv/
│
├── app.py
├── chatbot.py
├── ingest.py
├── skill_gap.py
├── .env
├── .gitignore
└── README.md