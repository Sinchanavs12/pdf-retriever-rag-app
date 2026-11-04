
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pages(extracted_pages, source_filename):

    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []
    chunk_id = 0

    # Process each extracted page
    for page in extracted_pages:

        page_text = page["text"]

        if not page_text.strip():
            continue

        # Split page text into smaller chunks
        page_chunks = text_splitter.split_text(page_text)

        for text in page_chunks:

            chunks.append({
                "chunk_id": chunk_id,
                "text": text,
                "metadata": {
                    "source": source_filename,
                    "page_number": page["page_number"]
                }
            })

            chunk_id += 1

    return chunks
