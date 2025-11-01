"""
Output formatting utilities.
Converts biochar findings to various table formats.
"""

import pandas as pd
from typing import List, Dict


def format_to_markdown(biochars: List[Dict[str, str]], questions: List[str]) -> str:
    """
    Convert list of biochar findings to markdown table.
    
    Args:
        biochars: List of biochar information dicts
        questions: Original questions (for column headers)
        
    Returns:
        Markdown formatted table string
    """
    
    if not biochars:
        return "No biochars found in the document."
    
    # Create DataFrame
    df = pd.DataFrame(biochars)
    
    # Reorder columns to match questions
    desired_columns = ["name", "description", "targeted_molecule", "adsorption_capacity", "location"]
    
    # Only include columns that exist
    columns = [col for col in desired_columns if col in df.columns]
    df = df[columns]
    
    # Rename columns to be more readable
    column_names = {
        "name": "Biochar Name",
        "description": "What is the Biochar?",
        "targeted_molecule": "Targeted Molecule",
        "adsorption_capacity": "Adsorption Capacity",
        "location": "Location (Page/Section)"
    }
    
    df = df.rename(columns=column_names)
    
    # Convert to markdown
    markdown_table = df.to_markdown(index=False)
    
    return markdown_table