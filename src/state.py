from typing import List, Dict, Any
from typing_extensions import TypedDict

class State(TypedDict):
    """
    State for the biochar extraction agent.
    Tracks the flow of information from PDF input to table output.
    """
    pdf_path: str
    questions: List[str]
    pdf_chunks: List[Dict[str, Any]] 
    current_chunk_index: int 
    page_count : int
    biochars_found: List[Dict[str, str]]
    final_table: str
    status: str  # "initialized", "processing", "complete", "error"
    error_message: str 