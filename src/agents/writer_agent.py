"""
Writer Agent for generating SEO-optimized Substack newsletter articles.

This agent accepts research summaries and keywords, then generates engaging
articles with proper SEO integration, structure, and readability.
"""
import logging
import re
from typing import Dict, List, Optional
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)


class WriterAgent:
    """AI-powered writer agent for SEO-optimized content generation."""
    
    def __init__(self):
        """Initialize the writer agent with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4"
        self.target_word_count_min = 800
        self.target_word_count_max = 1200
        self.target_keyword_density = 0.02  # 2% keyword density
    
    def calculate_keyword_density(self, content: str, keyword: str) -> float:
        """
        Calculate the density of a keyword in the content.
        
        Args:
            content: The article content
            keyword: The keyword to check
            
        Returns:
            Keyword density as a float (e.g., 0.02 for 2%)
        """
        content_lower = content.lower()
        keyword_lower = keyword.lower()
        
        # Count total words
        words = content_lower.split()
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        # Count keyword occurrences (handle multi-word keywords)
        keyword_count = content_lower.count(keyword_lower)
        
        return keyword_count / total_words
    
    def _build_writing_prompt(
        self,
        topic: str,
        keywords: List[str],
        research_summary: Optional[str] = None
    ) -> str:
        """
        Build the writing prompt for the AI.
        
        Args:
            topic: The main topic/title for the article
            keywords: List of SEO keywords to integrate
            research_summary: Optional research summary to inform the article
            
        Returns:
            The formatted prompt for article generation
        """
        # Build custom requirements
        custom_requirements = []
        if settings.content_style:
            custom_requirements.append(f"- Style: {settings.content_style}")
        if settings.content_tone:
            custom_requirements.append(f"- Tone: {settings.content_tone}")
        if settings.target_audience:
            custom_requirements.append(f"- Target audience: {settings.target_audience}")
        if settings.custom_instructions:
            custom_requirements.append(f"- Additional instructions: {settings.custom_instructions}")
        
        requirements_text = "\n        ".join(custom_requirements) if custom_requirements else "- Informative and engaging\n        - Professional tone\n        - General educated audience"
        
        # Format keywords
        primary_keyword = keywords[0] if keywords else topic
        secondary_keywords = keywords[1:5] if len(keywords) > 1 else []
        
        keyword_text = f"Primary keyword: {primary_keyword}"
        if secondary_keywords:
            keyword_text += f"\n        Secondary keywords: {', '.join(secondary_keywords)}"
        
        research_context = ""
        if research_summary:
            research_context = f"""
        
        Research Summary:
        {research_summary}
        
        Use this research as background information to inform your article."""
        
        prompt = f"""
        Write a comprehensive, SEO-optimized blog article about: "{topic}"
        
        SEO Keywords to integrate naturally:
        {keyword_text}
        
        Requirements:
        - Word count: {self.target_word_count_min}-{self.target_word_count_max} words
        - Integrate the primary keyword naturally throughout (aim for ~2% density)
        - Include secondary keywords where relevant and natural
        - Well-structured with clear sections and logical flow
        - Engaging introduction that hooks the reader
        - Informative body with practical insights
        - Strong conclusion with key takeaways
        - Use subheadings to organize content
        - Write for readability and engagement
        {requirements_text}
        {research_context}
        
        Important: 
        - Do NOT force keywords unnaturally - maintain readability
        - Do NOT include a title at the top - just the article content
        - Use markdown formatting for structure (## for headers)
        - Focus on providing genuine value to readers
        
        Write the complete article now:
        """
        
        return prompt
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_article(
        self,
        topic: str,
        keywords: List[str],
        research_summary: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Generate a complete SEO-optimized article.
        
        Args:
            topic: The main topic/title for the article
            keywords: List of SEO keywords to integrate
            research_summary: Optional research summary to inform the article
            
        Returns:
            Dictionary containing the article and metadata:
            - title: Article title
            - content: Main article content
            - word_count: Number of words
            - keyword_density: Density of primary keyword
            - keywords_used: Keywords that appear in the content
        """
        try:
            # Build and execute the writing prompt
            prompt = self._build_writing_prompt(topic, keywords, research_summary)
            
            logger.info(f"Generating article for topic: {topic}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            word_count = len(content.split())
            
            # Calculate keyword metrics
            primary_keyword = keywords[0] if keywords else topic
            keyword_density = self.calculate_keyword_density(content, primary_keyword)
            
            # Check which keywords appear in the content
            keywords_used = [kw for kw in keywords if kw.lower() in content.lower()]
            
            logger.info(f"Generated article: {word_count} words, keyword density: {keyword_density:.2%}")
            
            return {
                "title": topic,
                "content": content,
                "word_count": word_count,
                "keyword_density": keyword_density,
                "keywords_used": keywords_used
            }
            
        except Exception as e:
            logger.error(f"Error generating article: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_meta_description(self, title: str, content: str, keywords: List[str]) -> str:
        """
        Generate an SEO-optimized meta description.
        
        Args:
            title: The article title
            content: The article content
            keywords: List of keywords to consider
            
        Returns:
            Meta description (150-160 characters)
        """
        primary_keyword = keywords[0] if keywords else title
        
        prompt = f"""
        Create an SEO-optimized meta description for this article:
        
        Title: {title}
        Primary Keyword: {primary_keyword}
        Content Preview: {content[:300]}...
        
        Requirements:
        - Length: 150-160 characters
        - Include the primary keyword naturally
        - Compelling and action-oriented
        - Summarize the article's value proposition
        
        Return only the meta description, nothing else.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            meta_description = response.choices[0].message.content.strip()
            
            # Ensure it's within character limits
            if len(meta_description) > 160:
                meta_description = meta_description[:157] + "..."
            
            return meta_description
            
        except Exception as e:
            logger.error(f"Error generating meta description: {e}")
            # Fallback to a simple description
            return f"{title} - {content[:120]}..."[:160]
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_meta_title(self, title: str, keywords: List[str]) -> str:
        """
        Generate an SEO-optimized meta title.
        
        Args:
            title: The original article title
            keywords: List of keywords to consider
            
        Returns:
            SEO-optimized meta title (50-60 characters)
        """
        primary_keyword = keywords[0] if keywords else ""
        
        prompt = f"""
        Create an SEO-optimized meta title based on this article title:
        
        Original Title: {title}
        Primary Keyword: {primary_keyword}
        
        Requirements:
        - Length: 50-60 characters optimal (max 70)
        - Include the primary keyword if not already present
        - Compelling and click-worthy
        - Accurate representation of content
        
        Return only the meta title, nothing else.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.7
            )
            
            meta_title = response.choices[0].message.content.strip()
            
            # Ensure it's within character limits
            if len(meta_title) > 70:
                meta_title = meta_title[:67] + "..."
            
            return meta_title
            
        except Exception as e:
            logger.error(f"Error generating meta title: {e}")
            # Fallback to original title
            return title[:70]
    
    def generate_tags(self, title: str, content: str, keywords: List[str]) -> List[str]:
        """
        Generate relevant tags for the article.
        
        Args:
            title: The article title
            content: The article content
            keywords: List of keywords
            
        Returns:
            List of 5-8 relevant tags
        """
        prompt = f"""
        Generate relevant tags for this article:
        
        Title: {title}
        Keywords: {', '.join(keywords)}
        Content Preview: {content[:400]}...
        
        Requirements:
        - 5-8 tags total
        - Include primary keywords as tags
        - Add related topics and categories
        - Single words or short phrases
        - Relevant for content discovery
        
        Return only the tags as a comma-separated list, nothing else.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.6
            )
            
            tags_text = response.choices[0].message.content.strip()
            tags = [tag.strip() for tag in tags_text.split(",")]
            
            # Ensure we have 5-8 tags
            tags = tags[:8]
            
            # Add primary keywords if not already in tags
            for keyword in keywords[:3]:
                if keyword not in tags and len(tags) < 8:
                    tags.append(keyword)
            
            return tags
            
        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            # Fallback to keywords
            return keywords[:8]
    
    def create_complete_article(
        self,
        topic: str,
        keywords: List[str],
        research_summary: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Generate a complete article with all SEO metadata.
        
        Args:
            topic: The main topic/title for the article
            keywords: List of SEO keywords to integrate
            research_summary: Optional research summary to inform the article
            
        Returns:
            Complete article package with:
            - title: Article title
            - content: Main article content
            - meta_title: SEO-optimized meta title
            - meta_description: SEO-optimized meta description
            - tags: Suggested tags for the article
            - word_count: Number of words
            - keyword_density: Density of primary keyword
            - keywords_used: Keywords that appear in the content
            - seo_optimized: Boolean flag
        """
        try:
            # Generate the main article
            article_data = self.generate_article(topic, keywords, research_summary)
            
            logger.info(f"Generating SEO metadata for article: {topic}")
            
            # Generate SEO metadata
            meta_title = self.generate_meta_title(article_data["title"], keywords)
            meta_description = self.generate_meta_description(
                article_data["title"],
                article_data["content"],
                keywords
            )
            tags = self.generate_tags(
                article_data["title"],
                article_data["content"],
                keywords
            )
            
            # Compile complete package
            complete_article = {
                "title": article_data["title"],
                "content": article_data["content"],
                "meta_title": meta_title,
                "meta_description": meta_description,
                "tags": tags,
                "word_count": article_data["word_count"],
                "keyword_density": article_data["keyword_density"],
                "keywords_used": article_data["keywords_used"],
                "seo_optimized": True,
                "ai_generated": True
            }
            
            logger.info(
                f"Complete article generated: {article_data['word_count']} words, "
                f"{len(article_data['keywords_used'])}/{len(keywords)} keywords used"
            )
            
            return complete_article
            
        except Exception as e:
            logger.error(f"Error creating complete article: {e}")
            raise
