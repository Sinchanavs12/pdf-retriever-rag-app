
from pypdf import PdfReader

def extract_pdf_text(file_path):

    # Read the PDF
    reader = PdfReader(file_path)

    extracted_pages = []

    # Extract text from each page
    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        extracted_pages.append({
            "page_number": page_number,
            "text": text
        })

    return extracted_pages
