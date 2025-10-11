# Visual Director Agent Documentation

## Overview

The Visual Director Agent is a specialized AI agent designed to generate SEO-optimized media for blog posts and newsletters. It analyzes article content and SEO metadata to create images that are not only visually engaging but also optimized for search engines and content discoverability.

## Features

- **SEO Content Analysis**: Extracts keywords, themes, and concepts from article content
- **SEO-Optimized Image Prompts**: Generates image generation prompts aligned with SEO strategy
- **Intelligent Filename Generation**: Creates SEO-friendly filenames with proper formatting
- **Alt-Text Generation**: Produces accessible, SEO-optimized alt text for images
- **Caption Generation**: Creates engaging captions that incorporate keywords naturally
- **Multiple Media Types**: Supports featured images, thumbnails, and social media images
- **Comprehensive Metadata**: Outputs detailed SEO metadata with each generated image
- **Complete Image Sets**: Can generate all required images for an article in one call

## Installation

The Visual Director Agent is included in the standard installation. Ensure you have all dependencies installed:

```bash
pip install -r requirements.txt
```

Required environment variables:
```env
OPENAI_API_KEY=your_openai_api_key_here
OUTPUT_DIR=generated_content
```

## Usage

### Basic Usage

```python
from agents.visual_director_agent import VisualDirectorAgent

# Initialize the agent
agent = VisualDirectorAgent()

# Generate a single SEO-optimized image
result = agent.generate_seo_optimized_image(
    title="The Future of Artificial Intelligence",
    content="Full article content here...",
    tags=["AI", "technology", "innovation"],
    media_type="featured",
    size="1024x1024"
)

# Access the generated image and metadata
print(f"Image saved to: {result['image_path']}")
print(f"Alt text: {result['alt_text']}")
print(f"Caption: {result['caption']}")
print(f"SEO focus keyword: {result['seo_metadata']['focus_keyword']}")
```

### Generate Complete Image Set

```python
# Generate featured, thumbnail, and social media images
image_set = agent.generate_image_set(
    title="The Future of Artificial Intelligence",
    content="Full article content here...",
    tags=["AI", "technology", "innovation"]
)

# Check results
if image_set["success"]:
    print(f"Generated {image_set['images_generated']} images")
    
    # Access featured image
    featured = image_set["images"]["featured"]
    print(f"Featured image: {featured['filename']}")
    print(f"Alt text: {featured['alt_text']}")
    
    # Access thumbnail
    thumbnail = image_set["images"]["thumbnail"]
    print(f"Thumbnail: {thumbnail['filename']}")
    
    # Access social media image
    social = image_set["images"]["social"]
    print(f"Social image: {social['filename']}")
```

### SEO Analysis Only

```python
# Analyze content for SEO without generating images
seo_analysis = agent.analyze_content_for_seo(
    title="The Future of AI",
    content="Article content...",
    tags=["AI", "technology"]
)

print(f"Focus keyword: {seo_analysis['seo_focus']}")
print(f"Primary keywords: {seo_analysis['primary_keywords']}")
print(f"Visual themes: {seo_analysis['visual_themes']}")
print(f"Target emotion: {seo_analysis['target_emotion']}")
```

### Generate SEO Report

```python
# Generate a readable SEO report
result = agent.generate_image_set(title, content, tags)
report = agent.get_seo_report(result)
print(report)
```

Output:
```
=== SEO-Optimized Media Report ===

SEO Analysis:
  Focus Keyword: artificial intelligence
  Primary Keywords: AI, machine learning, technology
  Visual Themes: futuristic, modern, digital
  Target Emotion: inspired

Images Generated: 3

FEATURED Image:
  Filename: featured-artificial-intelligence-future-of-ai.png
  Alt Text: Featured image for article about artificial intelligence - AI advancement
  Caption: Discover how AI is reshaping our future with innovative technology...

THUMBNAIL Image:
  Filename: thumbnail-artificial-intelligence-future-of-ai.png
  Alt Text: Thumbnail image showing artificial intelligence - AI advancement
  Caption: Explore the cutting-edge world of AI technology...

SOCIAL Image:
  Filename: social-artificial-intelligence-future-of-ai.png
  Alt Text: Social media image for artificial intelligence - AI advancement
  Caption: Dive into the revolutionary world of artificial intelligence...
```

