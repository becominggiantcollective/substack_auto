# Writer Agent Documentation

## Overview

The Writer Agent is an AI-powered content generation agent that creates SEO-optimized newsletter articles based on research input. It accepts topic, keywords, and research summaries, then generates comprehensive, well-structured articles with proper SEO integration.

## Features

- **SEO-Optimized Content Generation**: Creates articles with natural keyword integration
- **Keyword Density Analysis**: Calculates and optimizes keyword density (target: 2%)
- **Content Structure Validation**: Ensures proper paragraph structure and readability
- **Meta Data Generation**: Produces SEO-optimized meta titles and descriptions
- **Tag Suggestions**: Generates relevant tags for content categorization
- **Quality Scoring**: Provides SEO quality scores (0-100) for generated content

## Installation

The Writer Agent is part of the `src/agents` module. Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from agents.writer_agent import WriterAgent

# Initialize the agent
writer = WriterAgent()

# Generate complete content
result = writer.create_complete_content(
    topic="The Future of Artificial Intelligence",
    keywords=["AI", "machine learning", "technology", "innovation"],
    research_summary="Recent advances in AI have led to breakthroughs in natural language processing..."
)

# Access the generated content
print(f"Title: {result['title']}")
print(f"Meta Title: {result['meta_title']}")
print(f"Meta Description: {result['meta_description']}")
print(f"Word Count: {result['word_count']}")
print(f"SEO Score: {result['seo_score']}/100")
print(f"\nArticle:\n{result['article']}")
print(f"\nTags: {', '.join(result['tags'])}")
```

### Advanced Usage

#### Custom API Key

```python
from agents.writer_agent import WriterAgent

# Use a custom OpenAI API key
writer = WriterAgent(openai_api_key="your-api-key-here")
```

#### Generate Individual Components

```python
from agents.writer_agent import WriterAgent

writer = WriterAgent()

# Generate just the article
article_result = writer.generate_article(
    topic="AI in Healthcare",
    keywords=["AI", "healthcare", "medical technology"],
    research_summary="AI is transforming healthcare through...",
    target_word_count=1000
)

# Generate just the meta title
meta_title = writer.generate_meta_title(
    topic="AI in Healthcare",
    keywords=["AI", "healthcare"]
)

# Generate just the meta description
meta_description = writer.generate_meta_description(
    topic="AI in Healthcare",
    keywords=["AI", "healthcare"],
    article_preview="First 200 words of article..."
)

