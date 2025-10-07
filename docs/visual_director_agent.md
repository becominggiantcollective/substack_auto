# Visual Director Agent Documentation

## Overview

The Visual Director Agent is an AI-powered system that generates SEO-optimized media for Substack newsletters. It analyzes article content and SEO metadata to create images with optimized filenames, alt-text, and captions that improve content engagement and search engine visibility.

## Features

- **SEO Metadata Analysis**: Automatically extracts keywords, themes, and mood from article content
- **Smart Image Generation**: Creates visually compelling images aligned with article themes
- **SEO-Friendly Filenames**: Generates descriptive filenames using keywords and article titles
- **Optimized Alt Text**: Creates accessible, SEO-friendly alt text (50-125 characters)
- **Engaging Captions**: Generates professional captions that connect to the article theme
- **Full Metadata Output**: Provides complete SEO data for publishing workflows

## Installation

The Visual Director Agent is included in the Substack Auto system. Ensure you have all dependencies installed:

```bash
pip install -r requirements.txt
```

Required environment variables:
```bash
OPENAI_API_KEY=your_openai_api_key
OUTPUT_DIR=generated_content  # Optional, defaults to "generated_content"
```

## Usage

### Basic Usage

```python
from agents.visual_director_agent import VisualDirectorAgent

# Initialize the agent
visual_director = VisualDirectorAgent()

# Generate SEO-optimized image
result = visual_director.generate_seo_optimized_image(
    title="The Future of Artificial Intelligence",
    content="Long-form article content...",
    tags=["AI", "technology", "innovation"]
)

# Access the results
image_path = result["image_path"]
alt_text = result["alt_text"]
caption = result["caption"]
keywords = result["keywords"]
```

### Integration with Content Pipeline

```python
from agents.visual_director_agent import VisualDirectorAgent

visual_director = VisualDirectorAgent()

# Use with existing post data
post_data = {
    "title": "Article Title",
    "content": "Article content...",
    "tags": ["tag1", "tag2"]
}

result = visual_director.generate_featured_image_with_seo(post_data)

# Result includes:
# - image_path: Full path to the generated image
# - thumbnail_path: Path to thumbnail version
# - filename: SEO-friendly filename
# - alt_text: Optimized alt text
# - caption: Engaging caption
# - keywords: List of SEO keywords
# - seo_metadata: Complete SEO analysis
```

### Standalone SEO Analysis

```python
# Analyze content without generating images
seo_metadata = visual_director.analyze_seo_metadata(
    title="Your Article Title",
    content="Your article content...",
    tags=["optional", "tags"]
)

# Returns:
# {
#     "title": "Your Article Title",
#     "keywords": ["keyword1", "keyword2", ...],
#     "theme": "Main theme description",
#     "mood": "professional",
#     "style": "modern"
# }
```

### Generate Components Separately

```python
# Generate SEO-friendly filename
filename = visual_director.generate_seo_friendly_filename(
    title="Article Title",
    keywords=["AI", "machine learning", "innovation"]
)
# Returns: "article-title-ai-machine-learning-innovation"

# Generate alt text
alt_text = visual_director.generate_alt_text(
    title="Article Title",
    seo_metadata=seo_metadata
)

# Generate caption
caption = visual_director.generate_caption(
    title="Article Title",
    seo_metadata=seo_metadata
)
```

## Output Structure

When generating an SEO-optimized image, the Visual Director Agent returns:

```python
{
    "image_path": "/path/to/generated_content/seo-friendly-filename.png",
    "thumbnail_path": "/path/to/generated_content/seo-friendly-filename_thumb.png",
    "filename": "seo-friendly-filename.png",
    "alt_text": "Descriptive alt text optimized for SEO and accessibility",
    "caption": "Engaging caption connecting to the article theme",
    "seo_metadata": {
        "title": "Article Title",
        "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
        "theme": "Main theme or concept of the article",
        "mood": "professional",
        "style": "modern"
    },
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "theme": "Main theme description",
    "mood": "professional",
    "ai_generated": true
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OUTPUT_DIR`: Directory for generated images (default: "generated_content")
- `IMAGE_STYLE`: Comma-separated list of preferred image styles (default: "digital art,modern,professional")

### Image Sizes

Supported image sizes:
- `1024x1024`: Square (default)
- `1024x1792`: Portrait
- `1792x1024`: Landscape

Example:
```python
result = visual_director.generate_seo_optimized_image(
    title="Article Title",
    content="Content...",
    size="1792x1024"  # Landscape format
)
```

## SEO Best Practices

### Filenames
The agent automatically creates SEO-friendly filenames by:
- Converting title and keywords to lowercase
- Replacing spaces with hyphens
- Removing special characters
- Limiting length to 80 characters
- Including top 3 relevant keywords

Example: `future-artificial-intelligence-ai-machine-learning.png`

### Alt Text
Alt text is optimized for:
- **Length**: 50-125 characters (SEO sweet spot)
- **Descriptiveness**: Specific and informative
- **Keyword Integration**: Natural inclusion of relevant keywords
- **Accessibility**: Clear description for screen readers
- **No Redundancy**: Avoids phrases like "image of" or "picture of"