## Integration with Existing Code

### Integration with ImageGenerator

Replace or supplement the existing `ImageGenerator` with the Visual Director Agent:

```python
from agents.visual_director_agent import VisualDirectorAgent

class ContentOrchestrator:
    def __init__(self):
        # Use Visual Director Agent instead of or alongside ImageGenerator
        self.visual_director = VisualDirectorAgent()
        # ... other generators
    
    def generate_complete_content(self):
        # Generate text content
        post_data = self.text_generator.create_complete_post()
        
        # Generate SEO-optimized images
        image_set = self.visual_director.generate_image_set(
            title=post_data["title"],
            content=post_data["content"],
            tags=post_data.get("tags", [])
        )
        
        # Use the generated images
        if image_set["success"]:
            return {
                "post_data": post_data,
                "media_files": {
                    "featured_image": image_set["images"]["featured"],
                    "thumbnail": image_set["images"]["thumbnail"],
                    "social_image": image_set["images"]["social"]
                },
                "seo_metadata": image_set["seo_analysis"]
            }
```

### Integration with SubstackPublisher

Include SEO metadata when publishing:

```python
def publish_with_seo(self, content):
    # Extract SEO-optimized image metadata
    featured_image = content["media_files"]["featured_image"]
    
    # Use SEO-friendly filenames and alt text
    post_html = f"""
    <img src="{featured_image['image_path']}" 
         alt="{featured_image['alt_text']}"
         title="{featured_image['caption']}">
    """
    
    # Include caption with keywords
    post_html += f"<p><em>{featured_image['caption']}</em></p>"
    
    # Publish with optimized metadata
    self.publish(post_html)
```

## API Reference

### VisualDirectorAgent

#### `__init__()`
Initializes the Visual Director Agent with OpenAI client.

#### `analyze_content_for_seo(title, content, tags=None)`
Analyzes article content to extract SEO metadata.

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `tags` (list, optional): Article tags

**Returns:**
- dict: SEO analysis containing keywords, themes, emotion, concepts, and focus keyword

#### `generate_seo_optimized_prompt(title, content, seo_analysis, media_type='featured')`
Generates an SEO-optimized image generation prompt.

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `seo_analysis` (dict): SEO analysis from `analyze_content_for_seo`
- `media_type` (str): Type of media ('featured', 'thumbnail', 'social')

**Returns:**
- str: Optimized prompt for image generation

#### `generate_seo_filename(title, seo_focus, media_type='image')`
Generates an SEO-friendly filename.

**Parameters:**
- `title` (str): Article title
- `seo_focus` (str): Primary SEO focus keyword
- `media_type` (str): Type of media

**Returns:**
- str: SEO-optimized filename

#### `generate_alt_text(title, seo_analysis, media_type='featured')`
Generates SEO-optimized alt text for accessibility and search engines.

**Parameters:**
- `title` (str): Article title
- `seo_analysis` (dict): SEO analysis data
- `media_type` (str): Type of media

**Returns:**
- str: SEO-optimized alt text

#### `generate_caption(title, seo_analysis)`
Generates an engaging, SEO-friendly caption.

**Parameters:**
- `title` (str): Article title
- `seo_analysis` (dict): SEO analysis data

**Returns:**
- str: SEO-optimized caption

#### `generate_seo_optimized_image(title, content, tags=None, media_type='featured', size='1024x1024')`
Generates a complete SEO-optimized image with metadata.

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `tags` (list, optional): Article tags
- `media_type` (str): Type of media
- `size` (str): Image size

