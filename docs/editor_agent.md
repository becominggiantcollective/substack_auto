# Editor Agent Documentation

## Overview

The Editor Agent is a sophisticated AI-powered content refinement system designed to review, enhance, and optimize draft articles for both quality and SEO performance. It integrates seamlessly with the content generation pipeline, accepting drafts from the Writer Agent (TextGenerator) and producing polished, SEO-optimized articles ready for publication.

## Purpose

The Editor Agent serves as the quality assurance and optimization layer in the automated content generation workflow, ensuring that:
- Content is grammatically correct and stylistically consistent
- Articles have optimal structure and readability
- SEO best practices are applied throughout
- Meta tags and descriptions are optimized for search engines
- Keywords are naturally integrated for better discoverability

## Key Features

### 1. Grammar and Spelling Checks
- Detects and corrects grammatical errors
- Identifies spelling mistakes
- Provides style improvement suggestions
- Returns corrected text when errors are found

### 2. Tone and Style Analysis
- Analyzes current tone against target tone (configurable via settings)
- Measures tone consistency throughout the article
- Provides specific suggestions for tone adjustments
- Rates overall style consistency (1-10 scale)

### 3. Structure Analysis
- Evaluates introduction effectiveness
- Assesses body flow and organization
- Rates conclusion strength
- Provides readability score (1-10 scale)
- Suggests structural improvements

### 4. SEO Keyword Optimization
- Identifies primary keywords (2-3 most important)
- Generates secondary keywords (5-7 supporting)
- Creates long-tail keyword phrases (3-5 phrases)
- Assesses keyword density
- Provides integration suggestions

### 5. Meta Title Refinement
- Optimizes title for SEO (50-60 character sweet spot)
- Ensures primary keywords are included
- Makes titles compelling and click-worthy
- Maintains clarity and relevance
- Provides SEO score for the title

### 6. Meta Description Generation
- Creates optimized descriptions (150-160 characters)
- Naturally integrates primary keywords
- Makes descriptions compelling and informative
- Includes calls-to-action when appropriate
- Scores SEO effectiveness

### 7. Tag Optimization
- Generates 5-8 relevant tags
- Balances broad and specific tags
- Identifies trending topics
- Optimizes for both SEO value and relevance
- Provides reasoning for tag choices

## Architecture

### Class Structure

```python
class EditorAgent:
    """
    Main editor agent class that handles all editing and optimization tasks.
    """
    
    def __init__(self):
        """Initialize with OpenAI client and GPT-4 model."""
        
    def check_grammar_and_spelling(content: str) -> Dict
    def analyze_tone_and_style(content: str, target_tone: str) -> Dict
    def analyze_structure(content: str) -> Dict
    def optimize_seo_keywords(title: str, content: str, keywords: List) -> Dict
    def refine_meta_title(title: str, summary: str) -> Dict
    def generate_meta_description(title: str, content: str) -> Dict
    def optimize_tags(title: str, content: str, tags: List) -> Dict
    def edit_article(article_data: Dict) -> Dict
    def get_editing_summary(editing_result: Dict) -> str
```

### Input Format

The Editor Agent accepts article data in the following format:

```python
article_data = {
    "title": "Article Title",
    "subtitle": "Article Subtitle (optional)",
    "content": "Full article content...",
    "tags": ["tag1", "tag2", "tag3"],  # Optional
    "ai_generated": True
}
```

### Output Format

The `edit_article()` method returns a comprehensive result:

```python
{
    "edited_article": {
        "title": "Optimized Title",
        "subtitle": "Subtitle",
        "content": "Refined content with corrections",
        "meta_description": "SEO-optimized description",
        "tags": ["optimized", "tags", "list"],
        "word_count": 1234,
        "ai_generated": True
    },
    "seo_report": {
        "overall_seo_score": 8.5,
        "title_optimization": {...},
        "meta_description": {...},
        "keywords": {...},
        "tags": {...}
    },
    "quality_metrics": {
        "overall_score": 8.0,
        "grammar_check": {...},
        "tone_analysis": {...},
        "structure_analysis": {...}
    },
    "improvements_made": {
        "grammar_corrections": True/False,
        "title_optimized": True/False,
        "tags_optimized": True/False,
        "meta_description_generated": True
    }
}
```

