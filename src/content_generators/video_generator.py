"""
AI-powered video generation for blog posts.
"""
import os
import logging
from typing import Optional, Dict, List
from PIL import Image, ImageDraw, ImageFont
import random

try:
    from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, TextClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    logging.warning("MoviePy not available, video generation will be disabled")

from config.settings import settings

logger = logging.getLogger(__name__)


class VideoGenerator:
    """AI-powered video generator for blog post content."""
    
    def __init__(self):
        """Initialize the video generator."""
        self.output_dir = settings.output_dir
        self.video_duration = settings.video_duration
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_title_slide(self, title: str, subtitle: str) -> str:
        """Create a title slide image."""
        try:
            # Create image dimensions
            width, height = 1920, 1080
            
            # Create a new image with a gradient background
            img = Image.new('RGB', (width, height), color='#1a1a2e')
            draw = ImageDraw.Draw(img)
            
            # Create gradient effect
            for i in range(height):
                color_value = int(26 + (i / height) * 30)  # Gradient from dark to slightly lighter
                color = (color_value, color_value, color_value + 20)
                draw.line([(0, i), (width, i)], fill=color)
            
            # Try to load a font, fall back to default if not available
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
                subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Calculate text positions for centering
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            
            # Draw title
            title_x = (width - title_width) // 2
            title_y = height // 2 - 80
            draw.text((title_x, title_y), title, font=title_font, fill='#ffffff')
            
            # Draw subtitle
            subtitle_x = (width - subtitle_width) // 2
            subtitle_y = title_y + title_height + 30
            draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill='#cccccc')
            
            # Save the title slide
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:30]
            slide_path = os.path.join(self.output_dir, f"title_slide_{safe_title}.png")
            img.save(slide_path)
            
            return slide_path
            
        except Exception as e:
            logger.error(f"Error creating title slide: {e}")
            # Create a simple fallback slide
            return self._create_simple_slide(title, subtitle)
    
    def _create_simple_slide(self, title: str, subtitle: str) -> str:
        """Create a simple fallback title slide."""
        try:
            img = Image.new('RGB', (1920, 1080), color='#2c3e50')
            draw = ImageDraw.Draw(img)
            
            # Use default font
            font = ImageFont.load_default()
            
            # Simple centered text
            draw.text((100, 400), title, font=font, fill='white')
            draw.text((100, 500), subtitle, font=font, fill='lightgray')
            
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:30]
            slide_path = os.path.join(self.output_dir, f"simple_slide_{safe_title}.png")
            img.save(slide_path)
            
            return slide_path
            
        except Exception as e:
            logger.error(f"Error creating simple slide: {e}")
            raise
    
    def create_content_slides(self, content: str, num_slides: int = 3) -> List[str]:
        """Create content slides from the blog post content."""
        try:
            # Split content into key points
            sentences = content.split('.')
            sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
            
            # Select key sentences for slides
            if len(sentences) > num_slides:
                step = len(sentences) // num_slides
                selected_sentences = [sentences[i * step] for i in range(num_slides)]
            else:
                selected_sentences = sentences[:num_slides]
            
            slide_paths = []
            
            for i, sentence in enumerate(selected_sentences):
                slide_path = self._create_content_slide(sentence, i + 1)
                slide_paths.append(slide_path)
            
            return slide_paths
            
        except Exception as e:
            logger.error(f"Error creating content slides: {e}")
            return []
    
    def _create_content_slide(self, text: str, slide_number: int) -> str:
        """Create a single content slide."""
        try:
            img = Image.new('RGB', (1920, 1080), color='#34495e')
            draw = ImageDraw.Draw(img)
            
            # Try to load font
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Wrap text to fit slide
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                if len(test_line) > 40:  # Approximate character limit per line
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text lines
            y_start = 300
            line_height = 80
            
            for i, line in enumerate(lines[:6]):  # Limit to 6 lines
                y_pos = y_start + i * line_height
                draw.text((100, y_pos), line, font=font, fill='white')
            
            # Save slide
            slide_path = os.path.join(self.output_dir, f"content_slide_{slide_number}.png")
            img.save(slide_path)
            
            return slide_path
            
        except Exception as e:
            logger.error(f"Error creating content slide: {e}")
            raise
    
    def create_video_from_images(self, image_paths: List[str], title: str) -> Optional[str]:
        """Create a video from a list of images."""
        if not MOVIEPY_AVAILABLE:
            logger.warning("MoviePy not available, skipping video creation")
            return None
            
        try:
            if not image_paths:
                logger.warning("No images provided for video creation")
                return None
            
            # Calculate duration per image
            duration_per_image = self.video_duration / len(image_paths)
            
            # Create video clips from images
            clips = []
            for image_path in image_paths:
                if os.path.exists(image_path):
                    clip = ImageClip(image_path, duration=duration_per_image)
                    clips.append(clip)
                else:
                    logger.warning(f"Image not found: {image_path}")
            
            if not clips:
                logger.error("No valid images found for video creation")
                return None
            
            # Concatenate clips
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Create output filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:30]
            video_path = os.path.join(self.output_dir, f"video_{safe_title}.mp4")
            
            # Write video file
            final_video.write_videofile(
                video_path,
                fps=1,  # Low FPS for slideshow style
                codec='libx264',
                audio=False,
                verbose=False,
                logger=None
            )
            
            # Clean up
            final_video.close()
            for clip in clips:
                clip.close()
            
            logger.info(f"Created video: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return None
    
    def generate_blog_video(self, post_data: Dict, featured_image_path: Optional[str] = None) -> Dict[str, str]:
        """Generate a complete video for a blog post."""
        try:
            # Create title slide
            title_slide = self.create_title_slide(post_data["title"], post_data["subtitle"])
            
            # Create content slides
            content_slides = self.create_content_slides(post_data["content"])
            
            # Combine all slides
            all_slides = [title_slide] + content_slides
            
            # Add featured image if available
            if featured_image_path and os.path.exists(featured_image_path):
                all_slides.append(featured_image_path)
            
            # Create video
            video_path = self.create_video_from_images(all_slides, post_data["title"])
            
            if video_path:
                return {
                    "video_path": video_path,
                    "slides_created": len(all_slides),
                    "duration": self.video_duration,
                    "ai_generated": True
                }
            else:
                return {"error": "Failed to create video"}
                
        except Exception as e:
            logger.error(f"Error generating blog video: {e}")
            return {"error": str(e)}