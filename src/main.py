"""
Main entry point for the biochar extraction agent.
Run this script to process a PDF and extract biochar information.
"""

import os
from dotenv import load_dotenv
from src.state import State
from src.graph import create_agent_graph


def main():
    """
    Main function to run the biochar extraction agent.
    """
    # Load environment variables
    load_dotenv()
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in environment!")
        print("Please add it to your .env file")
        return
    
    print("=" * 60)
    print("BIOCHAR EXTRACTION AGENT")
    print("=" * 60)
    
    # Define questions to answer
    questions = [
        "What is the biochar?",
        "What is the targeted molecule?",
        "What is the adsorption capacity of the biochar?",
        "Where is this information located (page number or section)?"
    ]
    
    # Initialize state
    initial_state = State(
        pdf_path="data/research_paper.pdf",
        questions=questions,
        pdf_chunks=[],
        current_chunk_index=0,
        page_count=0,
        biochars_found=[],
        final_table="",
        status="initialized",
        error_message=""
    )
    
    print(f"\nProcessing: {initial_state['pdf_path']}")
    print(f"Questions: {len(questions)}")
    print("\n" + "=" * 60)
    
    # Create agent
    agent = create_agent_graph()
    
    # Run agent
    try:
        print("\n Starting agent execution...\n")
        final_state = agent.invoke(initial_state)
        
        # Display results
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        print(f"Status: {final_state['status']}")
        print(f"Pages processed: {final_state['page_count']}")
        print(f"Chunks processed: {len(final_state['pdf_chunks'])}")
        print(f"Biochars found: {len(final_state['biochars_found'])}")
        
        if final_state['error_message']:
            print(f"\n  Error: {final_state['error_message']}")
        
        print("\n" + "=" * 60)
        print("FINAL TABLE")
        print("=" * 60)
        print(final_state['final_table'])
        
        # Optionally save to file
        save_results(final_state)
        
    except Exception as e:
        print(f"\n Agent execution failed: {str(e)}")
        import traceback
        traceback.print_exc()


def save_results(state: State):
    """
    Save results to output files.
    
    Args:
        state: Final state with results
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save markdown table
    markdown_path = os.path.join(output_dir, "biochar_results.md")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write("# Biochar Extraction Results\n\n")
        f.write(f"**Source:** {state['pdf_path']}\n\n")
        f.write(f"**Pages:** {state['page_count']}\n\n")
        f.write(f"**Biochars Found:** {len(state['biochars_found'])}\n\n")
        f.write("## Results Table\n\n")
        f.write(state['final_table'])
    
    print(f"\n Results saved to: {markdown_path}")
    
    # Save JSON for programmatic access
    import json
    json_path = os.path.join(output_dir, "biochar_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "pdf_path": state['pdf_path'],
            "page_count": state['page_count'],
            "biochars_found": state['biochars_found'],
            "status": state['status']
        }, f, indent=2)
    
    print(f" JSON saved to: {json_path}")


if __name__ == "__main__":
    main()