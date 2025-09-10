"""
AI-powered text content generation for blog posts.
"""
import random
import logging
from typing import Dict, List, Optional
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)


class TextGenerator:
    """AI-powered text content generator for Substack posts."""
    
    def __init__(self):
        """Initialize the text generator with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_topic(self) -> str:
        """Generate a creative topic for a blog post."""
        base_topics = settings.topics_list
        selected_topic = random.choice(base_topics)
        
        # Build custom instructions for topic generation
        custom_guidance = []
        if settings.target_audience:
            custom_guidance.append(f"- Suitable for {settings.target_audience}")
        if settings.content_tone:
            custom_guidance.append(f"- Written in a {settings.content_tone} tone")
        if settings.custom_instructions:
            custom_guidance.append(f"- {settings.custom_instructions}")
        
        guidance_text = "\n        ".join(custom_guidance) if custom_guidance else "- Suitable for an intelligent audience"
        
        prompt = f"""
        Generate a specific, engaging topic for a blog post about {selected_topic}.
        The topic should be:
        - Current and relevant
        - Thought-provoking
        - Not overly technical
        {guidance_text}
        
        Return only the topic title, nothing else.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating topic: {e}")
            # Fallback to a default topic
            return f"The Future of {selected_topic.title()}: What's Next?"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_blog_post(self, topic: str) -> Dict[str, str]:
        """Generate a complete blog post for the given topic."""
        
        # Build custom requirements for blog post generation
        custom_requirements = []
        if settings.content_style:
            custom_requirements.append(f"- {settings.content_style.title()}")
        if settings.content_tone:
            custom_requirements.append(f"- Written in a {settings.content_tone} tone")
        if settings.target_audience:
            custom_requirements.append(f"- Suitable for {settings.target_audience}")
        if settings.custom_instructions:
            custom_requirements.append(f"- {settings.custom_instructions}")
        
        requirements_text = "\n        ".join(custom_requirements) if custom_requirements else "- Informative and thought-provoking\n        - Written in an accessible but intelligent tone\n        - Suitable for a general but educated audience"
        
        # Generate the main content
        content_prompt = f"""
        Write a comprehensive, engaging blog post about: "{topic}"
        
        The blog post should be:
        - Well-structured with clear sections
        - Between 800-1200 words
        - Include practical insights or takeaways
        {requirements_text}
        
        Format the response as a complete blog post with paragraphs.
        Do not include a title at the top - just the content.
        """
        
        # Generate a subtitle/description
        subtitle_prompt = f"""
        Create a compelling subtitle or brief description (1-2 sentences) for a blog post titled: "{topic}"
        The subtitle should capture the essence of the post and entice readers.
        {f"Write in a {settings.content_tone} tone" if settings.content_tone else ""}
        Return only the subtitle, nothing else.
        """
        
        try:
            # Generate main content
            content_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": content_prompt}],
                max_tokens=1500,
                temperature=0.7
            )
            
            # Generate subtitle
            subtitle_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": subtitle_prompt}],
                max_tokens=100,
                temperature=0.8
            )
            
            return {
                "title": topic,
                "subtitle": subtitle_response.choices[0].message.content.strip(),
                "content": content_response.choices[0].message.content.strip(),
                "word_count": len(content_response.choices[0].message.content.split())
            }
            
        except Exception as e:
            logger.error(f"Error generating blog post: {e}")
            raise
    
    def generate_tags(self, title: str, content: str) -> List[str]:
        """Generate relevant tags for the blog post."""
        prompt = f"""
        Based on this blog post title and content, generate 5-8 relevant tags:
        
        Title: {title}
        Content: {content[:500]}...
        
        Return only the tags as a comma-separated list, nothing else.
        Tags should be single words or short phrases, relevant and specific.
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
            return tags[:8]  # Limit to 8 tags
            
        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            # Return default tags based on configured topics
            return settings.topics_list[:5]
    
    def create_complete_post(self) -> Dict[str, any]:
        """Generate a complete blog post with all components."""
        try:
            # Generate topic
            topic = self.generate_topic()
            logger.info(f"Generated topic: {topic}")
            
            # Generate blog post content
            post_data = self.generate_blog_post(topic)
            logger.info(f"Generated blog post with {post_data['word_count']} words")
            
            # Generate tags
            tags = self.generate_tags(post_data["title"], post_data["content"])
            logger.info(f"Generated tags: {tags}")
            
            return {
                "title": post_data["title"],
                "subtitle": post_data["subtitle"],
                "content": post_data["content"],
                "tags": tags,
                "word_count": post_data["word_count"],
                "ai_generated": True
            }
            
        except Exception as e:
            logger.error(f"Error creating complete post: {e}")
            raise