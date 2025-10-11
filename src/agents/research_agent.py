"""
Research Agent for topic discovery and SEO keyword analysis.

This agent discovers trending topics for Substack newsletters and identifies
high-value SEO keywords to optimize content for search engines.
"""
import logging
import random
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)


class ResearchAgent:
    """Agent for discovering trending topics and analyzing SEO keywords."""
    
    def __init__(self):
        """Initialize the research agent with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def discover_trending_topics(self, base_topics: Optional[List[str]] = None, count: int = 5) -> List[Dict[str, any]]:
        """
        Discover trending topics based on current trends and configured topics.
        
        Args:
            base_topics: Optional list of base topics to focus on. If None, uses settings.
            count: Number of trending topics to discover (default: 5)
        
        Returns:
            List of topic dictionaries with topic, rationale, and trend_score
        """
        if base_topics is None:
            base_topics = settings.topics_list
        
        topics_str = ", ".join(base_topics)
        
        prompt = f"""
        You are a content research expert analyzing current trends for newsletter content.
        Based on the following topic areas: {topics_str}
        
        Identify {count} specific, trending topics that would make excellent newsletter content.
        For each topic, provide:
        1. A clear, engaging topic title
        2. A brief rationale explaining why this topic is trending and valuable
        3. A trend score (1-10) indicating how timely and relevant it is
        
        Format your response as a JSON array with this structure:
        [
            {{
                "topic": "Topic Title",
                "rationale": "Why this topic is trending and valuable",
                "trend_score": 8
            }},
            ...
        ]
        
        Focus on topics that are:
        - Current and newsworthy
        - Relevant to the specified areas
        - Have strong reader interest
        - Suitable for in-depth newsletter content
        
        Return ONLY the JSON array, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            import json
            content = response.choices[0].message.content.strip()
            
            # Extract JSON if wrapped in code blocks
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:].strip()
            
            topics = json.loads(content)
            
            # Add metadata
            for topic in topics:
                topic["discovered_at"] = datetime.now().isoformat()
                topic["source"] = "ai_trend_analysis"
            
            logger.info(f"Discovered {len(topics)} trending topics")
            return topics
            
        except Exception as e:
            logger.error(f"Error discovering trending topics: {e}")
            # Fallback to generating topics from base topics
            return self._generate_fallback_topics(base_topics, count)
    
    def _generate_fallback_topics(self, base_topics: List[str], count: int) -> List[Dict[str, any]]:
        """Generate fallback topics when API call fails."""
        fallback_topics = []
        
        topic_templates = [
            "The Future of {topic}: Key Trends to Watch",
            "How {topic} is Transforming Industries in 2024",
            "5 Game-Changing Developments in {topic}",
            "{topic}: What Experts are Saying Now",
            "The Hidden Opportunities in {topic}"
        ]
        
        for i in range(min(count, len(base_topics))):
            topic = base_topics[i % len(base_topics)]
            template = random.choice(topic_templates)
            
            fallback_topics.append({
                "topic": template.format(topic=topic.title()),
                "rationale": f"A comprehensive look at current developments and future directions in {topic}.",
                "trend_score": random.randint(5, 8),
                "discovered_at": datetime.now().isoformat(),
                "source": "fallback_generation"
            })
        
        return fallback_topics
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def analyze_seo_keywords(self, topic: str, target_keywords: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Analyze and generate SEO keywords for a given topic.
        
        Args:
            topic: The topic to analyze for SEO keywords
            target_keywords: Optional list of target keywords to include
        
        Returns:
            Dictionary with primary keywords, secondary keywords, and long-tail keywords
        """
        target_keywords_text = ""
        if target_keywords:
            target_keywords_text = f"\nAlso consider these target keywords: {', '.join(target_keywords)}"
        
        prompt = f"""
        You are an SEO expert analyzing keywords for newsletter content optimization.
        
        Topic: "{topic}"{target_keywords_text}
        
        Provide a comprehensive SEO keyword analysis with:
        1. Primary keywords (3-5): High-volume, highly relevant keywords
        2. Secondary keywords (5-8): Supporting keywords with good search volume
        3. Long-tail keywords (5-10): Specific phrases with lower competition
        4. Search intent: The primary search intent (informational/navigational/transactional)
        5. Content recommendations: Brief tips for optimizing content
        
        Format your response as a JSON object:
        {{
            "primary_keywords": ["keyword1", "keyword2", "keyword3"],
            "secondary_keywords": ["keyword1", "keyword2", ...],
            "long_tail_keywords": ["specific phrase 1", "specific phrase 2", ...],
            "search_intent": "informational",
            "content_recommendations": "Brief optimization tips",
            "estimated_monthly_searches": "10k-100k"
        }}
        
        Return ONLY the JSON object, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.6
            )
            
            import json
            content = response.choices[0].message.content.strip()
            
            # Extract JSON if wrapped in code blocks
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:].strip()
            
            keywords = json.loads(content)
            
            # Add metadata
            keywords["analyzed_at"] = datetime.now().isoformat()
            keywords["topic"] = topic
            
            logger.info(f"Generated SEO keywords for topic: {topic}")
            return keywords
            
        except Exception as e:
            logger.error(f"Error analyzing SEO keywords: {e}")
            # Fallback to basic keyword extraction
            return self._generate_fallback_keywords(topic)
    
    def _generate_fallback_keywords(self, topic: str) -> Dict[str, any]:
        """Generate fallback keywords when API call fails."""
        # Extract words from topic
        words = topic.lower().split()
        
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = [word for word in words if word not in stop_words]
        
        return {
            "primary_keywords": keywords[:3] if len(keywords) >= 3 else keywords,
            "secondary_keywords": keywords[3:8] if len(keywords) > 3 else keywords + ["trends", "guide", "insights"],
            "long_tail_keywords": [
                f"{topic} guide",
                f"{topic} trends 2024",
                f"how to {topic}",
                f"{topic} best practices",
                f"{topic} for beginners"
            ],
            "search_intent": "informational",
            "content_recommendations": "Focus on comprehensive coverage and actionable insights.",
            "estimated_monthly_searches": "1k-10k",
            "analyzed_at": datetime.now().isoformat(),
            "topic": topic
        }
    
    def generate_research_summary(
        self, 
        topic_count: int = 3, 
        base_topics: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Generate a complete research summary with trending topics and SEO analysis.
        
        Args:
            topic_count: Number of topics to research (default: 3)
            base_topics: Optional list of base topics to focus on
        
        Returns:
            Complete research summary with topics and SEO keywords
        """
        logger.info(f"Starting research summary generation for {topic_count} topics")
        
        try:
            # Discover trending topics
            trending_topics = self.discover_trending_topics(base_topics, topic_count)
            
            # Analyze SEO keywords for each topic
            research_results = []
            for topic_data in trending_topics:
                topic_title = topic_data["topic"]
                
                # Get SEO keywords
                seo_analysis = self.analyze_seo_keywords(topic_title)
                
                # Combine results
                research_results.append({
                    "topic": topic_title,
                    "rationale": topic_data["rationale"],
                    "trend_score": topic_data["trend_score"],
                    "seo_keywords": {
                        "primary": seo_analysis["primary_keywords"],
                        "secondary": seo_analysis["secondary_keywords"],
                        "long_tail": seo_analysis["long_tail_keywords"]
                    },
                    "search_intent": seo_analysis["search_intent"],
                    "content_recommendations": seo_analysis["content_recommendations"],
                    "estimated_monthly_searches": seo_analysis.get("estimated_monthly_searches", "unknown"),
                    "discovered_at": topic_data["discovered_at"]
                })
            
            summary = {
                "research_date": datetime.now().isoformat(),
                "topic_count": len(research_results),
                "base_topics": base_topics or settings.topics_list,
                "research_results": research_results,
                "agent_version": "1.0.0",
                "status": "success"
            }
            
            logger.info(f"Research summary generated successfully with {len(research_results)} topics")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating research summary: {e}")
            raise
    
    def get_top_topic_with_seo(self, base_topics: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Get the single best trending topic with SEO analysis.
        
        Convenience method for getting one topic recommendation.
        
        Args:
            base_topics: Optional list of base topics to focus on
        
        Returns:
            Single topic with full SEO analysis
        """
        summary = self.generate_research_summary(topic_count=1, base_topics=base_topics)
        
        if summary["research_results"]:
            return summary["research_results"][0]
        else:
            raise Exception("No topics discovered")
