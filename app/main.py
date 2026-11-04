
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path

from .pdf_processor import extract_pdf_text
from .chunker import chunk_pages
from .embeddings import generate_embeddings
from .vector_store import store_chunks
from .workflow import run_workflow


# Create FastAPI application
app = FastAPI(
    title="PDF Retriever",
    description="A RAG-based PDF Question Answering Application",
    version="1.0.0"
)


# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# Define request structure for questions
class QuestionRequest(BaseModel):
    question: str


# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to PDF Retriever Application!"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "Application is running successfully"
    }


# PDF Upload and Processing endpoint
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Validate PDF extension
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read uploaded file
    content = await file.read()

    # Validate PDF content
    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    try:
        # Save PDF
        safe_filename = Path(file.filename).name
        file_path = UPLOAD_DIR / safe_filename
        file_path.write_bytes(content)

        # Extract text
        pages = extract_pdf_text(str(file_path))

        # Generate chunks
        chunks = chunk_pages(pages, safe_filename)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF"
            )

        # Generate embeddings
        embeddings = generate_embeddings(chunks)

        # Store in ChromaDB
        total_records = store_chunks(chunks, embeddings)

        return {
            "message": "PDF uploaded and processed successfully",
            "filename": safe_filename,
            "total_pages": len(pages),
            "total_chunks": len(chunks),
            "stored_records": total_records
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(e)}"
        )


# Question and Answer endpoint
@app.post("/ask")
def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        # Execute LangGraph workflow
        result = run_workflow(request.question)

        return {
            "question": result["question"],
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(e)}"
        )