### Captions
Captions are designed to:
- Be concise (1-2 sentences)
- Connect to the article theme
- Maintain a professional tone
- Engage readers
- Complement the alt text without duplication

## Integration Examples

### With Content Orchestrator

```python
from main import ContentOrchestrator
from agents.visual_director_agent import VisualDirectorAgent

class EnhancedOrchestrator(ContentOrchestrator):
    def __init__(self):
        super().__init__()
        self.visual_director = VisualDirectorAgent()
    
    def generate_complete_content(self):
        # Generate text content
        post_data = self.text_generator.create_complete_post()
        
        # Generate SEO-optimized image
        image_result = self.visual_director.generate_featured_image_with_seo(post_data)
        
        # Continue with video and publishing...
        return {
            "post_data": post_data,
            "media_files": {
                "image_path": image_result["image_path"],
                "thumbnail_path": image_result["thumbnail_path"],
                "alt_text": image_result["alt_text"],
                "caption": image_result["caption"]
            },
            "seo_metadata": image_result["seo_metadata"]
        }
```

### Batch Processing

```python
posts = [
    {"title": "Post 1", "content": "Content 1...", "tags": ["tag1"]},
    {"title": "Post 2", "content": "Content 2...", "tags": ["tag2"]},
]

visual_director = VisualDirectorAgent()

for post in posts:
    result = visual_director.generate_featured_image_with_seo(post)
    print(f"Generated: {result['filename']}")
    print(f"Alt text: {result['alt_text']}")
    print(f"Keywords: {', '.join(result['keywords'])}")
    print("---")
```

## Error Handling

The Visual Director Agent includes retry logic and fallback mechanisms:

```python
try:
    result = visual_director.generate_seo_optimized_image(
        title="Article Title",
        content="Content..."
    )
except Exception as e:
    logger.error(f"Error generating image: {e}")
    # Fallback to basic image generator if needed
```

Key error scenarios:
- **API failures**: Automatic retry with exponential backoff (up to 3 attempts)
- **Invalid content**: Returns basic metadata with error details
- **Missing dependencies**: Clear error messages with resolution steps

## Performance Considerations

- **API Calls**: The agent makes multiple OpenAI API calls per image (SEO analysis + image generation + alt text + caption)
- **Processing Time**: Expect 10-30 seconds per image depending on API response times
- **Cost**: Uses GPT-3.5-turbo for analysis (cheaper) and DALL-E 3 for generation
- **Caching**: Consider implementing caching for repeated content analysis

## Troubleshooting

### Common Issues

**Issue**: Images not generating
- **Check**: OpenAI API key is valid and has credits
- **Check**: OUTPUT_DIR is writable
- **Solution**: Verify environment variables and permissions

**Issue**: SEO analysis returns empty keywords
- **Check**: Article content has sufficient text (minimum 100 characters recommended)
- **Solution**: The agent falls back to basic metadata; ensure content is substantial

**Issue**: Filename too long or contains invalid characters
- **Check**: Article title length and special characters
- **Solution**: Agent automatically truncates to 80 characters and removes invalid chars

## API Reference

### VisualDirectorAgent Class

#### `__init__()`
Initialize the Visual Director Agent.

#### `analyze_seo_metadata(title, content, tags=None)`
Analyze article content for SEO metadata.

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `tags` (list, optional): Article tags

**Returns:** Dictionary with keywords, theme, mood, and style

#### `generate_seo_optimized_image(title, content, tags=None, size="1024x1024")`
Generate a complete SEO-optimized image with metadata.

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `tags` (list, optional): Article tags
- `size` (str, optional): Image size

**Returns:** Dictionary with image path, metadata, and SEO information

#### `generate_featured_image_with_seo(post_data)`
Convenience method for generating featured images.

**Parameters:**
- `post_data` (dict): Dictionary with title, content, and optional tags

**Returns:** Dictionary with image path, thumbnail, and complete metadata

#### `generate_seo_friendly_filename(title, keywords)`
Generate an SEO-friendly filename.

**Parameters:**
- `title` (str): Article title
- `keywords` (list): List of keywords

**Returns:** SEO-optimized filename string

#### `generate_alt_text(title, seo_metadata)`
Generate SEO-optimized alt text.

**Parameters:**
- `title` (str): Article title
- `seo_metadata` (dict): SEO metadata dictionary

**Returns:** Alt text string

#### `generate_caption(title, seo_metadata)`
Generate an engaging caption.

**Parameters:**
- `title` (str): Article title
- `seo_metadata` (dict): SEO metadata dictionary

**Returns:** Caption text string

## Future Enhancements

Potential improvements for future versions:
- Multi-image generation with variations
- A/B testing support for different visual styles
- Integration with image optimization tools
- Analytics tracking for image performance
- Custom SEO rule configurations
- Bulk processing with parallel execution

## Support

For issues, questions, or contributions:
- Check existing documentation
- Review error logs for specific issues
- Ensure all dependencies are up to date
- Verify API keys and credentials

## License

Part of the Substack Auto project. See main repository for license information.
