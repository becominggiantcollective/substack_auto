# Writer Agent Documentation

## Overview

The Writer Agent is an AI-powered content generation agent that creates SEO-optimized Substack newsletter articles. It accepts research summaries and keyword lists, then generates engaging, well-structured articles with proper SEO integration.

## Features

- **SEO-Optimized Content Generation**: Generates articles with natural keyword integration
- **Keyword Density Management**: Maintains optimal keyword density (~2%) for SEO
- **Structured Content**: Creates well-organized articles with proper formatting
- **Meta Data Generation**: Produces SEO-optimized meta titles and descriptions
- **Tag Suggestions**: Generates relevant tags for content discovery
- **Readability Focus**: Ensures content is engaging and readable while maintaining SEO best practices
- **Configurable Output**: Respects content style, tone, and audience settings

## Installation

The Writer Agent is included in the Substack Auto package. Ensure you have all dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from agents.writer_agent import WriterAgent

# Initialize the agent
writer = WriterAgent()

# Generate a complete article
article = writer.create_complete_article(
    topic="The Future of Artificial Intelligence",
    keywords=["AI", "artificial intelligence", "machine learning", "technology"],
    research_summary="AI is rapidly evolving with new breakthroughs in deep learning..."
)

# Access the generated content
print(f"Title: {article['title']}")
print(f"Word Count: {article['word_count']}")
print(f"Meta Title: {article['meta_title']}")
print(f"Meta Description: {article['meta_description']}")
print(f"Tags: {', '.join(article['tags'])}")
print(f"Content: {article['content']}")
```

### Generate Article Only

```python
# Generate just the article content without metadata
article_data = writer.generate_article(
    topic="Understanding Blockchain Technology",
    keywords=["blockchain", "cryptocurrency", "decentralization"],
    research_summary="Blockchain provides a distributed ledger system..."
)

print(f"Word Count: {article_data['word_count']}")
print(f"Keyword Density: {article_data['keyword_density']:.2%}")
print(f"Keywords Used: {article_data['keywords_used']}")
```

### Generate Individual Components

```python
# Generate meta title
meta_title = writer.generate_meta_title(
    title="The Rise of Quantum Computing",
    keywords=["quantum computing", "quantum mechanics", "technology"]
)

# Generate meta description
meta_description = writer.generate_meta_description(
    title="The Rise of Quantum Computing",
    content="Quantum computing represents a paradigm shift...",
    keywords=["quantum computing", "quantum mechanics"]
)

# Generate tags
tags = writer.generate_tags(
    title="The Rise of Quantum Computing",
    content="Quantum computing leverages quantum mechanics...",
    keywords=["quantum computing", "quantum mechanics", "technology"]
)
```

## Input Parameters

### Required Parameters

#### `topic` (str)
The main topic or title for the article. This serves as the primary subject and will be used as the article title.

**Example:** `"The Future of Artificial Intelligence in Healthcare"`

#### `keywords` (List[str])
A list of SEO keywords to integrate into the article. The first keyword is treated as the primary keyword.

**Example:** `["AI healthcare", "medical AI", "artificial intelligence", "diagnosis"]`

### Optional Parameters

#### `research_summary` (str, optional)
A research summary or background information that informs the article content. This helps ground the article in specific facts or findings.

**Example:** 
```
"Recent studies show that AI diagnostic tools achieve 95% accuracy in detecting 
certain cancers. Healthcare providers are increasingly adopting AI systems..."
```

## Output Format

The `create_complete_article()` method returns a dictionary with the following structure:

```python
{
    "title": str,              # Article title
    "content": str,            # Main article content (800-1200 words)
    "meta_title": str,         # SEO-optimized meta title (50-60 chars)
    "meta_description": str,   # SEO-optimized meta description (150-160 chars)
    "tags": List[str],         # 5-8 relevant tags
    "word_count": int,         # Actual word count
    "keyword_density": float,  # Primary keyword density (e.g., 0.02 for 2%)
    "keywords_used": List[str],# Keywords that appear in content
    "seo_optimized": bool,     # Always True
    "ai_generated": bool       # Always True
}
```

## Configuration

The Writer Agent respects the following environment variables from your `.env` file:

- **CONTENT_TONE**: The tone of voice for content (e.g., "professional and engaging")
- **TARGET_AUDIENCE**: Who the content is written for (e.g., "intelligent general audience")
- **CONTENT_STYLE**: The style of content (e.g., "informative and thought-provoking")
- **CUSTOM_INSTRUCTIONS**: Additional specific instructions for content generation

### Example Configuration

```env
CONTENT_TONE=professional and engaging
TARGET_AUDIENCE=tech-savvy business professionals
CONTENT_STYLE=practical and actionable
CUSTOM_INSTRUCTIONS=Include real-world examples and case studies
```

## SEO Optimization Features

### Keyword Integration

The Writer Agent integrates keywords naturally throughout the content:

- **Primary Keyword**: Integrated with ~2% density (configurable)
- **Secondary Keywords**: Included where relevant and natural
- **Semantic Variations**: Uses related terms and synonyms
- **Natural Flow**: Maintains readability while optimizing for SEO

### Keyword Density

Keyword density is calculated as:

```
keyword_density = (keyword_count / total_words)
```

The agent targets approximately 2% density for the primary keyword, which is considered optimal for SEO without keyword stuffing.

### Meta Data Optimization

#### Meta Title
- Length: 50-60 characters (optimal for search results)
- Includes primary keyword when possible
- Compelling and click-worthy
- Accurately represents content

#### Meta Description
- Length: 150-160 characters (optimal for search results)
- Includes primary keyword naturally
- Action-oriented and compelling
- Summarizes article's value proposition

## Content Structure

Articles generated by the Writer Agent follow this structure:

1. **Engaging Introduction**: Hooks the reader and introduces the topic
2. **Well-Organized Body**: 
   - Multiple sections with clear subheadings
   - Logical flow of ideas
   - Practical insights and examples
3. **Strong Conclusion**: Summarizes key takeaways

The content uses markdown formatting:
- `##` for main section headers
- `###` for subsection headers
- Proper paragraph breaks for readability

