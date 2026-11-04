
from .pdf_processor import extract_pdf_text
from .chunker import chunk_pages

# PDF path
file_path = "uploads/CNS-module-1.pdf"

# Extract PDF text
pages = extract_pdf_text(file_path)

# Generate chunks
chunks = chunk_pages(pages, "CNS-module-1.pdf")

# Display results
print("Total PDF pages:", len(pages))
print("Total chunks generated:", len(chunks))

for chunk in chunks[:5]:

    print("\nChunk ID:", chunk["chunk_id"])
    print("Metadata:", chunk["metadata"])
    print("Content:", chunk["text"])
    print("-" * 50)
