
from app.pdf_processor import extract_pdf_text
from app.chunker import chunk_pages
from app.embeddings import generate_embeddings
from app.vector_store import store_chunks

file_path = "uploads/CNS-module-1.pdf"

# Step 1: Extract PDF text
pages = extract_pdf_text(file_path)

# Step 2: Generate chunks
chunks = chunk_pages(pages, "CNS-module-1.pdf")

# Step 3: Generate embeddings
embeddings = generate_embeddings(chunks)

# Step 4: Store everything in ChromaDB
total_records = store_chunks(
    chunks,
    embeddings,
    "test-document-001"
)

print("Total chunks:", len(chunks))
print("Records stored in ChromaDB:", total_records)
print("Vector storage successful!")