## Usage Examples

### Basic Usage

```python
from agents.editor_agent import EditorAgent

# Initialize the editor
editor = EditorAgent()

# Prepare article data (typically from Writer Agent)
article_data = {
    "title": "The Future of Artificial Intelligence",
    "subtitle": "Exploring AI innovations and their impact",
    "content": "Artificial intelligence is transforming...",
    "tags": ["AI", "technology", "innovation"]
}

# Edit and optimize the article
result = editor.edit_article(article_data)

# Access the edited article
edited_article = result["edited_article"]
print(f"Optimized Title: {edited_article['title']}")
print(f"Meta Description: {edited_article['meta_description']}")
print(f"Tags: {', '.join(edited_article['tags'])}")

# View the SEO report
seo_report = result["seo_report"]
print(f"Overall SEO Score: {seo_report['overall_seo_score']}/10")

# Get a human-readable summary
summary = editor.get_editing_summary(result)
print(summary)
```

### Integration with Writer Agent

```python
from content_generators.text_generator import TextGenerator
from agents.editor_agent import EditorAgent

# Generate initial draft
writer = TextGenerator()
draft = writer.create_complete_post()

# Edit and optimize
editor = EditorAgent()
result = editor.edit_article(draft)

# Use the edited article
edited_article = result["edited_article"]
```

### Individual Check Functions

You can also use individual editing functions:

```python
editor = EditorAgent()

# Check only grammar
grammar_result = editor.check_grammar_and_spelling(content)
if grammar_result["has_errors"]:
    print(f"Errors found: {grammar_result['errors']}")
    corrected = grammar_result["corrected_text"]

# Analyze only tone
tone_result = editor.analyze_tone_and_style(content, "professional")
if not tone_result["matches_target"]:
    print(f"Tone suggestions: {tone_result['suggestions']}")

# Optimize only keywords
keywords = editor.optimize_seo_keywords(title, content)
print(f"Primary keywords: {keywords['primary_keywords']}")

# Refine only title
title_result = editor.refine_meta_title(current_title, summary)
print(f"Optimized title: {title_result['optimized_title']}")
```

## Integration with Content Pipeline

### Standard Workflow

```
TextGenerator → EditorAgent → SubstackPublisher
    (Draft)        (Edited)      (Published)
```

### Example Pipeline Implementation

```python
from content_generators.text_generator import TextGenerator
from agents.editor_agent import EditorAgent
from publishers.substack_publisher import SubstackPublisher

# Step 1: Generate draft content
writer = TextGenerator()
draft_article = writer.create_complete_post()

# Step 2: Edit and optimize
editor = EditorAgent()
editing_result = editor.edit_article(draft_article)
edited_article = editing_result["edited_article"]

# Step 3: Publish
publisher = SubstackPublisher()
publish_result = publisher.publish_complete_post(
    edited_article,
    media_files  # From image/video generation
)

# Step 4: Log SEO report
seo_summary = editor.get_editing_summary(editing_result)
print(seo_summary)
```

## Configuration

The Editor Agent respects settings from the main configuration:

```python
# In .env or environment variables
CONTENT_TONE=professional and engaging
TARGET_AUDIENCE=intelligent general audience
CONTENT_STYLE=informative and thought-provoking
CUSTOM_INSTRUCTIONS=Always include practical examples
```

These settings influence:
- Tone analysis target
- Style recommendations
- Audience-appropriate content suggestions

## Quality Metrics

### Overall Quality Score
Calculated as the average of:
- Grammar score (10 if clean, 7 if errors)
- Tone consistency rating (1-10)
- Structure readability score (1-10)
- Title SEO score (1-10)
- Meta description SEO score (1-10)

### SEO Effectiveness

The Editor Agent evaluates SEO on multiple dimensions:
- **Title Optimization**: Character count, keyword inclusion, clickability
- **Meta Description**: Length, keyword density, call-to-action
- **Keyword Integration**: Primary, secondary, and long-tail keywords
- **Tag Relevance**: Balance of broad and specific tags

