import os

import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from skill_gap import (
    ALL_SKILLS,
    CAREER_SKILLS,
    get_skill_gap,
    generate_roadmap,
    calculate_skill_match,
    get_matched_skills
)

load_dotenv()

st.set_page_config(
    page_title="AI-SKILLSYNC",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# EMBEDDINGS
# =========================================================

@st.cache_resource
def load_embeddings():
    return FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )


# =========================================================
# CREATE CHROMADB IF IT DOES NOT EXIST
# =========================================================

@st.cache_resource
def load_vectorstore():

    embeddings = load_embeddings()

    chroma_path = "chroma_db"

    # If ChromaDB already exists
    if os.path.exists(chroma_path):

        return Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings
        )

    # Create ChromaDB from skills.txt
    loader = TextLoader(
        "data/skills.txt",
        encoding="utf-8"
    )

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=chroma_path
    )

    return vectorstore


vectorstore = load_vectorstore()


# =========================================================
# RETRIEVER
# =========================================================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# =========================================================
# GROQ
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_skills" not in st.session_state:
    st.session_state.current_skills = []


# =========================================================
# TITLE
# =========================================================

st.title("🎯 AI-SKILLSYNC")

st.write(
    "AI-powered skill gap analysis, technical chatbot "
    "and resume generator."
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Modules")

option = st.sidebar.radio(
    "Choose a module",
    [
        "💬 Chat with SkillSync",
        "🎯 Skill Gap Analysis",
        "📄 Resume Generator"
    ]
)


# =========================================================
# CLEAR CHAT
# =========================================================

if st.sidebar.button(
    "🗑️ Clear Chat",
    use_container_width=True
):

    st.session_state.messages = []
    st.session_state.current_skills = []

    if "all_skills_selector" in st.session_state:
        st.session_state.all_skills_selector = []

    st.rerun()


# =========================================================
# CHAT WITH SKILLSYNC
# =========================================================

if option == "💬 Chat with SkillSync":

    st.header("💬 Chat with SkillSync")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    question = st.chat_input(
        "Ask SkillSync anything..."
    )


    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        with st.chat_message("user"):
            st.markdown(question)


        documents = retriever.invoke(question)


        context = "\n\n".join(
            document.page_content
            for document in documents
        )


        prompt = f"""
You are SkillSync, a beginner-friendly technical
skills assistant.

MOST IMPORTANT RULE:

ANSWER ONLY WHAT THE USER ASKED.

Do NOT automatically add unrelated information.

If the user asks for:

- Explanation → give only the explanation.
- Roadmap → give only the roadmap.
- Comparison → give only the comparison.
- Interview questions → give only interview questions.
- Code → give only the relevant code.
- Project ideas → give only project ideas.

Do NOT automatically add:

- Certifications
- Projects
- Roadmaps
- Interview questions
- Career advice

unless the user specifically asks.

Use the knowledge base when relevant.

KNOWLEDGE BASE:

{context}

USER QUESTION:

{question}
"""


        response = llm.invoke(prompt)

        answer = response.content


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


        with st.chat_message("assistant"):
            st.markdown(answer)


# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

elif option == "🎯 Skill Gap Analysis":

    st.header("🎯 Skill Gap Analysis")

    st.write(
        "Compare your current skills with the skills "
        "required for your target career."
    )


    st.subheader("Your Current Skills")


    selected_skills = st.multiselect(
        "Select skills from the list",

        options=ALL_SKILLS,

        key="all_skills_selector",

        placeholder="Search and select skills..."
    )


    manual_skills = st.text_input(
        "Add other skills manually",

        placeholder="Example: React, TensorFlow, PyTorch"
    )


    if manual_skills:

        manual_skill_list = [
            skill.strip()
            for skill in manual_skills.split(",")
            if skill.strip()
        ]

    else:

        manual_skill_list = []


    current_skills = (
        selected_skills +
        manual_skill_list
    )


    current_skills = list(
        dict.fromkeys(current_skills)
    )


    st.session_state.current_skills = current_skills


    st.caption(
        f"{len(ALL_SKILLS)} predefined skills available • "
        f"{len(current_skills)} total skills selected"
    )


    if current_skills:

        st.write("### Your Skills")

        for skill in current_skills:

            st.write(
                f"✅ {skill}"
            )

    else:

        st.info(
            "Select skills from the list or add skills manually."
        )


    st.subheader("Target Career")


    skill_gap_role = st.selectbox(
        "Select your target career",
        sorted(CAREER_SKILLS.keys())
    )


    analyze = st.button(
        "🔍 Analyze Skill Gap",
        use_container_width=True
    )


    if analyze:

        if not current_skills:

            st.warning(
                "Please select or enter at least one skill."
            )

        else:

            required_skills, missing_skills = get_skill_gap(
                current_skills,
                skill_gap_role
            )


            match_percentage = calculate_skill_match(
                current_skills,
                skill_gap_role
            )


            matched_skills = get_matched_skills(
                current_skills,
                skill_gap_role
            )


            st.subheader("📊 Skill Match")

            st.metric(
                "Career Match",
                f"{match_percentage}%"
            )


            st.subheader("✅ Matched Skills")


            if matched_skills:

                for skill in matched_skills:

                    st.write(
                        f"✅ {skill}"
                    )

            else:

                st.info(
                    "No required skills matched yet."
                )


            st.subheader("❌ Skill Gaps")


            if missing_skills:

                for skill in missing_skills:

                    st.write(
                        f"❌ {skill}"
                    )

            else:

                st.success(
                    "You have all required skills for this role!"
                )


            st.subheader("🛣️ Learning Roadmap")


            roadmap = generate_roadmap(
                missing_skills
            )


            if roadmap:

                for step in roadmap:

                    st.write(step)

            else:

                st.success(
                    "No additional learning required."
                )


            with st.expander(
                "📋 View Required Skills"
            ):

                for skill in required_skills:

                    st.write(
                        f"• {skill}"
                    )


# =========================================================
# RESUME GENERATOR
# =========================================================

elif option == "📄 Resume Generator":

    st.header("📄 Resume Generator")

    st.write(
        "Enter your information to generate a resume draft."
    )


    name = st.text_input(
        "Full Name"
    )


    contact = st.text_input(
        "Contact Information"
    )


    education = st.text_area(
        "Education"
    )


    technical_skills = st.text_area(
        "Technical Skills"
    )


    projects = st.text_area(
        "Projects"
    )


    certifications = st.text_area(
        "Certifications"
    )


    experience = st.text_area(
        "Experience"
    )


    achievements = st.text_area(
        "Achievements"
    )


    target_role = st.text_input(
        "Target Role"
    )


    additional_requirements = st.text_area(
        "Additional Requirements"
    )


    if st.button(
        "Generate Resume",
        use_container_width=True
    ):

        resume_prompt = f"""
Create a professional one-page resume
using ONLY the information provided below.

Do not invent information.

NAME:
{name}

CONTACT:
{contact}

EDUCATION:
{education}

TECHNICAL SKILLS:
{technical_skills}

PROJECTS:
{projects}

CERTIFICATIONS:
{certifications}

EXPERIENCE:
{experience}

ACHIEVEMENTS:
{achievements}

TARGET ROLE:
{target_role}

ADDITIONAL REQUIREMENTS:
{additional_requirements}
"""


        response = llm.invoke(
            resume_prompt
        )


        resume = response.content


        st.subheader(
            "Generated Resume"
        )


        st.markdown(resume)


        st.download_button(
            label="⬇️ Download Resume",

            data=resume,

            file_name="SkillSync_Resume.md",

            mime="text/markdown"
        )