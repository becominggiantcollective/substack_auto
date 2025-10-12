"""
Writer Agent for SEO-optimized content generation.

This agent generates engaging newsletter articles with SEO keyword integration,
proper content structure, and readability optimization.
"""
import logging
import re
from typing import Dict, List, Optional
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)


class WriterAgent:
    """
    AI-powered Writer Agent for generating SEO-optimized newsletter articles.
    
    This agent accepts research input (topic, keywords, summary) and generates
    comprehensive draft articles optimized for SEO with proper keyword density,
    structure, and readability.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the Writer Agent with OpenAI client.
        
        Args:
            openai_api_key: Optional OpenAI API key. If not provided, uses settings.
        """
        api_key = openai_api_key or settings.openai_api_key
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
        self.target_word_count_min = 800
        self.target_word_count_max = 1200
        self.target_keyword_density = 0.02  # 2% keyword density target (maximum)
        
    def calculate_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, float]:
        """
        Calculate keyword density for each keyword in the content.
        
        Args:
            content: The article content
            keywords: List of keywords to check
            
        Returns:
            Dictionary mapping keywords to their density percentages
        """
        content_lower = content.lower()
        total_words = len(content.split())
        
        if total_words == 0:
            return {keyword: 0.0 for keyword in keywords}
        
        keyword_densities = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Count occurrences (case-insensitive)
            count = content_lower.count(keyword_lower)
            density = count / total_words if total_words > 0 else 0.0
            keyword_densities[keyword] = density
            
        return keyword_densities
    
    def validate_content_structure(self, content: str) -> Dict[str, bool]:
        """
        Validate that the content has proper structure.
        
        Args:
            content: The article content
            
        Returns:
            Dictionary with validation results
        """
        validations = {
            "has_paragraphs": len(content.split("\n\n")) >= 3,
            "has_sufficient_length": self.target_word_count_min <= len(content.split()) <= self.target_word_count_max,
            "has_opening": len(content.split("\n\n")[0].split()) >= 30 if content else False,
            "has_sections": len(content.split("\n")) >= 5,
        }
        
        return validations
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_article(
        self,
        topic: str,
        keywords: List[str],
        research_summary: str,
        target_word_count: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Generate an SEO-optimized article based on research input.
        
        Args:
            topic: The main topic/title for the article
            keywords: List of SEO keywords to integrate
            research_summary: Summary of research findings to base the article on
            target_word_count: Optional specific target word count (defaults to 800-1200)
            
        Returns:
            Dictionary containing:
                - article: The generated article content
                - word_count: Actual word count
                - keyword_densities: Density for each keyword
                - structure_validation: Structure validation results
        """
        if target_word_count is None:
            target_word_count = (self.target_word_count_min + self.target_word_count_max) // 2
        
        # Build custom requirements
        custom_requirements = []
        if settings.content_style:
            custom_requirements.append(f"- Style: {settings.content_style}")
        if settings.content_tone:
            custom_requirements.append(f"- Tone: {settings.content_tone}")
        if settings.target_audience:
            custom_requirements.append(f"- Audience: {settings.target_audience}")
        if settings.custom_instructions:
            custom_requirements.append(f"- {settings.custom_instructions}")
        
        requirements_text = "\n        ".join(custom_requirements) if custom_requirements else ""
        
        # Build keyword integration guidance
        keywords_text = ", ".join(keywords[:10])  # Limit to top 10 keywords
        
        prompt = f"""
        Write a comprehensive, SEO-optimized blog article based on the following:
        
        Topic: {topic}
        
        SEO Keywords to integrate naturally: {keywords_text}
        
        Research Summary:
        {research_summary}
        
        Requirements:
        - Target word count: approximately {target_word_count} words (between {self.target_word_count_min}-{self.target_word_count_max})
        - Integrate the SEO keywords naturally throughout the content (maximum 2% keyword density - do not exceed this to avoid robotic tone)
        - Use clear, engaging structure with proper paragraphs
        - Include an engaging opening paragraph that hooks the reader
        - Organize content into logical sections with smooth transitions
        - Ensure readability and flow
        - Make the content informative, valuable, and actionable
        {requirements_text}
        
        Format Guidelines:
        - Use paragraphs separated by double line breaks
        - Do NOT include a title at the top (title will be added separately)
        - Focus on clear, concise writing with strong topic sentences
        - Include relevant examples or insights where appropriate
        
        Write the article now:
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1800,
                temperature=0.7
            )
            
            article_content = response.choices[0].message.content.strip()
            word_count = len(article_content.split())
            
            # Calculate keyword densities
            keyword_densities = self.calculate_keyword_density(article_content, keywords)
            
            # Validate structure
            structure_validation = self.validate_content_structure(article_content)
            
            logger.info(f"Generated article with {word_count} words")
            logger.info(f"Keyword densities: {keyword_densities}")
            logger.info(f"Structure validation: {structure_validation}")
            
            return {
                "article": article_content,
                "word_count": word_count,
                "keyword_densities": keyword_densities,
                "structure_validation": structure_validation
            }
            
        except Exception as e:
            logger.error(f"Error generating article: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_meta_title(self, topic: str, keywords: List[str]) -> str:
        """
        Generate an SEO-optimized meta title.
        
        Args:
            topic: The article topic
            keywords: List of SEO keywords
            
        Returns:
            Meta title string (optimized for ~60 characters)
        """
        primary_keywords = keywords[:3] if len(keywords) >= 3 else keywords
        keywords_text = ", ".join(primary_keywords)
        
        prompt = f"""
        Create an SEO-optimized meta title for an article about: {topic}
        
        Include these primary keywords naturally: {keywords_text}
        
        Requirements:
        - Maximum 60 characters (including spaces)
        - Compelling and click-worthy
        - Include primary keyword near the beginning
        - Clear and descriptive
        
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
            # Ensure it's within character limit
            if len(meta_title) > 60:
                meta_title = meta_title[:57] + "..."
                
            logger.info(f"Generated meta title: {meta_title} ({len(meta_title)} chars)")
            return meta_title
            
        except Exception as e:
            logger.error(f"Error generating meta title: {e}")
            # Fallback to simple title
            return topic[:60]
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_meta_description(self, topic: str, keywords: List[str], article_preview: str) -> str:
        """
        Generate an SEO-optimized meta description.
        
        Args:
            topic: The article topic
            keywords: List of SEO keywords
            article_preview: Preview/snippet of the article content
            
        Returns:
            Meta description string (optimized for ~155 characters)
        """
        primary_keywords = keywords[:3] if len(keywords) >= 3 else keywords
        keywords_text = ", ".join(primary_keywords)
        
        # Get first ~200 words of article for context
        preview_words = article_preview.split()[:200]
        preview = " ".join(preview_words)
        
        prompt = f"""
        Create an SEO-optimized meta description for an article about: {topic}
        
        Article preview:
        {preview}
        
        Include these keywords naturally: {keywords_text}
        
        Requirements:
        - Maximum 155 characters (including spaces)
        - Compelling and descriptive
        - Include primary keyword
        - Include a call-to-action or value proposition
        - Summarize the key benefit or insight
        
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
            # Ensure it's within character limit
            if len(meta_description) > 155:
                meta_description = meta_description[:152] + "..."
                
            logger.info(f"Generated meta description: {meta_description} ({len(meta_description)} chars)")
            return meta_description
            
        except Exception as e:
            logger.error(f"Error generating meta description: {e}")
            # Fallback to simple description
            return f"Learn about {topic}. Discover insights on {keywords[0] if keywords else 'this topic'}."[:155]
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_tags(self, topic: str, keywords: List[str], article: str) -> List[str]:
        """
        Generate suggested tags for the article.
        
        Args:
            topic: The article topic
            keywords: List of SEO keywords
            article: The article content
            
        Returns:
            List of 5-8 suggested tags
        """
        # Combine keywords with article context
        article_preview = " ".join(article.split()[:300])
        keywords_text = ", ".join(keywords[:10])
        
        prompt = f"""
        Based on this article topic, keywords, and content, generate 5-8 relevant tags:
        
        Topic: {topic}
        Keywords: {keywords_text}
        Article preview: {article_preview}
        
        Requirements:
        - Tags should be single words or short phrases (1-3 words)
        - Include primary keywords as tags
        - Add related topical tags
        - Keep tags specific and relevant
        - Format as comma-separated list
        
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
            # Limit to 8 tags and ensure uniqueness
            tags = list(dict.fromkeys(tags))[:8]
            
            logger.info(f"Generated tags: {tags}")
            return tags
            
        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            # Fallback to using keywords as tags
            return keywords[:8]
    
    def create_complete_content(
        self,
        topic: str,
        keywords: List[str],
        research_summary: str,
        target_word_count: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Generate complete SEO-optimized content package.
        
        This is the main method that generates all content components:
        - Article content
        - Meta title
        - Meta description
        - Suggested tags
        - SEO analytics (keyword densities, structure validation)
        
        Args:
            topic: The main topic/title for the article
            keywords: List of SEO keywords to integrate
            research_summary: Summary of research findings
            target_word_count: Optional specific target word count
            
        Returns:
            Dictionary containing all generated content and metadata:
                - title: The article title
                - article: The article content
                - meta_title: SEO-optimized meta title
                - meta_description: SEO-optimized meta description
                - tags: List of suggested tags
                - word_count: Actual word count
                - keyword_densities: Density analysis for each keyword
                - structure_validation: Content structure validation results
                - seo_score: Overall SEO quality score (0-100)
        """
        try:
            logger.info(f"Starting content generation for topic: {topic}")
            logger.info(f"Keywords: {keywords}")
            
            # Generate main article
            article_result = self.generate_article(
                topic=topic,
                keywords=keywords,
                research_summary=research_summary,
                target_word_count=target_word_count
            )
            
            # Generate meta title
            meta_title = self.generate_meta_title(topic, keywords)
            
            # Generate meta description
            meta_description = self.generate_meta_description(
                topic=topic,
                keywords=keywords,
                article_preview=article_result["article"]
            )
            
            # Generate tags
            tags = self.generate_tags(
                topic=topic,
                keywords=keywords,
                article=article_result["article"]
            )
            
            # Calculate overall SEO score
            seo_score = self._calculate_seo_score(
                article_result["keyword_densities"],
                article_result["structure_validation"],
                article_result["word_count"]
            )
            
            result = {
                "title": topic,
                "article": article_result["article"],
                "meta_title": meta_title,
                "meta_description": meta_description,
                "tags": tags,
                "word_count": article_result["word_count"],
                "keyword_densities": article_result["keyword_densities"],
                "structure_validation": article_result["structure_validation"],
                "seo_score": seo_score,
                "ai_generated": True
            }
            
            logger.info(f"Content generation complete. SEO score: {seo_score}/100")
            return result
            
        except Exception as e:
            logger.error(f"Error creating complete content: {e}")
            raise
    
    def _calculate_seo_score(
        self,
        keyword_densities: Dict[str, float],
        structure_validation: Dict[str, bool],
        word_count: int
    ) -> int:
        """
        Calculate an overall SEO quality score (0-100).
        
        Args:
            keyword_densities: Keyword density analysis
            structure_validation: Structure validation results
            word_count: Article word count
            
        Returns:
            SEO score from 0-100
        """
        score = 0
        
        # Word count score (30 points max)
        if self.target_word_count_min <= word_count <= self.target_word_count_max:
            score += 30
        elif word_count >= self.target_word_count_min:
            score += 20
        else:
            score += 10
        
        # Keyword density score (40 points max)
        if keyword_densities:
            avg_density = sum(keyword_densities.values()) / len(keyword_densities)
            # Optimal density is 1.5-2% (maximum 2% to avoid robotic tone)
            if 0.015 <= avg_density <= 0.020:  # 1.5% - 2.0% (optimal)
                score += 40
            elif 0.01 <= avg_density <= 0.025:  # 1% - 2.5% (acceptable)
                score += 30
            elif avg_density > 0.025:  # Above 2.5% (penalized for robotic tone)
                score += 10
            elif avg_density > 0:
                score += 20
        
        # Structure score (30 points max)
        structure_score = sum(1 for valid in structure_validation.values() if valid)
        max_structure_checks = len(structure_validation)
        if max_structure_checks > 0:
            score += int((structure_score / max_structure_checks) * 30)
        
        return min(score, 100)
