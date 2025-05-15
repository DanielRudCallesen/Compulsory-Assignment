# INORGE THIS DOCUMENT. IT IS NOT USED.


import autogen
from typing import Dict, List, Optional
import requests



# Configuration
LLM_CONFIG = {
    "config_list": [
        {
            "model": "open-mistral-nemo",
            "api_key": "T1pm2HHhpue136c6SRR2H8SL9cwjpt2s",
            "api_type": "mistral",
            "api_rate_limit": 0.25,
            "repeat_penalty": 1.1,
            "temperature": 0.0,
            "seed": 42,
            "stream": False,
            "native_tool_calls": False,
            "cache_seed": None,
        }
    ]
}

# Research Paper Tool
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
            print(f"Error searching papers: {e}")
            return []
        
# Create the research paper search agent
def create_research_agent():
    """Create and configure the research paper search agent."""
    
    # Create the research paper tool
    research_tool = ResearchPaperTool()
    
    # Define the assistant configuration
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
    
    # Create the assistant
    assistant = autogen.AssistantAgent(**assistant_config)
    
    # Define the user proxy
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "").upper(),
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False
        },
        llm_config=LLM_CONFIG,
        system_message="""You are an evaluator of research paper search results. Your task is to:
        1. Wait for the research assistant to provide papers and respond with 'PAPERS_PROVIDED'
        2. Then evaluate the papers based on these criteria:
           - Completeness (1-5): Did the agent provide all required information?
           - Quality (1-5): Is the information clear and well-formatted?
           - Robustness (1-5): Do the papers match the search criteria?
           - Consistency (1-5): Is the formatting consistent?
           - Specificity (1-5): Are the details relevant and precise?
        3. Provide a score and detailed feedback for each criterion
        4. Return 'TERMINATE' after providing the evaluation"""
    )
    
    return assistant, user_proxy, research_tool

def main():
    try:
        assistant, user_proxy, research_tool = create_research_agent()

        search_query = {
            "topic": "machine learning",
            "year": 2020,
            "min_citations": 100
        }
        
        # Start the conversation
        prompt = f"""Please find research papers about {search_query['topic']} from {search_query['year']} 
        with at least {search_query['min_citations']} citations. For each paper, provide:
        1. Title
        2. Year
        3. Citations
        4. Brief Summary
        
        After providing the papers, respond with 'PAPERS_PROVIDED'"""
        
        # Get response from research assistant and evaluate
        user_proxy.initiate_chat(
            assistant,
            message=prompt
        )
        
        logger.info("Program completed after evaluation.")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main() 