## Best Practices

### 1. Always Use Complete Workflow
Use `edit_article()` for comprehensive optimization rather than individual functions.

### 2. Review SEO Reports
Check the SEO report to understand what was optimized:
```python
print(editor.get_editing_summary(result))
```

### 3. Monitor Quality Scores
Track quality scores over time to ensure consistent output:
```python
if result["quality_metrics"]["overall_score"] < 7:
    # Log for review or regenerate
    logger.warning("Low quality score detected")
```

### 4. Validate Output
Always verify the edited article before publishing:
```python
edited = result["edited_article"]
assert edited["title"], "Title cannot be empty"
assert len(edited["content"]) > 500, "Content too short"
assert edited["meta_description"], "Meta description required"
```

## Testing

Comprehensive tests are available in `tests/test_editor_agent.py`:

```bash
# Run all Editor Agent tests
python tests/test_editor_agent.py

# Run with verbose output
python tests/test_editor_agent.py -v
```

Test coverage includes:
- Grammar and spelling checks
- Tone and style analysis
- Structure evaluation
- SEO keyword optimization
- Meta title refinement
- Meta description generation
- Tag optimization
- Complete editing workflow
- Integration compatibility

## API Reference

### `EditorAgent.edit_article(article_data: Dict) -> Dict`

**Main method for comprehensive article editing.**

**Parameters:**
- `article_data` (dict): Article with title, content, subtitle (optional), tags (optional)

**Returns:**
- `dict`: Contains edited_article, seo_report, quality_metrics, improvements_made

### `EditorAgent.check_grammar_and_spelling(content: str) -> Dict`

**Check grammar and spelling in content.**

**Parameters:**
- `content` (str): Text to check

**Returns:**
- `dict`: has_errors, errors, corrected_text, suggestions

### `EditorAgent.analyze_tone_and_style(content: str, target_tone: str = None) -> Dict`

**Analyze tone and style consistency.**

**Parameters:**
- `content` (str): Text to analyze
- `target_tone` (str, optional): Target tone (defaults to settings)

**Returns:**
- `dict`: current_tone, matches_target, consistency_rating, suggestions

### `EditorAgent.analyze_structure(content: str) -> Dict`

**Analyze article structure and organization.**

**Parameters:**
- `content` (str): Text to analyze

**Returns:**
- `dict`: introduction, body_flow, conclusion, readability_score, improvements

### `EditorAgent.optimize_seo_keywords(title: str, content: str, existing_keywords: List = None) -> Dict`

**Optimize SEO keywords.**

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `existing_keywords` (list, optional): Current keywords

**Returns:**
- `dict`: primary_keywords, secondary_keywords, long_tail_keywords, keyword_density, integration_suggestions

### `EditorAgent.refine_meta_title(current_title: str, content_summary: str) -> Dict`

**Refine title for SEO.**

**Parameters:**
- `current_title` (str): Current title
- `content_summary` (str): Brief content summary

**Returns:**
- `dict`: original_title, optimized_title, character_count, improvements, seo_score

### `EditorAgent.generate_meta_description(title: str, content: str) -> Dict`

**Generate SEO-optimized meta description.**

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content

**Returns:**
- `dict`: meta_description, character_count, keywords_included, seo_score

### `EditorAgent.optimize_tags(title: str, content: str, existing_tags: List = None) -> Dict`

**Optimize article tags.**

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `existing_tags` (list, optional): Current tags

**Returns:**
- `dict`: original_tags, optimized_tags, new_tags, removed_tags, reasoning

### `EditorAgent.get_editing_summary(editing_result: Dict) -> str`

**Generate human-readable editing summary.**

**Parameters:**
- `editing_result` (dict): Result from edit_article()

**Returns:**
- `str`: Formatted summary report

## Support

For issues or questions:
1. Check the test suite for usage examples
2. Review log files for detailed error messages
3. Consult the main README.md for project-wide documentation

## License

Part of the Substack Auto project. See main LICENSE file.
