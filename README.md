# LLM Agent Researcher - Biochar Extraction

An intelligent agent built with LangGraph and Gemini that extracts biochar information from research papers.


![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-00ADD8?style=for-the-badge&logo=chainlink&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-9146FF?style=for-the-badge&logo=graph&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![PyPDF](https://img.shields.io/badge/PyPDF-2C2D72?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)
![AI Agents](https://img.shields.io/badge/AI%20Agents-FF6F00?style=for-the-badge&logo=openai&logoColor=white)

## Overview

This project uses a multi-agent workflow to:
- Load and process PDF research papers
- Extract structured information about biochars
- Answer specific questions about biochar properties
- Generate formatted tables of findings

## Architecture

The agent uses **chunked processing** with the following workflow:
```
START → load_pdf → analyze_chunk ⟲ → format_output → END
                        ↓              ↑
                        └──(loop)──────┘
```

### Components:
- **State Management**: TypedDict schema tracking data flow
- **Nodes**: Three main operations (load, analyze, format)
- **Conditional Edges**: Loop through chunks until complete
- **LLM**: Google Gemini 1.5 Flash for extraction

## Installation

### Prerequisites
- Python 3.9+
- Google Gemini API key (

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/chihebguesmi11/LLMAgentResearcher.git
cd LLMAgentResearcher
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

5. **Add your research paper**

Place your PDF in the `data/` folder:
```
data/research_paper.pdf
```

## Usage

Run the agent:
```bash
python src/main.py
```

The agent will:
1. Load the PDF and create chunks
2. Analyze each chunk with Gemini
3. Extract biochar information
4. Generate a markdown table
5. Save results to `output/biochar_results.md`

##  Project Structure
```
LLMAgentResearcher/
├── data/                   # Input PDFs
├── src/
│   ├── state.py           # State schema definition
│   ├── nodes.py           # Agent node functions
│   ├── graph.py           # LangGraph workflow
│   ├── pdf_processor.py   # PDF utilities
│   ├── prompts.py         # LLM prompts
│   ├── output_formatter.py # Table formatting
│   └── main.py            # Entry point
├── tutorials/              # Test notebooks
├── output/                 # Generated results
├── .env                    # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

##  Example Output
```markdown
| Biochar Name      | What is the Biochar?        | Targeted Molecule | Adsorption Capacity | Location        |
|-------------------|-----------------------------|-------------------|---------------------|-----------------|
| Rice husk biochar | Biochar from rice husk...   | Lead (Pb)        | 150 mg/g           | Pages 5-7       |
| Bamboo biochar    | Biochar from bamboo...      | Copper (Cu)      | 200 mg/g           | Pages 8-10      |
```

##  Technologies Used

- **LangGraph**: Agentic workflow orchestration
- **LangChain**: LLM integration
- **Google Gemini**: Gemini-2.5-flash-lite model for text extraction
- **pypdf**: PDF text extraction
- **Pandas**: Data manipulation and table formatting

## Configuration

Customize behavior in `src/main.py`:
```python
# Modify questions
questions = [
    "What is the biochar?",
    "What is the targeted molecule?",
    # Add more questions...
]

# Adjust chunk size in pdf_processor.py
pages_per_chunk = 3  # Process 3 pages at a time
```

##  Troubleshooting

### API Key Not Found
```bash
# Check .env file exists and has correct format
type .env
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### PDF Not Loading
- Ensure PDF is in `data/` folder
- Check file path in `main.py`
- Verify PDF is not corrupted

## Future Improvements

- [ ] Add deduplication for biochars mentioned multiple times
- [ ] Implement caching to reduce API costs
- [ ] Add support for multiple output formats (CSV, Excel)
- [ ] Create web interface for easier interaction
- [ ] Add batch processing for multiple PDFs
- [ ] Implement error recovery and retry logic
- [ ] Add progress bar for long documents

## 📄 License

MIT License - feel free to use and modify

## 👤 Author

Chiheb Guesmi - [GitHub Profile](https://github.com/chihebguesmi11)

##  Acknowledgments

- Built as a technical exercise for LLM agent development
- Uses LangGraph framework by LangChain
- Powered by Google Gemini AI
