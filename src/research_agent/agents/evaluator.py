"""Evaluator Agent for assessing research paper search results."""

import autogen
from ..config.settings import LLM_CONFIG

def create_evaluator() -> autogen.UserProxyAgent:
    """Create and configure the evaluator agent."""
    
    return autogen.UserProxyAgent(
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