# Generate just the tags
tags = writer.generate_tags(
    topic="AI in Healthcare",
    keywords=["AI", "healthcare"],
    article="Full article content..."
)
```

## API Reference

### WriterAgent Class

#### `__init__(openai_api_key: Optional[str] = None)`

Initialize the Writer Agent.

**Parameters:**
- `openai_api_key` (str, optional): OpenAI API key. If not provided, uses the key from settings.

**Attributes:**
- `model`: GPT model to use (default: "gpt-4")
- `target_word_count_min`: Minimum target word count (800)
- `target_word_count_max`: Maximum target word count (1200)
- `target_keyword_density`: Target keyword density (0.02 = 2%)

#### `create_complete_content(topic, keywords, research_summary, target_word_count=None)`

Generate complete SEO-optimized content package.

**Parameters:**
- `topic` (str): The main topic/title for the article
- `keywords` (List[str]): List of SEO keywords to integrate
- `research_summary` (str): Summary of research findings
- `target_word_count` (int, optional): Specific target word count

**Returns:**
Dictionary containing:
- `title`: The article title
- `article`: The article content
- `meta_title`: SEO-optimized meta title (max 60 chars)
- `meta_description`: SEO-optimized meta description (max 155 chars)
- `tags`: List of suggested tags (5-8 tags)
- `word_count`: Actual word count
- `keyword_densities`: Dictionary mapping keywords to density percentages
- `structure_validation`: Dictionary of structure validation results
- `seo_score`: Overall SEO quality score (0-100)
- `ai_generated`: Boolean flag (always True)

**Example:**
```python
result = writer.create_complete_content(
    topic="The Rise of AI",
    keywords=["AI", "technology", "innovation"],
    research_summary="AI is growing rapidly..."
)
```

#### `generate_article(topic, keywords, research_summary, target_word_count=None)`

Generate an SEO-optimized article.

**Parameters:**
- `topic` (str): The main topic/title
- `keywords` (List[str]): SEO keywords to integrate
- `research_summary` (str): Research summary
- `target_word_count` (int, optional): Target word count (default: 1000)

**Returns:**
Dictionary containing:
- `article`: The generated article content
- `word_count`: Actual word count
- `keyword_densities`: Density for each keyword
- `structure_validation`: Structure validation results

#### `generate_meta_title(topic, keywords)`

Generate an SEO-optimized meta title.

**Parameters:**
- `topic` (str): The article topic
- `keywords` (List[str]): List of SEO keywords

**Returns:**
String containing meta title (max 60 characters)

#### `generate_meta_description(topic, keywords, article_preview)`

Generate an SEO-optimized meta description.

**Parameters:**
- `topic` (str): The article topic
- `keywords` (List[str]): List of SEO keywords
- `article_preview` (str): Preview of the article content

**Returns:**
String containing meta description (max 155 characters)

#### `generate_tags(topic, keywords, article)`

Generate suggested tags for the article.

**Parameters:**
- `topic` (str): The article topic
- `keywords` (List[str]): List of SEO keywords
- `article` (str): The article content

**Returns:**
List of 5-8 suggested tags

#### `calculate_keyword_density(content, keywords)`

Calculate keyword density for each keyword.

**Parameters:**
- `content` (str): The article content
- `keywords` (List[str]): Keywords to check

**Returns:**
Dictionary mapping keywords to their density percentages

**Example:**
```python
densities = writer.calculate_keyword_density(
    content="AI is transforming technology...",
    keywords=["AI", "technology"]
)
# Returns: {"AI": 0.05, "technology": 0.025}
```

#### `validate_content_structure(content)`

Validate that content has proper structure.

**Parameters:**
- `content` (str): The article content

**Returns:**
Dictionary with validation results:
- `has_paragraphs`: Has at least 3 paragraphs
- `has_sufficient_length`: Word count is within 800-1200 range
- `has_opening`: Opening paragraph has at least 30 words
- `has_sections`: Has at least 5 sections/lines

## Output Format

### Complete Content Structure

```python
{
    "title": "The Future of Artificial Intelligence",
    "article": "Full article content with 800-1200 words...",
    "meta_title": "AI Future: Innovation & Technology Trends",
    "meta_description": "Discover how AI is shaping the future of technology...",
    "tags": ["AI", "technology", "innovation", "future tech"],
    "word_count": 1050,
    "keyword_densities": {
        "AI": 0.021,
        "machine learning": 0.015,
        "technology": 0.019
    },
    "structure_validation": {
        "has_paragraphs": True,
        "has_sufficient_length": True,
        "has_opening": True,
        "has_sections": True
    },
    "seo_score": 92,
    "ai_generated": True
}
```

## SEO Optimization Guidelines

### Keyword Density

The Writer Agent targets a 2% keyword density for primary keywords. This is calculated as:

```
Keyword Density = (Keyword Occurrences / Total Words) × 100
```

**Best Practices:**
- Primary keywords: 2-2.5% density
- Secondary keywords: 1-1.5% density
- Avoid keyword stuffing (>3% density)

### Content Structure

Well-structured content improves both SEO and readability:

1. **Opening Paragraph**: 30+ words that hook the reader
2. **Body Paragraphs**: 3-5 sentences each, separated by line breaks
3. **Logical Sections**: Clear progression of ideas
4. **Total Length**: 800-1200 words for optimal engagement

### Meta Title Optimization

- Maximum 60 characters
- Include primary keyword near the beginning
- Compelling and click-worthy
- Accurately describes content

**Example:**
```
"AI Revolution: The Future of Technology" (43 chars)
```

### Meta Description Optimization

- Maximum 155 characters
- Include primary keywords naturally
- Include a call-to-action or value proposition
- Summarize the key benefit

**Example:**
```
"Discover how AI is transforming technology and what it means for the future. Learn about the latest innovations." (112 chars)
```

## Integration with Other Agents

The Writer Agent is designed to work with other agents in the content generation pipeline:

### Research Agent → Writer Agent

```python
# Assuming research_agent.py provides research output
research_output = research_agent.conduct_research(topic="AI in Healthcare")

