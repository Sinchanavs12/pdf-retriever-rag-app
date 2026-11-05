# PDF Retriever – RAG-Based Question Answering Application

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content. The application retrieves relevant information from uploaded documents and uses a Large Language Model (LLM) to generate context-based answers with source references.

## Project Overview

The PDF Retriever application combines document processing, semantic search, vector storage, and LLM-based answer generation.

Users can:
- Upload PDF documents through a REST API.
- Extract text from PDF pages.
- Split extracted text into smaller chunks.
- Generate vector embeddings for the chunks.
- Store embeddings in ChromaDB.
- Ask natural-language questions about the documents.
- Receive generated answers with source document and page references.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API development |
| PyPDF | PDF text extraction |
| LangChain | Text splitting and embedding integration |
| Sentence Transformers | Text embedding generation |
| ChromaDB | Vector database and semantic retrieval |
| Groq | LLM-based answer generation |
| LangGraph | Workflow orchestration |
| Uvicorn | ASGI application server |

## Application Architecture

The application has two main workflows.

### 1. PDF Upload and Processing

1. User uploads a PDF through the `/upload` endpoint.
2. FastAPI validates and saves the PDF.
3. PyPDF extracts text page by page.
4. LangChain splits the extracted text into chunks.
5. Sentence Transformers generates embeddings.
6. ChromaDB stores the chunks, embeddings, and metadata.

### 2. Question Answering

1. User submits a question through the `/ask` endpoint.
2. LangGraph executes the retrieval node.
3. ChromaDB retrieves the most relevant chunks using semantic similarity.
4. Retrieved text is passed as context to the generation node.
5. The Groq-hosted LLM generates an answer based on the retrieved context.
6. The API returns the answer along with source document and page references.

### Workflow Diagram

```text
                 PDF Upload
                     |
                     v
              PDF Text Extraction
                     |
                     v
                 Chunking
                     |
                     v
             Embedding Generation
                     |
                     v
                 ChromaDB
                     |
                     |
User Question ------+
       |
       v
  LangGraph Workflow
       |
       v
  Retrieve Node
       |
       v
  Relevant Context
       |
       v
  Generate Node
       |
       v
    Groq LLM
       |
       v
 Answer + Source References
```

## Project Structure

```text
pdf-retriever-rag-app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── pdf_processor.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── generator.py
│   ├── graph_state.py
│   ├── nodes.py
│   ├── workflow.py
│   │
│   └── test_*.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Git
- A Groq API key

### 1. Clone the repository

```bash
git clone https://github.com/Sinchanavs12/pdf-retriever-rag-app.git
cd pdf-retriever-rag-app
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your own API key. Never commit your `.env` file to GitHub.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The application will run at:

`http://127.0.0.1:8000`

## API Endpoints

The application provides the following REST API endpoints.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Application health check |
| POST | `/upload` | Upload and process a PDF |
| POST | `/ask` | Ask a question about uploaded PDFs |

### API Testing with Swagger UI

Open:

`http://127.0.0.1:8000/docs`

Use Swagger UI to upload PDF files and submit questions.

Example question request:

```json
{
  "question": "What is symmetric encryption?"
}
```

Example response:

```json
{
  "question": "What is symmetric encryption?",
  "answer": "Symmetric encryption uses the same secret key for encryption and decryption.",
  "sources": [
    {
      "source": "CNS-module-1.pdf",
      "page_number": 4
    }
  ]
}
```

The generated answer and page references depend on the uploaded document and retrieved context.

## Implementation and Testing

The application components were developed and tested independently before integration.

The following components have been tested:

- PDF text extraction
- Text chunking
- Embedding generation
- ChromaDB vector storage
- Semantic retrieval
- LLM answer generation
- LangGraph nodes and workflow
- FastAPI PDF upload
- FastAPI question-answering endpoint

End-to-end testing was performed through Swagger UI.

## Daily Development Progress

### November 5, 2026 – Multi-PDF Support and Retrieval Improvements

The following enhancements were implemented and tested:

**1. Unique Document ID Generation**
- Generated a unique UUID for every uploaded PDF.
- Each document can be identified and tracked independently.
- Added upload status tracking with three states:
  - `processing`
  - `completed`
  - `failed`
- Implemented a status-checking endpoint: `GET /upload/{document_id}/status`.

**2. Multiple PDF Upload Support**
- Updated the `/upload` endpoint to accept multiple PDF files in a single request.
- Each PDF is processed independently.
- Added PDF extension and file-signature validation.
- Processing continues even if one of the uploaded files fails.
- The API response provides the total number of files, successful uploads, failed uploads, and individual processing results.

**3. Multiple-Question Handling**
- Improved question processing to handle multiple questions submitted in a single request.
- Implemented question splitting using sentence-ending punctuation.
- Each question is retrieved separately before generating the response.

**4. Multi-PDF Retrieval and Source References**
- Updated document storage to associate chunks with their respective document IDs.
- Improved retrieved context formatting to include source PDF filenames and page numbers.
- Enabled retrieval across multiple uploaded PDFs stored in the shared ChromaDB collection.
- Improved answer generation instructions to answer multiple questions separately using the relevant PDF context.

**5. Testing and Validation**

Uploaded and tested three PDF documents together:

- `BCS714D_MODULE_1.pdf` – Big Data Analytics Module 1
- `BCS714D_MODULE_2.pdf` – Big Data Analytics Module 2 (Hadoop)
- `BCS714D_MODULE_3.pdf` – Big Data Analytics Module 3 (MongoDB)

Testing included:
- Uploading all three PDFs in a single API request.
- Verifying unique document IDs and individual upload statuses.
- Asking separate questions about each PDF.
- Asking multiple questions in a single request.
- Verifying that relevant information was retrieved from the correct PDF.
- Checking whether generated answers included source filenames and page references.

**Testing Result:** All three PDFs were uploaded successfully. Individual and combined question-answering tests returned relevant responses with source references.

**6. GitHub Update**
- Committed and pushed the latest changes to the `main` branch.
- Commit: `Add multi-PDF upload and improve RAG retrieval`

**Pending Enhancement:**
- Implement progressive LLM response streaming so that answers are displayed incrementally instead of waiting for the complete response.


## Current Scope and Limitations

- The current implementation retrieves the top three matching chunks for a question.
- Retrieval is performed against the shared ChromaDB collection.
- Answers depend on the content and quality of the uploaded PDF.
- Source relevance filtering for unrelated questions can be further improved.
- The application currently uses a local persistent ChromaDB database.

## Future Enhancements

- Document-specific retrieval and filtering.
- Improved similarity threshold handling.
- Support for multiple document formats.
- Conversation history and multi-turn question answering.
- Frontend interface for document upload and chat.
- Improved error handling and document management.

## Author

**Sinchana V S**

GitHub: [Sinchanavs12](https://github.com/Sinchanavs12)

---

*Developed as a hands-on learning project to explore Retrieval-Augmented Generation, vector databases, LLM integration, FastAPI, and LangGraph.*