"""Research Assistant Agent for finding and presenting research papers."""

import autogen
from ..config.settings import LLM_CONFIG

def create_research_assistant() -> autogen.AssistantAgent:
    """Create and configure the research paper search assistant."""
    
    assistant_config = {
        "name": "research_assistant",
        "llm_config": LLM_CONFIG,
        "system_message": """You are a research paper search assistant. Your task is to help users find relevant research papers.
        When presenting results:
        1. Format each paper's information in a clear and structured manner
        2. Do not repeat information
        3. Include title, authors, year, citations, and a brief summary
        4. Use markdown formatting
        5. After providing the papers, respond with 'PAPERS_PROVIDED'"""
    }
    
    return autogen.AssistantAgent(**assistant_config) 