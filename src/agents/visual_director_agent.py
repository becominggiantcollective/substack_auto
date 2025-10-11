"""
Visual Director Agent for SEO-aligned media generation.

This agent specializes in generating media (images, video thumbnails, etc.) 
that is optimized for SEO and content engagement in Substack newsletters.
"""
import os
import re
import logging
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
from PIL import Image

logger = logging.getLogger(__name__)


class VisualDirectorAgent:
    """
    AI agent that generates SEO-optimized media for blog posts.
    
    This agent analyzes article content and SEO metadata to guide image
    prompt generation, creates SEO-friendly filenames and alt-text,
    and outputs media assets with comprehensive metadata.
    """
    
    def __init__(self, api_key: Optional[str] = None, output_dir: Optional[str] = None):
        """Initialize the Visual Director Agent with OpenAI client.
        
        Args:
            api_key: OpenAI API key (defaults to settings.openai_api_key)
            output_dir: Output directory for images (defaults to settings.output_dir)
        """
        # Import settings here to avoid module-level import issues in tests
        from config.settings import settings
        
        self.client = OpenAI(api_key=api_key or settings.openai_api_key)
        self.output_dir = output_dir or settings.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # SEO best practices
        self.max_filename_length = 60
        self.max_alt_text_length = 125
        self.max_caption_length = 200
    
    def analyze_content_for_seo(self, title: str, content: str, tags: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Analyze article content to extract SEO metadata and keywords.
        
        Args:
            title: Article title
            content: Article content
            tags: Optional list of article tags
            
        Returns:
            Dictionary containing SEO analysis including keywords, themes, and focus
        """
        try:
            # Build analysis prompt
            tags_text = f"\nTags: {', '.join(tags)}" if tags else ""
            
            prompt = f"""
            Analyze this article for SEO and visual content planning:
            
            Title: {title}
            Content: {content[:1000]}...{tags_text}
            
            Provide a structured analysis with:
            1. Primary keywords (3-5 most important SEO keywords)
            2. Visual themes (what visual concepts would best represent this content)
            3. Target emotion (what feeling should the visual evoke)
            4. Key concepts (main ideas to visualize)
            5. SEO focus keyword (single most important keyword for SEO)
            
            Return as a structured format:
            PRIMARY_KEYWORDS: keyword1, keyword2, keyword3
            VISUAL_THEMES: theme1, theme2, theme3
            TARGET_EMOTION: emotion
            KEY_CONCEPTS: concept1, concept2, concept3
            SEO_FOCUS: focus_keyword
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.5
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Parse the structured response
            analysis = {
                "primary_keywords": self._extract_list(analysis_text, "PRIMARY_KEYWORDS"),
                "visual_themes": self._extract_list(analysis_text, "VISUAL_THEMES"),
                "target_emotion": self._extract_value(analysis_text, "TARGET_EMOTION"),
                "key_concepts": self._extract_list(analysis_text, "KEY_CONCEPTS"),
                "seo_focus": self._extract_value(analysis_text, "SEO_FOCUS")
            }
            
            logger.info(f"SEO analysis completed: focus='{analysis['seo_focus']}'")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing content for SEO: {e}")
            # Return fallback analysis
            return {
                "primary_keywords": [title.split()[0]] if title else ["content"],
                "visual_themes": ["professional", "modern"],
                "target_emotion": "engaged",
                "key_concepts": [title] if title else ["article"],
                "seo_focus": title.split()[0] if title else "content"
            }
    
    def _extract_list(self, text: str, key: str) -> List[str]:
        """Extract comma-separated list from analysis text."""
        pattern = f"{key}:\\s*(.+?)(?:\\n|$)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            items = match.group(1).split(",")
            return [item.strip() for item in items if item.strip()]
        return []
    
    def _extract_value(self, text: str, key: str) -> str:
        """Extract single value from analysis text."""
        pattern = f"{key}:\\s*(.+?)(?:\\n|$)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""
    
    def generate_seo_optimized_prompt(self, title: str, content: str, 
                                      seo_analysis: Dict[str, any],
                                      media_type: str = "featured") -> str:
        """
        Generate an image prompt optimized for SEO and engagement.
        
        Args:
            title: Article title
            content: Article content
            seo_analysis: SEO analysis from analyze_content_for_seo
            media_type: Type of media (featured, thumbnail, social, etc.)
            
        Returns:
            SEO-optimized image generation prompt
        """
        try:
            # Import settings here to avoid module-level issues
            from config.settings import settings
            
            # Extract SEO elements
            keywords = seo_analysis.get("primary_keywords", [])
            visual_themes = seo_analysis.get("visual_themes", [])
            emotion = seo_analysis.get("target_emotion", "professional")
            concepts = seo_analysis.get("key_concepts", [])
            
            # Build prompt based on media type
            if media_type == "featured":
                style = "professional, high-quality, blog header"
                composition = "wide composition suitable for article header"
                size_hint = "landscape orientation"
            elif media_type == "thumbnail":
                style = "clear, recognizable, compact"
                composition = "centered composition, simple and bold"
                size_hint = "small format, high impact"
            elif media_type == "social":
                style = "eye-catching, shareable, vibrant"
                composition = "social media optimized, engaging"
                size_hint = "horizontal layout"
            else:
                style = "professional, modern"
                composition = "balanced composition"
                size_hint = "versatile format"
            
            # Construct the optimized prompt
            prompt = f"""
            Create a {style} image representing: {title}
            
            Visual Concepts: {', '.join(concepts[:3])}
            Themes: {', '.join(visual_themes[:3])}
            Keywords to convey: {', '.join(keywords[:3])}
            Emotional tone: {emotion}
            
            Style: {style}
            Composition: {composition}
            Format: {size_hint}
            
            The image should be visually engaging, professional, and clearly communicate
            the article's main theme. No text overlays. High quality and suitable for
            {media_type} image use in blog posts and newsletters.
            """
            
            logger.info(f"Generated SEO-optimized prompt for {media_type} image")
            return prompt.strip()
            
        except Exception as e:
            logger.error(f"Error generating SEO prompt: {e}")
            # Fallback to basic prompt
            return f"Create a professional illustration representing: {title}"
    
    def generate_seo_filename(self, title: str, seo_focus: str, media_type: str = "image") -> str:
        """
        Generate an SEO-friendly filename.
        
        Args:
            title: Article title
            seo_focus: Primary SEO focus keyword
            media_type: Type of media
            
        Returns:
            SEO-optimized filename
        """
        # Combine title and focus keyword
        combined = f"{seo_focus} {title}".lower()
        
        # Clean and format for SEO
        # Remove special characters, keep only alphanumeric, spaces, and hyphens
        cleaned = re.sub(r'[^\w\s-]', '', combined)
        # Replace spaces and underscores with hyphens
        cleaned = re.sub(r'[\s_]+', '-', cleaned)
        # Remove multiple consecutive hyphens
        cleaned = re.sub(r'-+', '-', cleaned)
        # Trim hyphens from ends
        cleaned = cleaned.strip('-')
        
        # Truncate to max length while preserving word boundaries
        if len(cleaned) > self.max_filename_length:
            cleaned = cleaned[:self.max_filename_length].rsplit('-', 1)[0]
        
        # Add media type prefix
        filename = f"{media_type}-{cleaned}.png"
        
        logger.info(f"Generated SEO filename: {filename}")
        return filename
    
    def generate_alt_text(self, title: str, seo_analysis: Dict[str, any], 
                         media_type: str = "featured") -> str:
        """
        Generate SEO-optimized alt text for accessibility and search engines.
        
        Args:
            title: Article title
            seo_analysis: SEO analysis data
            media_type: Type of media
            
        Returns:
            SEO-optimized alt text
        """
        try:
            keywords = seo_analysis.get("primary_keywords", [])
            focus = seo_analysis.get("seo_focus", "")
            concepts = seo_analysis.get("key_concepts", [])
            
            # Build descriptive alt text
            if media_type == "featured":
                alt_base = f"Featured image for article about {focus}"
            elif media_type == "thumbnail":
                alt_base = f"Thumbnail image showing {focus}"
            elif media_type == "social":
                alt_base = f"Social media image for {focus}"
            else:
                alt_base = f"Image about {focus}"
            
            # Add key concepts for context
            if concepts:
                alt_text = f"{alt_base} - {concepts[0]}"
            else:
                alt_text = alt_base
            
            # Add primary keyword if space allows
            if keywords and len(alt_text) < self.max_alt_text_length - 20:
                keyword = keywords[0]
                if keyword.lower() not in alt_text.lower():
                    alt_text = f"{alt_text} - {keyword}"
            
            # Ensure it's within limits
            if len(alt_text) > self.max_alt_text_length:
                alt_text = alt_text[:self.max_alt_text_length-3] + "..."
            
            logger.info(f"Generated alt text: {alt_text[:50]}...")
            return alt_text
            
        except Exception as e:
            logger.error(f"Error generating alt text: {e}")
            return f"Image for article: {title[:50]}"
    
    def generate_caption(self, title: str, seo_analysis: Dict[str, any]) -> str:
        """
        Generate an engaging, SEO-friendly caption for the image.
        
        Args:
            title: Article title
            seo_analysis: SEO analysis data
            
        Returns:
            SEO-optimized caption
        """
        try:
            keywords = seo_analysis.get("primary_keywords", [])
            emotion = seo_analysis.get("target_emotion", "")
            
            prompt = f"""
            Write a brief, engaging caption (1-2 sentences, max {self.max_caption_length} characters) 
            for an image accompanying this article: "{title}"
            
            Include these keywords naturally: {', '.join(keywords[:2])}
            Tone: {emotion}, engaging
            
            The caption should entice readers and support SEO. Return only the caption.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            caption = response.choices[0].message.content.strip()
            
            # Ensure within length limit
            if len(caption) > self.max_caption_length:
                caption = caption[:self.max_caption_length-3] + "..."
            
            logger.info(f"Generated caption: {caption[:50]}...")
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            return f"Explore {title}"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_seo_optimized_image(self, title: str, content: str,
                                    tags: Optional[List[str]] = None,
                                    media_type: str = "featured",
                                    size: str = "1024x1024") -> Optional[Dict[str, any]]:
        """
        Generate a complete SEO-optimized image with metadata.
        
        Args:
            title: Article title
            content: Article content
            tags: Optional article tags
            media_type: Type of media to generate
            size: Image size
            
        Returns:
            Dictionary with image path and SEO metadata, or None on failure
        """
        try:
            logger.info(f"Generating SEO-optimized {media_type} image for: {title[:50]}...")
            
            # Step 1: Analyze content for SEO
            seo_analysis = self.analyze_content_for_seo(title, content, tags)
            
            # Step 2: Generate SEO-optimized prompt
            prompt = self.generate_seo_optimized_prompt(title, content, seo_analysis, media_type)
            
            # Step 3: Generate image using DALL-E
            logger.info(f"Calling DALL-E with SEO-optimized prompt...")
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Step 4: Generate SEO-friendly filename
            filename = self.generate_seo_filename(title, seo_analysis.get("seo_focus", "article"), media_type)
            filepath = os.path.join(self.output_dir, filename)
            
            # Step 5: Download and save the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(image_response.content)
            
            # Step 6: Generate SEO metadata
            alt_text = self.generate_alt_text(title, seo_analysis, media_type)
            caption = self.generate_caption(title, seo_analysis)
            
            # Compile result with comprehensive metadata
            result = {
                "image_path": filepath,
                "filename": filename,
                "alt_text": alt_text,
                "caption": caption,
                "seo_metadata": {
                    "focus_keyword": seo_analysis.get("seo_focus", ""),
                    "keywords": seo_analysis.get("primary_keywords", []),
                    "visual_themes": seo_analysis.get("visual_themes", []),
                    "target_emotion": seo_analysis.get("target_emotion", ""),
                },
                "media_type": media_type,
                "size": size,
                "ai_generated": True,
                "seo_optimized": True
            }
            
            logger.info(f"Successfully generated SEO-optimized image: {filename}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating SEO-optimized image: {e}")
            return None
    
    def generate_image_set(self, title: str, content: str, 
                          tags: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Generate a complete set of SEO-optimized images for an article.
        
        Includes: featured image, thumbnail, and social media image.
        
        Args:
            title: Article title
            content: Article content
            tags: Optional article tags
            
        Returns:
            Dictionary with all generated images and metadata
        """
        try:
            logger.info(f"Generating complete image set for: {title[:50]}...")
            
            # Analyze once for all images
            seo_analysis = self.analyze_content_for_seo(title, content, tags)
            
            result = {
                "seo_analysis": seo_analysis,
                "images": {}
            }
            
            # Generate featured image
            logger.info("Generating featured image...")
            featured = self.generate_seo_optimized_image(
                title, content, tags, 
                media_type="featured", 
                size="1024x1024"
            )
            if featured:
                result["images"]["featured"] = featured
            
            # Generate thumbnail
            logger.info("Generating thumbnail image...")
            thumbnail = self.generate_seo_optimized_image(
                title, content, tags,
                media_type="thumbnail",
                size="1024x1024"
            )
            if thumbnail:
                result["images"]["thumbnail"] = thumbnail
                
                # Create smaller thumbnail version
                try:
                    thumb_path = self._create_thumbnail_size(thumbnail["image_path"])
                    result["images"]["thumbnail"]["thumbnail_path"] = thumb_path
                except Exception as e:
                    logger.warning(f"Could not create small thumbnail: {e}")
            
            # Generate social media image
            logger.info("Generating social media image...")
            social = self.generate_seo_optimized_image(
                title, content, tags,
                media_type="social",
                size="1024x1024"
            )
            if social:
                result["images"]["social"] = social
            
            result["success"] = len(result["images"]) > 0
            result["images_generated"] = len(result["images"])
            
            logger.info(f"Image set generation complete: {len(result['images'])} images generated")
            return result
            
        except Exception as e:
            logger.error(f"Error generating image set: {e}")
            return {
                "success": False,
                "error": str(e),
                "images": {}
            }
    
    def _create_thumbnail_size(self, image_path: str, size: Tuple[int, int] = (400, 300)) -> str:
        """
        Create a smaller thumbnail version of an image.
        
        Args:
            image_path: Path to original image
            size: Desired thumbnail size
            
        Returns:
            Path to thumbnail image
        """
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                thumbnail_path = os.path.join(self.output_dir, f"{base_name}_small.png")
                
                img.save(thumbnail_path, "PNG")
                
                return thumbnail_path
                
        except Exception as e:
            logger.error(f"Error creating thumbnail size: {e}")
            return image_path
    
    def get_seo_report(self, result: Dict[str, any]) -> str:
        """
        Generate a human-readable SEO report for generated images.
        
        Args:
            result: Result dictionary from generate_image_set or generate_seo_optimized_image
            
        Returns:
            Formatted SEO report string
        """
        report = ["=== SEO-Optimized Media Report ===\n"]
        
        if "seo_analysis" in result:
            analysis = result["seo_analysis"]
            report.append("SEO Analysis:")
            report.append(f"  Focus Keyword: {analysis.get('seo_focus', 'N/A')}")
            report.append(f"  Primary Keywords: {', '.join(analysis.get('primary_keywords', []))}")
            report.append(f"  Visual Themes: {', '.join(analysis.get('visual_themes', []))}")
            report.append(f"  Target Emotion: {analysis.get('target_emotion', 'N/A')}")
            report.append("")
        
        if "images" in result:
            report.append(f"Images Generated: {len(result['images'])}")
            for media_type, image_data in result["images"].items():
                report.append(f"\n{media_type.upper()} Image:")
                report.append(f"  Filename: {image_data.get('filename', 'N/A')}")
                report.append(f"  Alt Text: {image_data.get('alt_text', 'N/A')}")
                report.append(f"  Caption: {image_data.get('caption', 'N/A')[:60]}...")
        elif "filename" in result:
            # Single image report
            report.append(f"\nFilename: {result.get('filename', 'N/A')}")
            report.append(f"Alt Text: {result.get('alt_text', 'N/A')}")
            report.append(f"Caption: {result.get('caption', 'N/A')}")
        
        return "\n".join(report)
