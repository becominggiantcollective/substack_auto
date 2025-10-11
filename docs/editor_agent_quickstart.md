# Editor Agent Quick Start Guide

## What is the Editor Agent?

The Editor Agent is an AI-powered content refinement tool that reviews and enhances draft articles for:
- **Quality**: Grammar, spelling, tone, and structure
- **SEO**: Keywords, meta tags, and discoverability
- **Engagement**: Readability and compelling content

## Quick Usage

### 1. Basic Import and Setup

```python
from agents.editor_agent import EditorAgent

editor = EditorAgent()
```

### 2. Edit an Article

```python
# Your article data (from Writer Agent or manual input)
article = {
    "title": "Your Article Title",
    "subtitle": "Optional subtitle",
    "content": "Your article content...",
    "tags": ["tag1", "tag2"]
}

# Edit and optimize
result = editor.edit_article(article)

# Get the edited article
edited_article = result["edited_article"]
```

### 3. View Results

```python
# Print SEO report
print(f"SEO Score: {result['seo_report']['overall_seo_score']}/10")
print(f"Quality Score: {result['quality_metrics']['overall_score']}/10")

# Get detailed summary
summary = editor.get_editing_summary(result)
print(summary)
```

## What Gets Optimized?

### Title
- Character count optimized (50-60 chars)
- Keywords integrated
- Compelling and click-worthy

### Meta Description
- Length optimized (150-160 chars)
- Keywords naturally integrated
- Includes call-to-action

### Tags
- 5-8 relevant tags
- Mix of broad and specific
- SEO-optimized

### Content
- Grammar and spelling corrections
- Tone consistency
- Improved structure
- Better readability

## Integration with Existing Workflow

```python
from content_generators.text_generator import TextGenerator
from agents.editor_agent import EditorAgent
from publishers.substack_publisher import SubstackPublisher

# Generate draft
writer = TextGenerator()
draft = writer.create_complete_post()

# Edit and optimize
editor = EditorAgent()
result = editor.edit_article(draft)
optimized = result["edited_article"]

# Publish
publisher = SubstackPublisher()
publisher.publish_complete_post(optimized, media_files)
```

## Output Structure

```python
{
    "edited_article": {
        "title": "Optimized title",
        "content": "Refined content",
        "meta_description": "SEO description",
        "tags": ["optimized", "tags"],
        "word_count": 1234
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
    }
}
```

## Individual Checks

You can also use individual functions:

```python
# Grammar check only
grammar = editor.check_grammar_and_spelling(content)

# Keywords only
keywords = editor.optimize_seo_keywords(title, content)

# Title optimization only
new_title = editor.refine_meta_title(current_title, summary)
```

## Example Scripts

Run the included examples:

```bash
python examples_editor_agent.py
```

## Full Documentation

See [docs/editor_agent.md](editor_agent.md) for complete documentation including:
- All available methods
- Detailed API reference
- Configuration options
- Best practices
- Error handling
- Advanced usage

## Common Patterns

### Pattern 1: Pre-publish Check
```python
result = editor.edit_article(draft)
if result["quality_metrics"]["overall_score"] < 7:
    # Regenerate or review manually
    print("Quality score too low")
else:
    publish(result["edited_article"])
```

### Pattern 2: SEO Focus
```python
result = editor.edit_article(draft)
seo_score = result["seo_report"]["overall_seo_score"]
print(f"SEO Score: {seo_score}/10")
print(f"Keywords: {result['seo_report']['keywords']['primary']}")
```

### Pattern 3: Grammar Only
```python
grammar = editor.check_grammar_and_spelling(content)
if grammar["has_errors"]:
    content = grammar["corrected_text"]
```

## Tips

1. **Always check quality scores** before publishing
2. **Review SEO reports** to understand optimizations
3. **Use the full `edit_article()` method** for best results
4. **Cache results** if editing the same article multiple times
5. **Log summaries** for tracking improvements over time

## Next Steps

- Read the [full documentation](editor_agent.md)
- Check the [test suite](../tests/test_editor_agent.py) for more examples
- Integrate into your workflow
- Monitor quality and SEO scores
