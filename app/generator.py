
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
    You are a helpful PDF question-answering assistant.

    Answer the question using ONLY the context provided below.

    If the answer is not available in the context,
    say that the information is not available in the uploaded PDF.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)

    return response.content
