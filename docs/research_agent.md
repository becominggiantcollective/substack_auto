# Research Agent Documentation

## Overview

The Research Agent is responsible for discovering trending topics and analyzing SEO keywords for Substack newsletter content. It uses AI-powered analysis to identify current trends and optimize content for search engines.

## Features

- **Trending Topic Discovery**: Identifies current, relevant topics based on configured interest areas
- **SEO Keyword Analysis**: Generates primary, secondary, and long-tail keywords for optimization
- **Search Intent Analysis**: Determines the primary search intent for better content targeting
- **Content Recommendations**: Provides actionable tips for content optimization
- **Fallback Mechanisms**: Gracefully handles API failures with intelligent fallbacks

## Installation

The Research Agent is part of the main Substack Auto package and requires:

```bash
pip install openai>=1.3.0 tenacity>=8.2.0
```

## Usage

### Basic Usage

```python
from agents.research_agent import ResearchAgent

# Initialize the agent
research_agent = ResearchAgent()

# Get a complete research summary
summary = research_agent.generate_research_summary(topic_count=3)

# Access the results
for result in summary["research_results"]:
    print(f"Topic: {result['topic']}")
    print(f"Trend Score: {result['trend_score']}/10")
    print(f"Primary Keywords: {result['seo_keywords']['primary']}")
    print(f"Rationale: {result['rationale']}")
    print("---")
```

### Get Top Topic with SEO

```python
# Get the single best topic with full SEO analysis
top_topic = research_agent.get_top_topic_with_seo()

print(f"Recommended Topic: {top_topic['topic']}")
print(f"Primary Keywords: {', '.join(top_topic['seo_keywords']['primary'])}")
print(f"Search Intent: {top_topic['search_intent']}")
```

### Custom Topic Areas

```python
# Research specific topic areas
custom_topics = ["machine learning", "blockchain", "cybersecurity"]
summary = research_agent.generate_research_summary(
    topic_count=5,
    base_topics=custom_topics
)
```

### Discover Trending Topics Only

```python
# Just get trending topics without SEO analysis
trending = research_agent.discover_trending_topics(count=10)

for topic_data in trending:
    print(f"{topic_data['topic']} (Score: {topic_data['trend_score']}/10)")
    print(f"  {topic_data['rationale']}")
```

### SEO Keyword Analysis Only

```python
# Analyze SEO keywords for a specific topic
topic = "The Future of Artificial Intelligence"
seo_data = research_agent.analyze_seo_keywords(topic)

print(f"Primary Keywords: {seo_data['primary_keywords']}")
print(f"Secondary Keywords: {seo_data['secondary_keywords']}")
print(f"Long-tail Keywords: {seo_data['long_tail_keywords']}")
print(f"Search Intent: {seo_data['search_intent']}")
print(f"Recommendations: {seo_data['content_recommendations']}")
```

### With Target Keywords

```python
# Analyze keywords with specific target keywords in mind
topic = "Enterprise AI Adoption"
target_keywords = ["enterprise ai", "ai implementation", "business automation"]

seo_data = research_agent.analyze_seo_keywords(topic, target_keywords)
```

## Output Format

### Research Summary

The `generate_research_summary()` method returns a complete research summary:

```json
{
  "research_date": "2024-01-15T10:30:00.000000",
  "topic_count": 3,
  "base_topics": ["technology", "AI", "innovation"],
  "research_results": [
    {
      "topic": "The Rise of Generative AI in Enterprise",
      "rationale": "Generative AI is transforming how businesses operate...",
      "trend_score": 9,
      "seo_keywords": {
        "primary": ["generative ai", "enterprise ai", "business automation"],
        "secondary": ["ai tools", "machine learning", "digital transformation", "ai adoption"],
        "long_tail": [
          "generative ai for enterprise",
          "how to implement generative ai",
          "generative ai use cases",
          "enterprise ai solutions"
        ]
      },
      "search_intent": "informational",
      "content_recommendations": "Focus on practical use cases and ROI...",
      "estimated_monthly_searches": "10k-100k",
      "discovered_at": "2024-01-15T10:30:00.000000"
    }
  ],
  "agent_version": "1.0.0",
  "status": "success"
}
```

### Trending Topics

The `discover_trending_topics()` method returns:

```json
[
  {
    "topic": "Topic Title",
    "rationale": "Why this topic is trending and valuable",
    "trend_score": 8,
    "discovered_at": "2024-01-15T10:30:00.000000",
    "source": "ai_trend_analysis"
  }
]
```

### SEO Keywords

The `analyze_seo_keywords()` method returns:

```json
{
  "primary_keywords": ["keyword1", "keyword2", "keyword3"],
  "secondary_keywords": ["keyword1", "keyword2", "keyword3", "..."],
  "long_tail_keywords": ["specific phrase 1", "specific phrase 2", "..."],
  "search_intent": "informational",
  "content_recommendations": "Brief optimization tips",
  "estimated_monthly_searches": "10k-100k",
  "analyzed_at": "2024-01-15T10:30:00.000000",
  "topic": "Topic Title"
}
```

## Integration with Other Agents

### Writer Agent Integration

The research output is designed to be consumed by content generation agents:

```python
# Get research data
research_agent = ResearchAgent()
top_topic = research_agent.get_top_topic_with_seo()

# Pass to writer agent (example)
from content_generators.text_generator import TextGenerator

writer = TextGenerator()
post = writer.generate_blog_post(top_topic['topic'])

# Enhance with SEO keywords
post['seo_keywords'] = top_topic['seo_keywords']
post['search_intent'] = top_topic['search_intent']
```

