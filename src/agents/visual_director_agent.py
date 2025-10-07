"""
Visual Director Agent for generating SEO-aligned media for Substack newsletters.

This agent analyzes article content and SEO metadata to generate optimized images
with SEO-friendly filenames, alt-text, and captions.
"""
import os
import re
import logging
import requests
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings
from content_generators.image_generator import ImageGenerator

logger = logging.getLogger(__name__)


class VisualDirectorAgent:
    """
    AI-powered Visual Director Agent for generating SEO-optimized media.
    
    This agent enhances image generation by:
    - Analyzing article content for SEO keywords and themes
    - Creating SEO-optimized image prompts
    - Generating SEO-friendly filenames
    - Creating descriptive alt-text for accessibility and SEO
    - Generating engaging captions
    """
    
    def __init__(self):
        """Initialize the Visual Director Agent."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.image_generator = ImageGenerator()
        self.output_dir = settings.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("Visual Director Agent initialized")
    
    def analyze_seo_metadata(self, title: str, content: str, tags: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Analyze article content to extract SEO-relevant metadata.
        
        Args:
            title: Article title
            content: Article content
            tags: Optional list of article tags
            
        Returns:
            Dictionary containing SEO metadata including keywords, themes, and focus areas
        """
        try:
            # Build tags context
            tags_context = ""
            if tags:
                tags_context = f"\nTags: {', '.join(tags)}"
            
            prompt = f"""
            Analyze this article for SEO and visual content purposes:
            
            Title: {title}
            Content: {content[:1000]}...
            {tags_context}
            
            Extract and return:
            1. Top 5 SEO keywords (single words or short phrases)
            2. Main theme/concept (one sentence)
            3. Target emotion/mood (e.g., innovative, inspiring, educational)
            4. Visual style recommendation (e.g., modern, professional, abstract)
            
            Return in this exact format:
            KEYWORDS: keyword1, keyword2, keyword3, keyword4, keyword5
            THEME: main theme description
            MOOD: target mood
            STYLE: visual style
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.5
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Parse the response
            metadata = self._parse_seo_analysis(analysis_text)
            metadata["title"] = title
            
            logger.info(f"SEO analysis completed: {len(metadata.get('keywords', []))} keywords extracted")
            return metadata
            
        except Exception as e:
            logger.error(f"Error analyzing SEO metadata: {e}")
            # Return basic metadata as fallback
            return {
                "title": title,
                "keywords": [],
                "theme": title,
                "mood": "professional",
                "style": "modern"
            }
    
    def _parse_seo_analysis(self, analysis_text: str) -> Dict[str, any]:
        """Parse the SEO analysis response into structured data."""
        metadata = {
            "keywords": [],
            "theme": "",
            "mood": "professional",
            "style": "modern"
        }
        
        lines = analysis_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("KEYWORDS:"):
                keywords_str = line.replace("KEYWORDS:", "").strip()
                metadata["keywords"] = [k.strip() for k in keywords_str.split(",") if k.strip()]
            elif line.startswith("THEME:"):
                metadata["theme"] = line.replace("THEME:", "").strip()
            elif line.startswith("MOOD:"):
                metadata["mood"] = line.replace("MOOD:", "").strip()
            elif line.startswith("STYLE:"):
                metadata["style"] = line.replace("STYLE:", "").strip()
        
        return metadata
    
    def generate_seo_friendly_filename(self, title: str, keywords: List[str]) -> str:
        """
        Generate an SEO-friendly filename.
        
        Args:
            title: Article title
            keywords: List of SEO keywords
            
        Returns:
            SEO-optimized filename (without extension)
        """
        # Combine title and top keywords
        combined = f"{title}"
        if keywords:
            combined += f" {' '.join(keywords[:3])}"
        
        # Clean and format for filename
        # Convert to lowercase
        filename = combined.lower()
        # Remove special characters, keep only alphanumeric, spaces, and hyphens
        filename = re.sub(r'[^a-z0-9\s-]', '', filename)
        # Replace spaces with hyphens
        filename = re.sub(r'\s+', '-', filename)
        # Remove duplicate hyphens
        filename = re.sub(r'-+', '-', filename)
        # Trim and limit length
        filename = filename.strip('-')[:80]
        
        return filename
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_alt_text(self, title: str, seo_metadata: Dict[str, any]) -> str:
        """
        Generate SEO-optimized alt text for an image.
        
        Args:
            title: Article title
            seo_metadata: SEO metadata dictionary
            
        Returns:
            Descriptive alt text optimized for SEO and accessibility
        """
        try:
            keywords = seo_metadata.get("keywords", [])
            theme = seo_metadata.get("theme", title)
            
            prompt = f"""
            Create descriptive alt text for an image that will illustrate this article:
            
            Title: {title}
            Theme: {theme}
            Keywords: {', '.join(keywords[:5])}
            
            Guidelines:
            - Be descriptive and specific (50-125 characters)
            - Include key concepts naturally
            - Focus on what the image depicts
            - Make it accessible and SEO-friendly
            - Don't start with "Image of" or "Picture of"
            
            Return only the alt text, nothing else.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            alt_text = response.choices[0].message.content.strip()
            # Remove quotes if present
            alt_text = alt_text.strip('"\'')
            
            logger.info(f"Generated alt text: {alt_text[:50]}...")
            return alt_text
            
        except Exception as e:
            logger.error(f"Error generating alt text: {e}")
            # Fallback to basic alt text
            return f"{title} - {seo_metadata.get('theme', 'illustration')}"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_caption(self, title: str, seo_metadata: Dict[str, any]) -> str:
        """
        Generate an engaging caption for the image.
        
        Args:
            title: Article title
            seo_metadata: SEO metadata dictionary
            
        Returns:
            Engaging caption text
        """
        try:
            theme = seo_metadata.get("theme", title)
            mood = seo_metadata.get("mood", "professional")
            
            prompt = f"""
            Create an engaging caption for an article image:
            
            Article Title: {title}
            Theme: {theme}
            Mood: {mood}
            
            Guidelines:
            - Keep it concise (1-2 sentences)
            - Make it engaging and relevant
            - Connect to the article theme
            - Professional tone
            
            Return only the caption text, nothing else.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8
            )
            
            caption = response.choices[0].message.content.strip()
            # Remove quotes if present
            caption = caption.strip('"\'')
            
            logger.info(f"Generated caption: {caption[:50]}...")
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            # Fallback to basic caption
            return f"Exploring {title}"
    
    def create_seo_optimized_prompt(self, title: str, content: str, seo_metadata: Dict[str, any]) -> str:
        """
        Create an image generation prompt optimized for SEO and content relevance.
        
        Args:
            title: Article title
            content: Article content
            seo_metadata: SEO metadata dictionary
            
        Returns:
            Enhanced image generation prompt
        """
        keywords = seo_metadata.get("keywords", [])
        theme = seo_metadata.get("theme", title)
        mood = seo_metadata.get("mood", "professional")
        style = seo_metadata.get("style", "modern")
        
        # Select image style from settings
        import random
        base_style = random.choice(settings.image_styles_list)
        
        prompt = f"""
        Create a {base_style} illustration for an article about: "{title}"
        
        Key Concepts: {', '.join(keywords[:5])}
        Theme: {theme}
        Visual Style: {style}, {base_style}
        Mood: {mood}, engaging, thoughtful
        
        Requirements:
        - Professional and high-quality
        - Clearly represents the main theme
        - Suitable for blog header/featured image
        - No text overlays
        - SEO-friendly visual composition
        
        The image should be visually compelling and immediately communicate the article's core concept.
        """
        
        return prompt
    
    def generate_seo_optimized_image(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        size: str = "1024x1024"
    ) -> Dict[str, any]:
        """
        Generate an SEO-optimized image with complete metadata.
        
        Args:
            title: Article title
            content: Article content
            tags: Optional list of article tags
            size: Image size (default: "1024x1024")
            
        Returns:
            Dictionary containing:
            - image_path: Path to generated image
            - filename: SEO-friendly filename
            - alt_text: SEO-optimized alt text
            - caption: Engaging caption
            - seo_metadata: Complete SEO analysis
            - keywords: List of SEO keywords
        """
        try:
            logger.info(f"Starting SEO-optimized image generation for: {title}")
            
            # Step 1: Analyze SEO metadata
            seo_metadata = self.analyze_seo_metadata(title, content, tags)
            
            # Step 2: Create optimized prompt
            optimized_prompt = self.create_seo_optimized_prompt(title, content, seo_metadata)
            
            # Step 3: Generate image using the base image generator
            logger.info("Generating image with SEO-optimized prompt...")
            response = self.image_generator.client.images.generate(
                model="dall-e-3",
                prompt=optimized_prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Step 4: Generate SEO-friendly filename
            seo_filename = self.generate_seo_friendly_filename(
                title,
                seo_metadata.get("keywords", [])
            )
            
            # Step 5: Download image with SEO filename
            filepath = os.path.join(self.output_dir, f"{seo_filename}.png")
            
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(image_response.content)
            
            logger.info(f"Image saved with SEO filename: {seo_filename}.png")
            
            # Step 6: Generate alt text and caption
            alt_text = self.generate_alt_text(title, seo_metadata)
            caption = self.generate_caption(title, seo_metadata)
            
            # Return complete metadata
            result = {
                "image_path": filepath,
                "filename": f"{seo_filename}.png",
                "alt_text": alt_text,
                "caption": caption,
                "seo_metadata": seo_metadata,
                "keywords": seo_metadata.get("keywords", []),
                "theme": seo_metadata.get("theme", ""),
                "mood": seo_metadata.get("mood", ""),
                "ai_generated": True
            }
            
            logger.info("SEO-optimized image generation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error generating SEO-optimized image: {e}")
            raise
    
    def generate_featured_image_with_seo(self, post_data: Dict) -> Dict[str, any]:
        """
        Generate a featured image with complete SEO optimization.
        
        This is a convenience method that integrates with the existing content pipeline.
        
        Args:
            post_data: Dictionary containing article data (title, content, tags)
            
        Returns:
            Dictionary with image path, metadata, and SEO information
        """
        try:
            title = post_data.get("title", "")
            content = post_data.get("content", "")
            tags = post_data.get("tags", [])
            
            # Generate SEO-optimized image
            result = self.generate_seo_optimized_image(title, content, tags)
            
            # Create thumbnail using base image generator
            thumbnail_path = self.image_generator.create_thumbnail(result["image_path"])
            result["thumbnail_path"] = thumbnail_path
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating featured image with SEO: {e}")
            return {"error": str(e)}
