from .pdf_processor import extract_pdf_text
from .chunker import chunk_pages
from .embeddings import generate_embeddings

# Step 1: Extract PDF text
file_path = "uploads/CNS-module-1.pdf"

pages = extract_pdf_text(file_path)

# Step 2: Generate chunks
chunks = chunk_pages(pages, "CNS-module-1.pdf")

# Step 3: Generate embeddings
embeddings = generate_embeddings(chunks)

# Step 4: Display results
print("Total chunks:", len(chunks))
print("Total embeddings:", len(embeddings))

print("\nFirst embedding:")
print(embeddings[0])

print("\nEmbedding dimensions:")
print(len(embeddings[0]))

print("\nEmbedding generation successful!")