**Returns:**
- dict: Image data with path, filename, alt text, caption, and SEO metadata

#### `generate_image_set(title, content, tags=None)`
Generates a complete set of SEO-optimized images (featured, thumbnail, social).

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `tags` (list, optional): Article tags

**Returns:**
- dict: Complete image set with all images and metadata

#### `get_seo_report(result)`
Generates a human-readable SEO report.

**Parameters:**
- `result` (dict): Result from image generation

**Returns:**
- str: Formatted SEO report

## SEO Best Practices

### Filename Guidelines
- Uses hyphens (not underscores or spaces)
- Includes focus keyword early in filename
- Keeps filename under 60 characters
- Uses lowercase for consistency
- Removes special characters

**Good examples:**
- `featured-artificial-intelligence-future-trends.png`
- `thumbnail-machine-learning-guide-beginners.png`
- `social-ai-technology-innovation-2024.png`

**Bad examples:**
- `image_12345.png` (no keywords)
- `The Future of AI!!! (Final) v2.png` (special chars, spaces)
- `very-long-filename-that-goes-on-forever-with-too-many-words.png` (too long)

### Alt Text Guidelines
- Describes image content clearly
- Includes primary focus keyword
- Under 125 characters for optimal SEO
- Written naturally, not keyword-stuffed
- Provides context for visually impaired users

**Good examples:**
- "Featured image for article about artificial intelligence - machine learning concepts"
- "Thumbnail showing AI technology innovation and future trends"

**Bad examples:**
- "Image123.png" (not descriptive)
- "AI AI AI technology AI artificial intelligence AI AI" (keyword stuffing)
- "This is a very long description that goes into too much detail..." (too long)

### Caption Guidelines
- Engaging and encourages interaction
- Naturally incorporates keywords
- Under 200 characters
- Complements article content
- Can include call-to-action

**Good examples:**
- "Discover how artificial intelligence is transforming industries through machine learning and innovation."
- "Explore the cutting-edge world of AI technology and its impact on our future."

## Configuration

The Visual Director Agent uses settings from `config/settings.py`:

```python
# Relevant settings
OPENAI_API_KEY=your_key_here
OUTPUT_DIR=generated_content
IMAGE_STYLE=digital art,modern,professional  # Influences visual style
```

### Customizing SEO Behavior

You can customize the agent's behavior by modifying class attributes:

```python
agent = VisualDirectorAgent()
agent.max_filename_length = 80  # Increase max filename length
agent.max_alt_text_length = 150  # Increase alt text length
agent.max_caption_length = 250  # Increase caption length
```

## Performance Considerations

### API Calls
Each `generate_seo_optimized_image()` call makes:
- 1 call for SEO analysis (GPT-4)
- 1 call for image generation (DALL-E 3)
- 1 call for caption generation (GPT-4)

Each `generate_image_set()` call makes:
- 1 call for SEO analysis (shared across all images)
- 3 calls for image generation (featured, thumbnail, social)
- 3 calls for caption generation

### Cost Optimization
- Reuse SEO analysis when generating multiple images for the same article
- Cache analysis results if generating images at different times
- Consider batch processing for multiple articles

### Rate Limiting
The agent includes retry logic with exponential backoff:
- 3 retry attempts
- Exponential wait time between retries
- Handles API rate limits gracefully

## Troubleshooting

### Issue: Images not optimized for SEO

**Solution:** Ensure article content and tags are meaningful:
```python
# Provide detailed content and relevant tags
result = agent.generate_seo_optimized_image(
    title="Detailed, descriptive title",
    content="Full article content with keywords...",  # Not just excerpt
    tags=["relevant", "specific", "tags"]
)
```

### Issue: Filenames too long or contain invalid characters

**Solution:** The agent automatically handles this, but you can adjust:
```python
agent.max_filename_length = 50  # Reduce max length
```

