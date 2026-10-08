from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings


# Load environment variables
load_dotenv()


# Load embeddings
embeddings = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# Load ChromaDB
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# Load Groq
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


print("SkillSync Chatbot")
print("Type 'exit' to stop.")


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break


    # Retrieve relevant knowledge
    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )


    # Prompt
    prompt = f"""
You are SkillSync, a beginner-friendly technical skills assistant.

Your MOST IMPORTANT RULE:

ANSWER ONLY WHAT THE USER ASKED.

Do NOT automatically add extra sections.

For example:

User: "Explain SQL"
Answer: Only explain SQL.

Do NOT add:
- Project ideas
- Certifications
- Roadmaps
- Interview questions
- Career advice

unless the user specifically asks for them.

--------------------------------------------

FOLLOW THE USER'S REQUEST EXACTLY:

1. If the user asks for an explanation:
   Give only the explanation.

2. If the user asks for project ideas:
   Give only project ideas related to the requested topic.

3. If the user asks about certifications:
   Give only relevant certifications or certificate types.

4. If the user asks for a roadmap:
   Give only the roadmap.

5. If the user asks for interview questions:
   Give only interview questions.

6. If the user asks for code:
   Give only the relevant code and a short explanation if necessary.

7. If the user asks for a comparison:
   Compare only the requested topics.

8. If the user asks for multiple things:
   Answer all the requested things, but nothing extra.

9. If the user asks a follow-up question:
   Answer only that follow-up question.

--------------------------------------------

ANSWER STYLE:

- Keep explanations beginner-friendly.
- Use simple language.
- Give examples when useful.
- Do not unnecessarily make answers very long.
- Do not introduce unrelated technologies.
- Do not introduce unrelated programming languages.
- Do not introduce unrelated career roles.
- Do not add unnecessary advice.
- Do not invent information.

Use the knowledge base as the main source.

If the knowledge base does not contain enough information to answer,
say:

"I do not have enough information in my knowledge base to answer that."

--------------------------------------------

KNOWLEDGE BASE:

{context}

--------------------------------------------

USER QUESTION:

{question}
"""


    # Generate answer
    response = llm.invoke(prompt)


    # Display answer
    print("\nSkillSync:", response.content)