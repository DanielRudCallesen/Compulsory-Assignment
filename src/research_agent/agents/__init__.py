"""Agents package for the research agent."""

from .research_assistant import create_research_assistant
from .evaluator import create_evaluator

__all__ = ['create_research_assistant', 'create_evaluator'] 