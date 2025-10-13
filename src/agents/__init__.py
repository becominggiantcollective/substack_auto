"""
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


from .fact_checker_agent import FactCheckerAgent
from .analytics_agent import AnalyticsAgent
from .performance_predictor import PerformancePredictorAgent
from .topic_trending import TopicTrendingAgent
from .ab_testing import ABTestingFramework


__all__ = [
    "BaseAgent",
    "FactCheckerAgent",
    "AnalyticsAgent",
    "PerformancePredictorAgent",
    "TopicTrendingAgent",
    "ABTestingFramework"
]
