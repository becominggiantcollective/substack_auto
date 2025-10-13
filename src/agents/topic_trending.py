"""
Topic Trending Agent for identifying trending topics and content opportunities.

This agent analyzes current trends and suggests timely content topics.
"""
import json
import logging
from typing import Dict, List
from datetime import datetime
from openai import OpenAI

logger = logging.getLogger(__name__)


class TopicTrendingAgent:
    """Agent for identifying trending topics and content opportunities."""
    
    def __init__(self, api_key: str = None):
        """Initialize the topic trending agent.
        
        Args:
            api_key: OpenAI API key (if None, will load from settings)
        """
        if api_key is None:
            from config.settings import settings
            api_key = settings.openai_api_key
            self.default_topics = settings.topics_list
        else:
            self.default_topics = ["technology", "AI", "innovation"]
        
        self.client = OpenAI(api_key=api_key)
        self.trend_cache = {}
        logger.info("TopicTrendingAgent initialized")
    
    def discover_trending_topics(self, categories: List[str] = None, limit: int = 10) -> Dict[str, any]:
        """Discover trending topics in specified categories.
        
        Args:
            categories: List of categories to search (defaults to configured topics)
            limit: Maximum number of trends to return
        
        Returns:
            Dictionary with trending topics and analysis
        """
        try:
            if categories is None:
                categories = self.default_topics
            
            logger.info(f"Discovering trends in categories: {categories}")
            
            prompt = f"""As a content trends analyst, identify the most trending and engaging topics 
right now in these categories: {', '.join(categories)}.

For each trend, provide:
1. Topic name and brief description
2. Why it's trending (current events, innovations, discussions)
3. Audience interest level (high/medium/low)
4. Content angle suggestions (3-5 specific angles to cover)
5. Keywords and hashtags
6. Estimated longevity (short-term/medium-term/long-term)

Identify {limit} trending topics that would make compelling blog content.

Format as JSON:
{{
  "trends": [
    {{
      "topic": "Topic name",
      "description": "Brief description",
      "why_trending": "Explanation",
      "interest_level": "high/medium/low",
      "content_angles": ["angle1", "angle2", "angle3"],
      "keywords": ["keyword1", "keyword2"],
      "hashtags": ["#tag1", "#tag2"],
      "longevity": "short/medium/long-term",
      "relevance_score": 0.0-1.0
    }}
  ],
  "analysis_date": "ISO timestamp"
}}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content strategist who identifies trending topics and content opportunities based on current events, innovations, and audience interests."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            trends_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            if "```json" in trends_text:
                trends_text = trends_text.split("```json")[1].split("```")[0].strip()
            elif "```" in trends_text:
                trends_text = trends_text.split("```")[1].split("```")[0].strip()
            
            trends_data = json.loads(trends_text)
            trends_data["discovered_at"] = datetime.now().isoformat()
            trends_data["categories_analyzed"] = categories
            
            # Cache results
            self.trend_cache = trends_data
            
            logger.info(f"Discovered {len(trends_data.get('trends', []))} trending topics")
            return trends_data
            
        except Exception as e:
            logger.error(f"Error discovering trends: {e}")
            return self._get_fallback_trends(categories, limit)
    
    def suggest_content_topics(self, count: int = 5, categories: List[str] = None) -> List[Dict]:
        """Suggest specific content topics based on trends.
        
        Args:
            count: Number of topics to suggest
            categories: Categories to focus on
        
        Returns:
            List of content topic suggestions with details
        """
        try:
            trends_data = self.discover_trending_topics(categories, limit=count * 2)
            trends = trends_data.get("trends", [])
            
            # Filter and rank by relevance score
            high_value_trends = [t for t in trends if t.get("relevance_score", 0) >= 0.7]
            if len(high_value_trends) < count:
                high_value_trends = trends  # Use all if not enough high-value ones
            
            # Sort by relevance score
            sorted_trends = sorted(high_value_trends, key=lambda x: x.get("relevance_score", 0), reverse=True)
            
            # Generate specific content suggestions
            suggestions = []
            for i, trend in enumerate(sorted_trends[:count]):
                for angle in trend.get("content_angles", [])[:1]:  # Take first angle
                    suggestions.append({
                        "title_suggestion": self._generate_title(trend["topic"], angle),
                        "topic": trend["topic"],
                        "angle": angle,
                        "description": trend["description"],
                        "keywords": trend.get("keywords", []),
                        "hashtags": trend.get("hashtags", []),
                        "priority": "high" if trend.get("interest_level") == "high" else "medium",
                        "urgency": "urgent" if trend.get("longevity") == "short-term" else "normal",
                        "relevance_score": trend.get("relevance_score", 0.5)
                    })
                    
                    if len(suggestions) >= count:
                        break
                
                if len(suggestions) >= count:
                    break
            
            logger.info(f"Generated {len(suggestions)} content topic suggestions")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting content topics: {e}")
            return []
    
    def analyze_topic_competition(self, topic: str) -> Dict[str, any]:
        """Analyze competition and saturation for a topic.
        
        Args:
            topic: Topic to analyze
        
        Returns:
            Competition analysis
        """
        try:
            prompt = f"""Analyze the content competition and saturation for this topic: "{topic}"

