
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path
from uuid import uuid4

from .pdf_processor import extract_pdf_text
from .chunker import chunk_pages
from .embeddings import generate_embeddings
from .vector_store import store_chunks
from .workflow import run_workflow
from typing import Annotated
from fastapi.openapi.utils import get_openapi


# Create FastAPI application
app = FastAPI(
    title="PDF Retriever",
    description="A RAG-based PDF Question Answering Application",
    version="1.0.0"
)


# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# Temporary upload status registry
upload_status = {}


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


# Check upload status using document ID
@app.get("/upload/{document_id}/status")
def get_upload_status(document_id: str):

    if document_id not in upload_status:
        raise HTTPException(
            status_code=404,
            detail="Document ID not found"
        )

    return {
        "document_id": document_id,
        "filename": upload_status[document_id]["filename"],
        "status": upload_status[document_id]["status"]
    }


# Process an individual PDF
async def process_pdf(file: UploadFile):

    safe_filename = Path(file.filename or "").name
    document_id = str(uuid4())

    # Register upload as processing
    upload_status[document_id] = {
        "filename": safe_filename,
        "status": "processing"
    }

    try:
        # Validate PDF extension
        if not safe_filename or Path(safe_filename).suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are allowed")

        # Read uploaded file
        content = await file.read()

        # Validate PDF content
        if not content.startswith(b"%PDF-"):
            raise ValueError("Invalid PDF file")

        # Save PDF using unique document ID
        stored_filename = f"{document_id}_{safe_filename}"
        file_path = UPLOAD_DIR / stored_filename
        file_path.write_bytes(content)

        # Extract text
        pages = extract_pdf_text(str(file_path))

        # Generate chunks
        chunks = chunk_pages(pages, safe_filename)

        if not chunks:
            raise ValueError("No readable text found in the PDF")

        # Generate embeddings
        embeddings = generate_embeddings(chunks)

        # Store in ChromaDB with unique document ID
        total_records = store_chunks(
            chunks,
            embeddings,
            document_id
        )

        # Update upload status
        upload_status[document_id]["status"] = "completed"

        return {
            "document_id": document_id,
            "filename": safe_filename,
            "status": "completed",
            "total_pages": len(pages),
            "total_chunks": len(chunks),
            "stored_records": total_records
        }

    except Exception as e:

        # Update upload status if processing fails
        upload_status[document_id]["status"] = "failed"

        return {
            "document_id": document_id,
            "filename": safe_filename,
            "status": "failed",
            "error": str(e)
        }

    finally:
        await file.close()


# Multiple PDF Upload and Processing endpoint
@app.post("/upload")
async def upload_pdfs(
    files: Annotated[list[UploadFile], File(description="Select multiple PDF files")]
):

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Please upload at least one PDF file"
        )

    results = []

    # Process each PDF independently
    for file in files:

        result = await process_pdf(file)
        results.append(result)

    # Calculate upload statistics
    completed_count = sum(
        1 for result in results
        if result["status"] == "completed"
    )

    failed_count = sum(
        1 for result in results
        if result["status"] == "failed"
    )

    return {
        "message": "PDF upload processing finished",
        "total_files": len(files),
        "completed": completed_count,
        "failed": failed_count,
        "results": results
    }


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

# Fix Swagger UI file-upload rendering for OpenAPI 3.1
def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )

    def fix_file_schema(schema):

        if isinstance(schema, dict):

            if schema.get("contentMediaType") == "application/octet-stream":
                schema.pop("contentMediaType")
                schema["format"] = "binary"

            for value in schema.values():
                fix_file_schema(value)

        elif isinstance(schema, list):

            for item in schema:
                fix_file_schema(item)

    fix_file_schema(openapi_schema)

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi

