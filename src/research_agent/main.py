from .agents.research_assistant import create_research_assistant
from .agents.evaluator import create_evaluator
from .tools.paper_search import ResearchPaperTool
from .config.settings import logger, DEFAULT_SEARCH

def main():
    
    try:
        # Create the agents and tools
        assistant = create_research_assistant()
        user_proxy = create_evaluator()
        research_tool = ResearchPaperTool()
        
        

        # Example search query in settings.py
        search_query = DEFAULT_SEARCH
        
        logger.info("=== Research Paper Search Agent Demo ===")
        logger.info(f"Searching for papers about: {search_query['topic']}")
        logger.info(f"Published in: {search_query['year']}")
        logger.info(f"Minimum citations: {search_query['min_citations']}")
        logger.info("Starting search...")
        
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