Provide:
1. Competition level (low/medium/high)
2. Content saturation (low/medium/high)
3. Unique angle opportunities (list 5 unique angles not commonly covered)
4. Difficulty score (0.0-1.0, where 1.0 is very difficult to rank)
5. Opportunity score (0.0-1.0, where 1.0 is excellent opportunity)
6. Recommended approach (how to stand out)

Format as JSON:
{{
  "topic": "topic name",
  "competition_level": "low/medium/high",
  "saturation_level": "low/medium/high",
  "unique_angles": ["angle1", "angle2", "angle3", "angle4", "angle5"],
  "difficulty_score": 0.0-1.0,
  "opportunity_score": 0.0-1.0,
  "recommended_approach": "detailed strategy",
  "key_differentiators": ["diff1", "diff2", "diff3"]
}}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a content strategy expert specializing in competitive analysis and market positioning."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            if "```json" in analysis_text:
                analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
            elif "```" in analysis_text:
                analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(analysis_text)
            analysis["analyzed_at"] = datetime.now().isoformat()
            
            logger.info(f"Analyzed competition for topic: {topic}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing topic competition: {e}")
            return {
                "topic": topic,
                "competition_level": "medium",
                "saturation_level": "medium",
                "difficulty_score": 0.5,
                "opportunity_score": 0.5,
                "error": str(e)
            }
    
    def get_evergreen_topics(self, categories: List[str] = None, count: int = 10) -> List[Dict]:
        """Get evergreen topics that remain relevant over time.
        
        Args:
            categories: Categories to search
            count: Number of topics to return
        
        Returns:
            List of evergreen topic suggestions
        """
        try:
            if categories is None:
                categories = self.default_topics
            
            prompt = f"""Identify {count} evergreen topics in these categories: {', '.join(categories)}

Evergreen topics are those that remain relevant and valuable over time.

For each topic provide:
1. Topic name
2. Why it's evergreen
3. Key subtopics to cover
4. Target audience
5. Longevity score (0.0-1.0)

Format as JSON array."""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a content strategist specializing in evergreen content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            topics_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            if "```json" in topics_text:
                topics_text = topics_text.split("```json")[1].split("```")[0].strip()
            elif "```" in topics_text:
                topics_text = topics_text.split("```")[1].split("```")[0].strip()
            
            topics = json.loads(topics_text)
            
            # Ensure it's a list
            if isinstance(topics, dict) and "topics" in topics:
                topics = topics["topics"]
            
            logger.info(f"Identified {len(topics)} evergreen topics")
            return topics
            
        except Exception as e:
            logger.error(f"Error getting evergreen topics: {e}")
            return []
    
    def _generate_title(self, topic: str, angle: str) -> str:
        """Generate a catchy title from topic and angle.
        
        Args:
            topic: Main topic
            angle: Content angle
        
        Returns:
            Generated title
        """
        # Simple title generation
        templates = [
            f"The Ultimate Guide to {topic}: {angle}",
            f"{topic}: {angle}",
            f"How {angle} is Transforming {topic}",
            f"Understanding {topic} Through {angle}",
            f"{angle}: A Deep Dive into {topic}"
        ]
        
        # Use first template for now
        return templates[0]
    
    def _get_fallback_trends(self, categories: List[str], limit: int) -> Dict[str, any]:
        """Generate fallback trends when AI fails.
        
        Args:
            categories: Categories to generate trends for
            limit: Number of trends to generate
        
        Returns:
            Fallback trends dictionary
        """
        fallback_trends = []
        
        for i, category in enumerate(categories[:limit]):
            fallback_trends.append({
                "topic": f"Latest Developments in {category}",
                "description": f"Recent advancements and trends in {category}",
                "why_trending": "Ongoing innovation and interest",
                "interest_level": "medium",
                "content_angles": [
                    f"Practical applications of {category}",
                    f"Future of {category}",
                    f"Beginner's guide to {category}"
                ],
                "keywords": [category, "trends", "innovation"],
                "hashtags": [f"#{category.replace(' ', '')}"],
                "longevity": "medium-term",
                "relevance_score": 0.6
            })
        
        return {
            "trends": fallback_trends,
            "discovered_at": datetime.now().isoformat(),
            "categories_analyzed": categories,
            "note": "Fallback trends - AI analysis unavailable"
        }
