"""
AI-powered image generation for blog posts.
"""
import os
import random
import logging
from typing import Optional, Dict
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
from PIL import Image

from config.settings import settings

logger = logging.getLogger(__name__)


class ImageGenerator:
    """AI-powered image generator for blog post visuals."""
    
    def __init__(self):
        """Initialize the image generator with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.output_dir = settings.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _create_image_prompt(self, title: str, content: str) -> str:
        """Create an effective prompt for image generation."""
        # Extract key concepts from the title and content
        style = random.choice(settings.image_styles_list)
        
        # Create a focused prompt
        prompt = f"""
        Create a {style} illustration representing the concept: "{title}"
        
        Style: {style}, clean, professional, engaging
        Mood: Innovative, modern, thoughtful
        Colors: Professional color palette
        Composition: Suitable for blog header image
        
        The image should visually represent the main theme without text overlays.
        """
        
        return prompt
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_image(self, title: str, content: str, size: str = "1024x1024") -> Optional[str]:
        """Generate an image for the blog post."""
        try:
            # Create the prompt
            prompt = self._create_image_prompt(title, content)
            logger.info(f"Generating image with prompt: {prompt[:100]}...")
            
            # Generate image using DALL-E
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            # Get the image URL
            image_url = response.data[0].url
            
            # Download and save the image
            image_filename = self._download_image(image_url, title)
            
            logger.info(f"Generated and saved image: {image_filename}")
            return image_filename
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
    
    def _download_image(self, image_url: str, title: str) -> str:
        """Download image from URL and save locally."""
        try:
            # Create a safe filename from the title
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
            filename = f"image_{safe_title}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            raise
    
    def create_thumbnail(self, image_path: str, size: tuple = (400, 300)) -> str:
        """Create a thumbnail version of the image."""
        try:
            with Image.open(image_path) as img:
                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Create thumbnail filename
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                thumbnail_path = os.path.join(self.output_dir, f"{base_name}_thumb.png")
                
                # Save thumbnail
                img.save(thumbnail_path, "PNG")
                
                return thumbnail_path
                
        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            return image_path  # Return original if thumbnail creation fails
    
    def generate_featured_image(self, post_data: Dict) -> Dict[str, str]:
        """Generate a featured image for a blog post."""
        try:
            # Generate the main image
            image_path = self.generate_image(
                post_data["title"], 
                post_data["content"]
            )
            
            if not image_path:
                return {"error": "Failed to generate image"}
            
            # Create thumbnail
            thumbnail_path = self.create_thumbnail(image_path)
            
            return {
                "image_path": image_path,
                "thumbnail_path": thumbnail_path,
                "ai_generated": True
            }
            
        except Exception as e:
            logger.error(f"Error generating featured image: {e}")
            return {"error": str(e)}
    
    def generate_social_media_image(self, title: str, size: str = "1024x512") -> Optional[str]:
        """Generate a social media optimized image."""
        try:
            # Create a social media specific prompt
            style = random.choice(settings.image_styles_list)
            prompt = f"""
            Create a {style} social media image for: "{title}"
            
            Style: {style}, eye-catching, professional
            Format: Horizontal layout suitable for social media
            Text: No text overlay needed
            Colors: Vibrant but professional
            
            The image should be engaging and shareable.
            """
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Create filename for social media image
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]
            filename = f"social_{safe_title}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating social media image: {e}")
            return None