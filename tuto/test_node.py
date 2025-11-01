"""
Test individual nodes in isolation.
"""

import sys
sys.path.append('.') 

from src.state import State
from src.nodes import load_pdf_node


def test_load_pdf():
    """Test the load_pdf_node."""
    
    # Create initial state
    initial_state = State(
        pdf_path="data/research_paper.pdf", 
        questions=[],
        pdf_chunks=[],
        current_chunk_index=0,
        page_count=0,
        biochars_found=[],
        final_table="",
        status="initialized",
        error_message=""
    )
    
    print("=== Testing load_pdf_node ===")
    result = load_pdf_node(initial_state)
    
    print(f"\nResults:")
    print(f"  Status: {result['status']}")
    print(f"  Page count: {result['page_count']}")
    print(f"  Number of chunks: {len(result['pdf_chunks'])}")
    print(f"  Error: {result['error_message']}")
    
    if result['pdf_chunks']:
        print(f"\n  First chunk preview:")
        print(f"    Pages: {result['pdf_chunks'][0]['page_numbers']}")
        print(f"    Text length: {len(result['pdf_chunks'][0]['text'])} chars")
        print(f"    First 200 chars: {result['pdf_chunks'][0]['text'][:200]}...")


if __name__ == "__main__":
    test_load_pdf()