# Feed research into Writer Agent
writer = WriterAgent()
content = writer.create_complete_content(
    topic=research_output["topic"],
    keywords=research_output["keywords"],
    research_summary=research_output["summary"]
)
```

### Writer Agent → Editor Agent

```python
# Generate content with Writer Agent
writer_output = writer.create_complete_content(
    topic="AI in Healthcare",
    keywords=["AI", "healthcare"],
    research_summary="..."
)

# Pass to Editor Agent for refinement (when implemented)
# editor = EditorAgent()
# refined_content = editor.edit(writer_output)
```

### Writer Agent → SEO Specialist Agent

```python
# Generate content with Writer Agent
content = writer.create_complete_content(...)

# Pass to SEO Specialist for additional optimization (when implemented)
# seo_specialist = SEOSpecialistAgent()
# optimized_content = seo_specialist.optimize(content)
```

## Configuration

The Writer Agent respects global configuration settings:

```python
# In .env file
CONTENT_TONE=professional and engaging
TARGET_AUDIENCE=intelligent general audience
CONTENT_STYLE=informative and thought-provoking
CUSTOM_INSTRUCTIONS=Always include practical examples
```

These settings affect content generation:

```python
from config.settings import settings

# Settings are automatically applied
writer = WriterAgent()
content = writer.create_complete_content(...)
# Content will use the configured tone, audience, and style
```

## Error Handling

The Writer Agent includes retry logic and error handling:

```python
from tenacity import RetryError

try:
    result = writer.create_complete_content(
        topic="AI in Healthcare",
        keywords=["AI", "healthcare"],
        research_summary="..."
    )
except RetryError:
    print("Failed after 3 retry attempts")
except Exception as e:
    print(f"Error generating content: {e}")
```

## Performance Considerations

### API Calls

The `create_complete_content()` method makes 4 separate OpenAI API calls:
1. Article generation (~1500 tokens)
2. Meta title generation (~50 tokens)
3. Meta description generation (~100 tokens)
4. Tags generation (~100 tokens)

**Total estimated cost per complete content generation:** ~$0.03-0.05 (with GPT-4)

### Response Times

- Article generation: 10-30 seconds
- Meta title: 2-5 seconds
- Meta description: 3-7 seconds
- Tags: 2-5 seconds

**Total time:** Approximately 20-50 seconds per complete content package

### Optimization Tips

1. **Use targeted keywords**: Fewer, more focused keywords yield better results
2. **Provide quality research summaries**: Better input = better output
3. **Cache results**: Store generated content to avoid regeneration
4. **Batch processing**: Generate multiple articles in parallel when possible

## Testing

Run the Writer Agent tests:

```bash
# Run all Writer Agent tests
python -m unittest tests.test_writer_agent -v

# Run specific test
python -m unittest tests.test_writer_agent.TestWriterAgent.test_create_complete_content -v
```

## Logging

The Writer Agent logs important events and metrics:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Writer Agent will log:
# - Topic and keyword information
# - Word counts
# - Keyword densities
# - Structure validation results
# - SEO scores
# - Errors and exceptions
```

**Example log output:**
```
INFO:agents.writer_agent:Starting content generation for topic: The Future of AI
INFO:agents.writer_agent:Keywords: ['AI', 'technology', 'innovation']
INFO:agents.writer_agent:Generated article with 1050 words
INFO:agents.writer_agent:Keyword densities: {'AI': 0.021, 'technology': 0.019}
INFO:agents.writer_agent:Generated meta title: AI Future: Innovation & Technology (43 chars)
INFO:agents.writer_agent:Generated meta description: Discover how AI... (112 chars)
INFO:agents.writer_agent:Generated tags: ['AI', 'technology', 'innovation', ...]
INFO:agents.writer_agent:Content generation complete. SEO score: 92/100
```

