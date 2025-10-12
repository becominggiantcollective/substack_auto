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
    def analyze_competition(self, topic: str, keywords: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Analyze competition level for a given topic and keywords.
        
        Args:
            topic: The topic to analyze competition for
            keywords: Optional list of keywords to analyze competition for
        
        Returns:
            Dictionary with competition analysis including difficulty scores and opportunities
        """
        keywords_text = ""
        if keywords:
            keywords_text = f"\nFocus on these keywords: {', '.join(keywords[:5])}"
        
        prompt = f"""
        You are a competitive analysis expert for content marketing.
        
        Topic: "{topic}"{keywords_text}
        
        Analyze the competitive landscape for this topic and provide:
        1. Competition level (low/medium/high): Overall difficulty to rank for this topic
        2. Keyword difficulty: Average difficulty score (1-100) for ranking
        3. Content saturation: How saturated this topic is with existing content
        4. Content gaps: Specific angles or subtopics with lower competition
        5. Differentiation opportunities: Unique approaches to stand out
        6. Recommended focus: Which aspects to emphasize for competitive advantage
        
        Format your response as a JSON object:
        {{
            "competition_level": "medium",
            "keyword_difficulty": 45,
            "content_saturation": "high",
            "content_gaps": ["specific gap 1", "specific gap 2", "specific gap 3"],
            "differentiation_opportunities": ["unique angle 1", "unique angle 2"],
            "recommended_focus": "Brief recommendation on what to focus on",
            "competitive_advantage": "What makes this approach stand out"
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
            
            competition = json.loads(content)
            
            # Add metadata
            competition["analyzed_at"] = datetime.now().isoformat()
            competition["topic"] = topic
            
            logger.info(f"Analyzed competition for topic: {topic}")
            return competition
            
        except Exception as e:
            logger.error(f"Error analyzing competition: {e}")
            # Fallback to basic competition analysis
            return self._generate_fallback_competition(topic)
    
    def _generate_fallback_competition(self, topic: str) -> Dict[str, any]:
        """Generate fallback competition analysis when API call fails."""
        return {
            "competition_level": "medium",
            "keyword_difficulty": 50,
            "content_saturation": "moderate",
            "content_gaps": [
                f"Practical implementation of {topic}",
                f"Beginner's perspective on {topic}",
                f"Case studies in {topic}"
            ],
            "differentiation_opportunities": [
                "Focus on real-world examples",
                "Provide actionable step-by-step guides"
            ],
            "recommended_focus": "Focus on practical, actionable content with unique examples",
            "competitive_advantage": "Provide depth and practicality that others may lack",
            "analyzed_at": datetime.now().isoformat(),
            "topic": topic
        }
    
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
        base_topics: Optional[List[str]] = None,
        include_competition: bool = True
    ) -> Dict[str, any]:
        """
        Generate a complete research summary with trending topics, SEO analysis, and competition data.
        
        Args:
            topic_count: Number of topics to research (default: 3)
            base_topics: Optional list of base topics to focus on
            include_competition: Whether to include competition analysis (default: True)
        
        Returns:
            Complete research summary with topics, SEO keywords, and competition analysis
        """
        logger.info(f"Starting research summary generation for {topic_count} topics")
        
        try:
            # Discover trending topics
            trending_topics = self.discover_trending_topics(base_topics, topic_count)
            
            # Analyze SEO keywords and competition for each topic
            research_results = []
            for topic_data in trending_topics:
                topic_title = topic_data["topic"]
                
                # Get SEO keywords
                seo_analysis = self.analyze_seo_keywords(topic_title)
                
                # Build result object
                result = {
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
                }
                
                # Add competition analysis if requested
                if include_competition:
                    competition_analysis = self.analyze_competition(
                        topic_title, 
                        seo_analysis["primary_keywords"]
                    )
                    result["competition"] = {
                        "level": competition_analysis["competition_level"],
                        "keyword_difficulty": competition_analysis["keyword_difficulty"],
                        "content_saturation": competition_analysis["content_saturation"],
                        "content_gaps": competition_analysis["content_gaps"],
                        "differentiation_opportunities": competition_analysis["differentiation_opportunities"],
                        "recommended_focus": competition_analysis["recommended_focus"],
                        "competitive_advantage": competition_analysis.get("competitive_advantage", "")
                    }
                
                research_results.append(result)
            
            summary = {
                "research_date": datetime.now().isoformat(),
                "topic_count": len(research_results),
                "base_topics": base_topics or settings.topics_list,
                "research_results": research_results,
                "agent_version": "1.1.0",
                "status": "success",
                "includes_competition_analysis": include_competition
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
