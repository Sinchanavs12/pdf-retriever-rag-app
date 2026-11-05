
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()


# Initialize the Groq language model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def generate_answer(question, context):

    prompt = f"""
You are an accurate PDF question-answering assistant.

Your task is to answer questions using ONLY the information
available in the retrieved PDF context.

IMPORTANT INSTRUCTIONS:

1. Read the entire context carefully before answering.

2. The context may contain information from multiple PDF files.
   Each section includes a source PDF filename and page number.

3. If the user asks multiple questions in one request,
   answer EACH question separately.

4. For every question:
   - Identify the relevant information in the context.
   - Use information from the appropriate PDF.
   - Do not mix unrelated information from different PDFs.
   - Include the source PDF filename and page number when possible.

5. If information for one question is available, answer it
   even if information for another question is missing.

6. If the context does not contain sufficient information
   to answer a particular question, clearly state:
   "This information was not found in the retrieved PDF context."

7. Do not invent facts or use outside knowledge.

8. Give clear, simple, and well-structured answers.

RETRIEVED PDF CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:

Answer each question separately using numbered sections.
"""

    response = llm.invoke(prompt)

    return response.content
