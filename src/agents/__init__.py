"""
CrewAI agents for Substack Auto content generation.

This module provides AI agents for various content creation tasks,
including SEO analysis, content optimization, and workflow automation.
"""

__version__ = "1.0.0"

# Import agents when they are created
# from .seo_agent import SEOAnalyzer, create_seo_agent
Agent modules for content processing and validation.
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, name: str):
        """
        Initialize the base agent.
        
        Args:
            name: The name of the agent
        """
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    def process(self, content: Dict) -> Dict:
        """
        Process content with this agent.
        
        Args:
            content: Content dictionary to process
            
        Returns:
            Dictionary containing processing results
        """
        raise NotImplementedError("Subclasses must implement process()")
    
    def validate_input(self, content: Dict) -> bool:
        """
        Validate input content structure.
        
        Args:
            content: Content dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        return isinstance(content, dict)


__all__ = ["BaseAgent"]
