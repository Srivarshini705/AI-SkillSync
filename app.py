import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

from skill_gap import (
    ALL_SKILLS,
    CAREER_SKILLS,
    get_skill_gap,
    generate_roadmap,
    calculate_skill_match,
    get_matched_skills
)


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="SkillSync AI",
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
# CHROMA
# =========================================================

@st.cache_resource
def load_vectorstore():

    embeddings = load_embeddings()

    return Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )


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
# HEADER
# =========================================================

st.title("🎯 SkillSync AI")

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

    # Show previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )


    question = st.chat_input(
        "Ask SkillSync anything..."
    )


    if question:

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        with st.chat_message("user"):

            st.markdown(question)


        # Retrieve relevant knowledge
        documents = retriever.invoke(
            question
        )


        # Create context
        context = "\n\n".join(
            document.page_content
            for document in documents
        )


        # =================================================
        # CHAT PROMPT
        # =================================================

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


        response = llm.invoke(
            prompt
        )

        answer = response.content


        # Save assistant response
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


    # =====================================================
    # CURRENT SKILLS
    # =====================================================

    st.subheader("Your Current Skills")


    # -----------------------------------------------------
    # Option 1: Select from predefined skills
    # -----------------------------------------------------

    selected_skills = st.multiselect(
        "Select skills from the list",
        options=ALL_SKILLS,
        key="all_skills_selector",
        placeholder="Search and select skills..."
    )


    # -----------------------------------------------------
    # Option 2: Add skills manually
    # -----------------------------------------------------

    manual_skills = st.text_input(
        "Add other skills manually",
        placeholder="Example: React, TensorFlow, PyTorch"
    )


    # Convert manual input to list
    if manual_skills:

        manual_skill_list = [
            skill.strip()
            for skill in manual_skills.split(",")
            if skill.strip()
        ]

    else:

        manual_skill_list = []


    # -----------------------------------------------------
    # Combine both
    # -----------------------------------------------------

    current_skills = (
        selected_skills +
        manual_skill_list
    )


    # Remove duplicates
    current_skills = list(
        dict.fromkeys(current_skills)
    )


    # Save combined skills
    st.session_state.current_skills = current_skills


    # -----------------------------------------------------
    # Display count
    # -----------------------------------------------------

    st.caption(
        f"{len(ALL_SKILLS)} predefined skills available • "
        f"{len(current_skills)} total skills selected"
    )


    # -----------------------------------------------------
    # Display selected skills
    # -----------------------------------------------------

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


    # =====================================================
    # TARGET CAREER
    # =====================================================

    st.subheader("Target Career")

    skill_gap_role = st.selectbox(
        "Select your target career",
        sorted(
            CAREER_SKILLS.keys()
        )
    )


    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

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

            # =================================================
            # GET SKILL GAP
            # =================================================

            required_skills, missing_skills = get_skill_gap(
                current_skills,
                skill_gap_role
            )


            # =================================================
            # MATCH PERCENTAGE
            # =================================================

            match_percentage = calculate_skill_match(
                current_skills,
                skill_gap_role
            )


            # =================================================
            # MATCHED SKILLS
            # =================================================

            matched_skills = get_matched_skills(
                current_skills,
                skill_gap_role
            )


            # =================================================
            # SKILL MATCH
            # =================================================

            st.subheader("📊 Skill Match")

            st.metric(
                "Career Match",
                f"{match_percentage}%"
            )


            # =================================================
            # MATCHED SKILLS
            # =================================================

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


            # =================================================
            # SKILL GAPS
            # =================================================

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


            # =================================================
            # ROADMAP
            # =================================================

            st.subheader("🛣️ Learning Roadmap")

            roadmap = generate_roadmap(
                missing_skills
            )


            if roadmap:

                for step in roadmap:

                    st.write(
                        step
                    )

            else:

                st.success(
                    "No additional learning required."
                )


            # =================================================
            # REQUIRED SKILLS
            # =================================================

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


    # =====================================================
    # RESUME DETAILS
    # =====================================================

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


    # =====================================================
    # GENERATE RESUME
    # =====================================================

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


        # =================================================
        # DISPLAY RESUME
        # =================================================

        st.subheader(
            "Generated Resume"
        )

        st.markdown(
            resume
        )


        # =================================================
        # DOWNLOAD RESUME
        # =================================================

        st.download_button(
            label="⬇️ Download Resume",
            data=resume,
            file_name="SkillSync_Resume.md",
            mime="text/markdown"
        )