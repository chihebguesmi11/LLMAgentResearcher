"""
Prompt templates for LLM interactions.
"""

from typing import List


def get_extraction_prompt(text: str, questions: List[str]) -> str:
    """
    Create a prompt for extracting biochar information.
    
    Args:
        text: Text chunk to analyze
        questions: List of questions to answer about each biochar
        
    Returns:
        Formatted prompt string
    """
    
    # Format questions as numbered list
    questions_formatted = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    
    prompt = f"""You are a scientific research assistant analyzing a research paper about biochar.

Your task: Extract information about EVERY biochar mentioned in the text below.

For each biochar you find, answer these questions:
{questions_formatted}

IMPORTANT INSTRUCTIONS:
- Only extract information that is explicitly stated in the text
- If a biochar is mentioned but information is missing, use "Not specified"
- Include the page numbers where you found the information
- Return your response as a JSON array of objects
- Each object should have keys: "name", "description", "targeted_molecule", "adsorption_capacity", "location"

TEXT TO ANALYZE:
{text}

Return ONLY valid JSON in this format:
[
  {{
    "name": "Biochar name or type",
    "description": "What is this biochar",
    "targeted_molecule": "Molecule it targets",
    "adsorption_capacity": "Capacity with units",
    "location": "Page X, Section Y"
  }}
]

If NO biochars are found in this text, return an empty array: []
"""
    
    return prompt