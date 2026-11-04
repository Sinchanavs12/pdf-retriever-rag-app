
from .pdf_processor import extract_pdf_text

# Path of our uploaded PDF
file_path = "uploads/CNS-module-1.pdf"

# Extract text
pages = extract_pdf_text(file_path)

# Display extracted content
print("Total pages:", len(pages))

for page in pages:
    print("\nPage:", page["page_number"])
    print(page["text"][:500])