### SEO Optimization Agent Integration

The keyword data can be used for SEO optimization:

```python
# Get SEO data
seo_data = research_agent.analyze_seo_keywords("Your Topic Here")

# Use in SEO optimization
def optimize_content(content, seo_data):
    # Ensure primary keywords appear in title
    # Include secondary keywords in headers
    # Use long-tail keywords in body text
    pass
```

## Configuration

The Research Agent uses settings from the main configuration:

```python
# In config/settings.py or .env file
OPENAI_API_KEY=your_openai_api_key
CONTENT_TOPICS=technology,AI,innovation,science
```

## Error Handling

The agent includes robust error handling with fallback mechanisms:

- **API Failures**: Automatically falls back to template-based topic generation
- **Retry Logic**: Uses exponential backoff for transient failures (up to 3 attempts)
- **Logging**: Comprehensive logging for debugging and monitoring

```python
import logging

# Configure logging to see research agent activity
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('agents.research_agent')
```

## Performance Considerations

- **API Calls**: Each research summary makes multiple OpenAI API calls
- **Rate Limiting**: Built-in retry logic respects API rate limits
- **Caching**: Consider caching research results for repeated use
- **Cost**: Be mindful of API usage costs with large topic counts

### Optimization Tips

```python
# Research once, use multiple times
summary = research_agent.generate_research_summary(topic_count=10)

# Cache for the day
import json
with open('research_cache.json', 'w') as f:
    json.dump(summary, f)

# Load cached research
with open('research_cache.json', 'r') as f:
    cached_summary = json.load(f)
```

## Testing

The agent includes comprehensive test coverage. Run tests with:

```bash
python -m unittest tests.test_research_agent
```

## Examples

### Complete Workflow Example

```python
from agents.research_agent import ResearchAgent
from content_generators.text_generator import TextGenerator

# Initialize agents
research_agent = ResearchAgent()
text_generator = TextGenerator()

# Research trending topics
print("Researching trending topics...")
summary = research_agent.generate_research_summary(topic_count=3)

# Select best topic
best_topic = max(summary['research_results'], key=lambda x: x['trend_score'])
print(f"\nSelected topic: {best_topic['topic']}")
print(f"Trend score: {best_topic['trend_score']}/10")

# Generate content with SEO optimization
print("\nGenerating content...")
post = text_generator.generate_blog_post(best_topic['topic'])

# Add SEO metadata
post['seo_keywords'] = best_topic['seo_keywords']
post['search_intent'] = best_topic['search_intent']
post['content_recommendations'] = best_topic['content_recommendations']

print(f"\nGenerated post: {post['title']}")
print(f"Word count: {post['word_count']}")
print(f"Primary keywords: {', '.join(best_topic['seo_keywords']['primary'])}")
```

### Batch Research Example

```python
# Research multiple topic areas
topic_areas = [
    ["AI", "machine learning", "deep learning"],
    ["blockchain", "cryptocurrency", "web3"],
    ["cybersecurity", "privacy", "data protection"]
]

all_research = []
for topics in topic_areas:
    summary = research_agent.generate_research_summary(
        topic_count=2,
        base_topics=topics
    )
    all_research.extend(summary['research_results'])

# Sort by trend score
sorted_topics = sorted(all_research, key=lambda x: x['trend_score'], reverse=True)

print("Top 5 trending topics across all areas:")
for i, topic in enumerate(sorted_topics[:5], 1):
    print(f"{i}. {topic['topic']} (Score: {topic['trend_score']}/10)")
```

## API Reference

### ResearchAgent Class

#### `__init__()`
Initialize the research agent with OpenAI client.

#### `discover_trending_topics(base_topics=None, count=5)`
Discover trending topics based on current trends.

**Parameters:**
- `base_topics` (List[str], optional): Topics to focus on. Defaults to settings.
- `count` (int): Number of topics to discover. Default: 5

**Returns:** List[Dict] - List of topic dictionaries

#### `analyze_seo_keywords(topic, target_keywords=None)`
Analyze and generate SEO keywords for a topic.

**Parameters:**
- `topic` (str): The topic to analyze
- `target_keywords` (List[str], optional): Target keywords to include

**Returns:** Dict - SEO keyword analysis

#### `generate_research_summary(topic_count=3, base_topics=None)`
Generate complete research summary with topics and SEO.

**Parameters:**
- `topic_count` (int): Number of topics to research. Default: 3
- `base_topics` (List[str], optional): Topics to focus on

**Returns:** Dict - Complete research summary

#### `get_top_topic_with_seo(base_topics=None)`
Get the single best trending topic with SEO analysis.

**Parameters:**
- `base_topics` (List[str], optional): Topics to focus on

**Returns:** Dict - Single topic with SEO analysis

## Troubleshooting

### Common Issues

**Issue**: No topics discovered
```python
# Solution: Check your OpenAI API key and base topics
research_agent = ResearchAgent()
try:
    topics = research_agent.discover_trending_topics()
except Exception as e:
    print(f"Error: {e}")
    # Falls back to template-based generation
```

**Issue**: SEO analysis returns minimal keywords
```python
# Solution: Provide more specific topic or target keywords
seo_data = research_agent.analyze_seo_keywords(
    "Specific Topic with Context",
    target_keywords=["relevant", "keywords"]
)
```

## Contributing

To extend the Research Agent:

1. Add new trend sources (e.g., Google Trends API, Twitter API)
2. Enhance SEO analysis with actual search volume data
3. Add topic scoring algorithms
4. Implement caching mechanisms

## License

Part of the Substack Auto project. See main repository for license information.
