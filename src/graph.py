"""
LangGraph construction for the biochar extraction agent.
Defines the workflow and connects all nodes.
"""

from langgraph.graph import StateGraph, END
from src.state import State
from src.nodes import load_pdf_node, analyze_chunk_node, format_output_node


def should_continue(state: State) -> str:
    """
    Conditional edge: Determine if we should continue processing chunks.
    
    Returns:
        "analyze_chunk" if more chunks to process
        "format_output" if all chunks processed
    """
    current_idx = state['current_chunk_index']
    total_chunks = len(state['pdf_chunks'])
    
    if current_idx < total_chunks:
        print(f"[should_continue] Chunk {current_idx}/{total_chunks} - continuing...")
        return "analyze_chunk"
    else:
        print(f"[should_continue] All chunks processed - formatting output...")
        return "format_output"


def create_agent_graph():
    """
    Create and compile the biochar extraction agent graph.
    
    Workflow:
        START → load_pdf → analyze_chunk → [decision] → format_output → END
                                    ↑           |
                                    |___________|
                                    (loop if more chunks)
    
    Returns:
        Compiled LangGraph agent
    """
    
    # Initialize the graph with State schema
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("load_pdf", load_pdf_node)
    workflow.add_node("analyze_chunk", analyze_chunk_node)
    workflow.add_node("format_output", format_output_node)
    
    # Set entry point
    workflow.set_entry_point("load_pdf")
    
    # Add edges
    # load_pdf → analyze_chunk
    workflow.add_edge("load_pdf", "analyze_chunk")
    
    # analyze_chunk → [conditional decision]
    workflow.add_conditional_edges(
        "analyze_chunk",
        should_continue,
        {
            "analyze_chunk": "analyze_chunk",  # Loop back if more chunks
            "format_output": "format_output"    # Move forward if done
        }
    )
    
    # format_output → END
    workflow.add_edge("format_output", END)
    
    # Compile the graph
    print("[create_agent_graph] Graph compiled successfully!")
    return workflow.compile()