### Issue: Alt text doesn't include key concepts

**Solution:** Improve SEO analysis by providing more context:
```python
# Provide more detailed article content
seo_analysis = agent.analyze_content_for_seo(
    title=full_title,
    content=complete_article_text,  # Full text, not summary
    tags=comprehensive_tag_list
)
```

### Issue: API errors or timeouts

**Solution:** Check your OpenAI API key and rate limits:
```python
# Verify API key
import os
print(os.getenv('OPENAI_API_KEY'))

# Check retry configuration
from tenacity import retry, stop_after_attempt, wait_exponential
```

## Testing

Run the test suite:

```bash
# Run all Visual Director Agent tests
python -m pytest tests/test_visual_director_agent.py -v

# Run specific test
python -m pytest tests/test_visual_director_agent.py::TestVisualDirectorAgent::test_generate_seo_optimized_image -v

# Run with coverage
python -m pytest tests/test_visual_director_agent.py --cov=agents.visual_director_agent
```

Or use unittest:

```bash
python tests/test_visual_director_agent.py
```

## Examples

### Example 1: Generate Featured Image Only

```python
from agents.visual_director_agent import VisualDirectorAgent

agent = VisualDirectorAgent()

result = agent.generate_seo_optimized_image(
    title="10 Machine Learning Tips for Beginners",
    content="""
    Machine learning is revolutionizing technology. Here are 10 essential
    tips for beginners starting their journey in ML and AI...
    """,
    tags=["machine learning", "AI", "beginner guide"],
    media_type="featured"
)

if result:
    print(f"✓ Image saved: {result['filename']}")
    print(f"✓ Alt text: {result['alt_text']}")
    print(f"✓ SEO focus: {result['seo_metadata']['focus_keyword']}")
```

### Example 2: Generate All Images for Blog Post

```python
agent = VisualDirectorAgent()

# Generate complete image set
images = agent.generate_image_set(
    title="The Complete Guide to Neural Networks",
    content=article_text,
    tags=["neural networks", "deep learning", "AI"]
)

# Use in blog post
if images["success"]:
    # Featured image for article header
    featured_img = images["images"]["featured"]
    
    # Thumbnail for article list
    thumb_img = images["images"]["thumbnail"]
    
    # Social media sharing
    social_img = images["images"]["social"]
    
    # Generate report
    print(agent.get_seo_report(images))
```

### Example 3: Custom Integration

```python
class MyContentGenerator:
    def __init__(self):
        self.visual_director = VisualDirectorAgent()
    
    def create_post_with_seo_images(self, topic):
        # Generate content
        content = self.generate_content(topic)
        
        # Generate SEO-optimized images
        images = self.visual_director.generate_image_set(
            title=content["title"],
            content=content["body"],
            tags=content["tags"]
        )
        
        # Combine for publishing
        return {
            "title": content["title"],
            "body": content["body"],
            "featured_image": images["images"]["featured"]["image_path"],
            "featured_alt": images["images"]["featured"]["alt_text"],
            "thumbnail": images["images"]["thumbnail"]["image_path"],
            "seo_keywords": images["seo_analysis"]["primary_keywords"]
        }
```

## Future Enhancements

Planned features for future versions:

- [ ] Support for video thumbnail generation with SEO metadata
- [ ] A/B testing for image prompts to optimize engagement
- [ ] Integration with image CDNs for automatic optimization
- [ ] Multilingual SEO support for international content
- [ ] Advanced analytics for image performance tracking
- [ ] Custom style profiles for brand consistency
- [ ] Automatic image schema markup generation
- [ ] Integration with Stable Diffusion and other image APIs

## Support

For issues, questions, or contributions:

1. Check the test suite for usage examples
2. Review the API documentation above
3. Check logs in the output directory
4. Open an issue on GitHub with details about your use case

## License

The Visual Director Agent is part of the Substack Auto project and is licensed under the MIT License.
