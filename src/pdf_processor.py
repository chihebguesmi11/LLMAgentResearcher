"""
PDF processing utilities.
Handles loading PDFs and creating chunks with page tracking.
"""

from pypdf import PdfReader
from typing import List, Dict, Any


def extract_pdf_chunks(pdf_path: str, pages_per_chunk: int = 3) -> tuple[List[Dict[str, Any]], int]:
    """
    Extract text from PDF and split into chunks by pages.
    
    Args:
        pdf_path: Path to PDF file
        pages_per_chunk: Number of pages to include in each chunk
        
    Returns:
        Tuple of (chunks_list, total_pages)
        Each chunk is a dict with: {text, page_numbers, chunk_index}
    """
    print(f"[pdf_processor] Loading PDF from: {pdf_path}")
    
    # Load PDF
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"[pdf_processor] Total pages: {total_pages}")
    
    chunks = []
    chunk_index = 0
    
    # Process pages in groups
    for i in range(0, total_pages, pages_per_chunk):
        # Get pages for this chunk
        chunk_pages = []
        page_numbers = []
        
        for page_num in range(i, min(i + pages_per_chunk, total_pages)):
            page = reader.pages[page_num]
            chunk_pages.append(page.extract_text())
            page_numbers.append(page_num + 1)  # 1-indexed for humans
        
        # Combine pages into one chunk
        chunk_text = "\n\n--- Page Break ---\n\n".join(chunk_pages)
        
        chunks.append({
            "text": chunk_text,
            "page_numbers": page_numbers,
            "chunk_index": chunk_index,
            "total_chunks": None 
        })
        
        chunk_index += 1
    
    # Set total_chunks for all chunks
    for chunk in chunks:
        chunk["total_chunks"] = len(chunks)
    
    print(f"[pdf_processor] Created {len(chunks)} chunks")
    return chunks, total_pages