## Integration with Other Agents

The Writer Agent is designed to work seamlessly with other agents in the content pipeline:

### Input from Research Agent
```python
# Research Agent provides topic, keywords, and research summary
research_output = {
    "topic": "The Impact of 5G on IoT",
    "keywords": ["5G", "IoT", "Internet of Things", "connectivity"],
    "research_summary": "5G networks offer 100x faster speeds..."
}

# Writer Agent generates content
article = writer.create_complete_article(
    topic=research_output["topic"],
    keywords=research_output["keywords"],
    research_summary=research_output["research_summary"]
)
```

### Output to Editor Agent
The Writer Agent output is compatible with future Editor Agent review:
```python
# Writer Agent output can be passed to Editor Agent
editor_input = {
    "content": article["content"],
    "title": article["title"],
    "keywords": article["keywords_used"]
}
```

### Output to SEO Specialist Agent
SEO metadata is ready for SEO Specialist Agent optimization:
```python
# SEO metadata can be further optimized
seo_data = {
    "meta_title": article["meta_title"],
    "meta_description": article["meta_description"],
    "tags": article["tags"],
    "keyword_density": article["keyword_density"]
}
```

## Best Practices

### Keyword Selection

1. **Primary Keyword**: Choose the most important keyword first
2. **Keyword Relevance**: Ensure keywords are relevant to the topic
3. **Keyword Balance**: Include 3-8 keywords for optimal coverage
4. **Avoid Keyword Stuffing**: Let the agent integrate keywords naturally

### Research Summary

1. **Be Specific**: Include concrete facts and data points
2. **Keep it Concise**: 200-500 words is ideal
3. **Provide Context**: Give background that informs the article
4. **Stay Relevant**: Ensure research directly relates to the topic

### Content Configuration

1. **Match Your Brand**: Set appropriate tone and style in `.env`
2. **Know Your Audience**: Configure target audience accurately
3. **Be Consistent**: Keep configuration consistent across articles
4. **Test and Iterate**: Experiment with different settings

## Examples

### Tech Blog Article

```python
writer = WriterAgent()

article = writer.create_complete_article(
    topic="How Cloud Computing is Transforming Small Businesses",
    keywords=[
        "cloud computing",
        "small business",
        "digital transformation",
        "SaaS"
    ],
    research_summary="""
    Cloud computing adoption among small businesses has increased 
    by 67% in the last two years. Key benefits include reduced IT 
    costs, improved collaboration, and scalability.
    """
)
```

### Health & Wellness Article

```python
article = writer.create_complete_article(
    topic="The Science Behind Meditation and Stress Reduction",
    keywords=[
        "meditation",
        "stress reduction",
        "mindfulness",
        "mental health"
    ],
    research_summary="""
    Studies show that regular meditation practice can reduce cortisol 
    levels by up to 30% and improve emotional regulation. MRI scans 
    reveal changes in brain structure after 8 weeks of practice.
    """
)
```

## API Reference

### WriterAgent Class

#### `__init__()`
Initialize the Writer Agent with OpenAI client.

#### `generate_article(topic, keywords, research_summary=None)`
Generate the main article content.

**Returns:** Dict with title, content, word_count, keyword_density, keywords_used

#### `generate_meta_title(title, keywords)`
Generate SEO-optimized meta title.

**Returns:** str (50-70 characters)

#### `generate_meta_description(title, content, keywords)`
Generate SEO-optimized meta description.

**Returns:** str (150-160 characters)

#### `generate_tags(title, content, keywords)`
Generate relevant tags for the article.

**Returns:** List[str] (5-8 tags)

#### `create_complete_article(topic, keywords, research_summary=None)`
Generate complete article with all metadata.

**Returns:** Dict with full article package

#### `calculate_keyword_density(content, keyword)`
Calculate keyword density in content.

**Returns:** float (density as decimal, e.g., 0.02 for 2%)

## Troubleshooting

### Low Keyword Density

If keyword density is too low:
- Ensure keywords are relevant to the topic
- Try more specific, targeted keywords
- Check that research summary includes keywords

### Content Too Short/Long

Target word count is 800-1200 words. If content is outside this range:
- Check if the topic is too broad or narrow
- Ensure research summary provides enough context
- The agent will retry if word count is significantly off

### Poor Tag Quality

If generated tags aren't relevant:
- Review keyword selection
- Ensure topic is specific and clear
- Check that content aligns with intended topic

## License

This component is part of the Substack Auto project.
