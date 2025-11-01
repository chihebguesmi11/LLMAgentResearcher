"""
Nodes for the biochar extraction agent.
Each node is a function that takes State and returns modified State.
"""

from src.state import State
from typing import Dict, Any
from src.pdf_processor import extract_pdf_chunks
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from src.prompts import get_extraction_prompt
from src.output_formatter import format_to_markdown


from dotenv import load_dotenv
load_dotenv()

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",  
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


def load_pdf_node(state: State) -> State:
    """
    Load PDF and create chunks with page tracking.
    
    Reads: pdf_path
    Writes: pdf_chunks, page_count, status
    """
    print(f"[load_pdf_node] Loading PDF: {state['pdf_path']}")
    
    try:
        # Extract chunks from PDF
        chunks, page_count = extract_pdf_chunks(state['pdf_path'], pages_per_chunk=3)
        
        # Update state
        state['pdf_chunks'] = chunks
        state['page_count'] = page_count
        state['status'] = 'processing'
        state['error_message'] = ''
        
        print(f"[load_pdf_node] Success! Created {len(chunks)} chunks from {page_count} pages")
        
    except Exception as e:
        print(f"[load_pdf_node] ERROR: {str(e)}")
        state['status'] = 'error'
        state['error_message'] = f"Failed to load PDF: {str(e)}"
    
    return state



def analyze_chunk_node(state: State) -> State:
    """
    Analyze current chunk with Gemini to extract biochar information.
    
    Reads: pdf_chunks, current_chunk_index, questions, biochars_found
    Writes: biochars_found (append), current_chunk_index (increment)
    """
    current_idx = state['current_chunk_index']
    print(f"[analyze_chunk_node] Analyzing chunk {current_idx + 1}/{len(state['pdf_chunks'])}")
    
    try:
        # Get current chunk
        current_chunk = state['pdf_chunks'][current_idx]
        chunk_text = current_chunk['text']
        page_numbers = current_chunk['page_numbers']
        
        # Create prompt
        prompt = get_extraction_prompt(chunk_text, state['questions'])
        
        # Call Gemini
        print(f"[analyze_chunk_node] Calling Gemini API...")
        response = llm.invoke(prompt)
        
        # Parse JSON response
        response_text = response.content.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove ```
        
        response_text = response_text.strip()
        
        # Parse JSON
        findings = json.loads(response_text)
        
        print(f"[analyze_chunk_node] Found {len(findings)} biochar(s) in this chunk")
        
        # Add page info if not present
        for finding in findings:
            if "location" not in finding or not finding["location"]:
                finding["location"] = f"Pages {page_numbers[0]}-{page_numbers[-1]}"
        
        # Append to state
        state['biochars_found'].extend(findings)
        
        # Increment chunk index
        state['current_chunk_index'] += 1
        
    except json.JSONDecodeError as e:
        print(f"[analyze_chunk_node] JSON parse error: {e}")
        print(f"[analyze_chunk_node] Response was: {response_text[:200]}...")
        # Continue anyway, just skip this chunk
        state['current_chunk_index'] += 1
        
    except Exception as e:
        print(f"[analyze_chunk_node] ERROR: {str(e)}")
        state['status'] = 'error'
        state['error_message'] = f"Analysis failed: {str(e)}"
    
    return state




def format_output_node(state: State) -> State:
    """
    Format findings into markdown table.
    
    Reads: biochars_found, questions
    Writes: final_table, status
    """
    print(f"[format_output_node] Formatting {len(state['biochars_found'])} biochar(s)")
    
    try:
        # Format to markdown table
        markdown_table = format_to_markdown(state['biochars_found'], state['questions'])
        
        # Update state
        state['final_table'] = markdown_table
        state['status'] = 'complete'
        
        print(f"[format_output_node] Success! Table created.")
        print(f"\n{markdown_table}\n")
        
    except Exception as e:
        print(f"[format_output_node] ERROR: {str(e)}")
        state['status'] = 'error'
        state['error_message'] = f"Formatting failed: {str(e)}"
    
    return state