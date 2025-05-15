"""Tool for searching research papers using the Semantic Scholar API."""

import requests
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class ResearchPaperTool:
    """Tool for searching research papers using the Semantic Scholar API."""
    
    def __init__(self):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        
    def search_papers(self, topic: str, year: Optional[int] = None, 
                     min_citations: Optional[int] = None, 
                     max_results: int = 10) -> List[Dict]:
        """
        Search for research papers using the Semantic Scholar API.
        
        Args:
            topic: The research topic to search for
            year: Optional year filter
            min_citations: Optional minimum number of citations
            max_results: Maximum number of results to return
            
        Returns:
            List of paper information dictionaries
        """
        query = {
            "query": topic,
            "fields": "title,authors,year,citationCount,abstract,url",
            "limit": max_results
        }
        
        try:
            response = requests.get(f"{self.base_url}/paper/search", params=query)
            response.raise_for_status()
            papers = response.json().get("data", [])
            
            # Apply filters
            if year is not None:
                papers = [p for p in papers if p.get("year") == year]
            if min_citations is not None:
                papers = [p for p in papers if p.get("citationCount", 0) >= min_citations]
                
            return papers
        except Exception as e:
            logger.error(f"Error searching papers: {e}")
            return [] 