## Best Practices

1. **Use Quality Research**: Provide comprehensive research summaries for best results
2. **Target Relevant Keywords**: Focus on 3-5 primary keywords rather than a long list
3. **Validate Output**: Always check the SEO score and structure validation
4. **Iterate if Needed**: Low SEO scores may require regeneration with adjusted parameters
5. **Monitor Keyword Density**: Aim for 2% density on primary keywords
6. **Review Generated Content**: While AI-generated, content should be reviewed for accuracy

## Troubleshooting

### Low SEO Score

If SEO score is below 70:
- Check keyword densities (should be 1.5-2.5%)
- Verify word count is within 800-1200 range
- Ensure structure validation passes all checks
- Consider adjusting research summary for more focused content

### Keyword Stuffing

If keyword density is too high (>3%):
- Use fewer instances of the keyword in research summary
- Add more secondary keywords to balance the content
- Request regeneration with adjusted parameters

### Poor Structure

If structure validation fails:
- Check that article has multiple paragraphs
- Verify opening paragraph is substantial (30+ words)
- Ensure content meets minimum length requirements

## Examples

### Example 1: Technology Blog Post

```python
from agents.writer_agent import WriterAgent

writer = WriterAgent()

result = writer.create_complete_content(
    topic="The Impact of Quantum Computing on Cybersecurity",
    keywords=["quantum computing", "cybersecurity", "encryption", "technology"],
    research_summary="""
    Quantum computing poses both opportunities and challenges for cybersecurity.
    Current encryption methods may become vulnerable to quantum attacks.
    Post-quantum cryptography is being developed to address these concerns.
    Organizations need to prepare for the quantum computing era.
    """
)

print(f"SEO Score: {result['seo_score']}/100")
print(f"Article: {result['article'][:200]}...")
```

### Example 2: Health & Wellness Content

```python
from agents.writer_agent import WriterAgent

writer = WriterAgent()

result = writer.create_complete_content(
    topic="Mental Health Benefits of Regular Exercise",
    keywords=["mental health", "exercise", "wellness", "fitness"],
    research_summary="""
    Exercise has significant mental health benefits beyond physical fitness.
    Regular physical activity reduces anxiety and depression symptoms.
    Exercise improves mood through endorphin release and stress reduction.
    Even moderate exercise can have positive mental health effects.
    """
)

# Check keyword optimization
for keyword, density in result['keyword_densities'].items():
    print(f"{keyword}: {density*100:.2f}%")
```

### Example 3: Business Strategy Article

```python
from agents.writer_agent import WriterAgent

writer = WriterAgent()

result = writer.create_complete_content(
    topic="Digital Transformation Strategies for SMBs",
    keywords=["digital transformation", "small business", "technology adoption", "strategy"],
    research_summary="""
    Small and medium businesses (SMBs) can leverage digital transformation
    for competitive advantage. Key strategies include cloud adoption,
    automation, and data analytics. Success requires proper planning
    and change management.
    """,
    target_word_count=1100
)

print(f"Title: {result['meta_title']}")
print(f"Description: {result['meta_description']}")
print(f"Tags: {', '.join(result['tags'])}")
```

## Future Enhancements

Planned improvements for the Writer Agent:

- [ ] Support for multiple content formats (listicles, how-to guides, etc.)
- [ ] Readability score calculation (Flesch-Kincaid)
- [ ] A/B testing support for headlines
- [ ] Multi-language content generation
- [ ] Custom tone/style templates
- [ ] Integration with plagiarism checkers
- [ ] Automatic internal linking suggestions
- [ ] Image placement recommendations

## Support

For issues or questions about the Writer Agent:

1. Check the troubleshooting section above
2. Review the test suite for usage examples
3. Enable debug logging for detailed information
4. Open an issue on the GitHub repository

## License

Part of the Substack Auto project. See repository LICENSE for details.
