# Fact-Checker Agent Documentation

## Overview

The Fact-Checker Agent is an AI-powered validation system that analyzes article content to verify factual claims, assess statistical accuracy, and evaluate SEO compliance. It provides detailed reports with confidence scores and actionable recommendations.

## Features

### Core Capabilities

1. **Claim Extraction**
   - Automatically identifies factual claims and statistics in articles
   - Categorizes claims by type (statistic, fact, prediction, opinion)
   - Provides contextual information for each claim

2. **Claim Validation**
   - Cross-references claims with AI knowledge base
   - Calculates confidence scores (0.0 - 1.0)
   - Flags potentially inaccurate or unverifiable claims
   - Suggests verification sources

3. **SEO Assessment**
   - Evaluates SEO value of each claim
   - Identifies featured snippet opportunities
   - Rates claims as high, medium, or low SEO value
   - Calculates overall SEO score

4. **Comprehensive Reporting**
   - Generates detailed validation reports
   - Provides actionable recommendations
   - Flags claims that need review
   - Summarizes quality metrics

## Installation and Setup

The Fact-Checker Agent is integrated into the Substack Auto system and requires:

```python
# Required environment variables (already configured in .env)
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Basic Usage

```python
from agents.fact_checker_agent import FactCheckerAgent

# Initialize the agent
fact_checker = FactCheckerAgent()

# Process an article
content = {
    "title": "The Future of AI in 2024",
    "content": "Article content with claims and statistics..."
}

# Get full fact-checking report
report = fact_checker.process(content)

# Quick quality check
quality = fact_checker.check_article_quality(content)
```

### Integration with Content Generation

```python
from main import ContentOrchestrator
from agents.fact_checker_agent import FactCheckerAgent

# Initialize
orchestrator = ContentOrchestrator()
fact_checker = FactCheckerAgent()

# Generate content
content = orchestrator.generate_complete_content()

# Validate before publishing
validation = fact_checker.process(content["post_data"])

if validation["summary"]["overall_status"] == "pass":
    orchestrator.publish_content(content)
else:
    print("Content needs review:", validation["recommendations"])
```

## API Reference

### FactCheckerAgent Class

#### `__init__()`
Initialize the Fact-Checker Agent.

**Parameters:** None

**Example:**
```python
agent = FactCheckerAgent()
```

#### `process(content: Dict) -> Dict`
Process content and validate all claims.

**Parameters:**
- `content` (Dict): Dictionary with keys:
  - `title` (str): Article title
  - `content` (str): Article content

**Returns:**
- `Dict`: Complete validation report with:
  - `summary`: Overall statistics
  - `claims`: List of extracted claims
  - `validations`: Validation results for each claim
  - `flagged_claims`: Claims needing review
  - `recommendations`: Actionable suggestions
  - `seo_report`: SEO assessment
  - `generated_at`: Timestamp
  - `agent`: Agent name

**Example:**
```python
report = agent.process({
    "title": "AI Market Growth",
    "content": "The AI market grew 47% to reach $150 billion..."
})

print(f"Total claims: {report['summary']['total_claims_extracted']}")
print(f"Flagged: {report['summary']['flagged_claims']}")
```

#### `check_article_quality(content: Dict) -> Dict`
Quick quality assessment of an article.

**Parameters:**
- `content` (Dict): Article content dictionary

**Returns:**
- `Dict`: Quality assessment with:
  - `quality_score` (float): Overall quality (0.0-1.0)
  - `passes_quality_check` (bool): Whether article passes threshold
  - `confidence` (float): Average confidence score
  - `seo_score` (float): SEO optimization score
  - `issues_count` (int): Number of flagged claims
  - `recommendation` (str): Publishing recommendation

**Example:**
```python
quality = agent.check_article_quality(content)

if quality["passes_quality_check"]:
    print(f"Quality score: {quality['quality_score']}")
    print(f"Recommendation: {quality['recommendation']}")
```

#### `validate_input(content: Dict) -> bool`
Validate input content structure.

**Parameters:**
- `content` (Dict): Content to validate

**Returns:**
- `bool`: True if valid, False otherwise

## Report Structure

### Summary Section
```json
{
  "summary": {
    "total_claims_extracted": 5,
    "claims_validated": 5,
    "valid_claims": 4,
    "flagged_claims": 1,
    "average_confidence": 0.82,
    "overall_status": "review_needed"
  }
}
```

### Validation Results
```json
{
  "validations": [
    {
      "claim_id": 1,
      "claim_text": "AI adoption increased by 47%",
      "is_valid": true,
      "confidence_score": 0.85,
      "reasoning": "Consistent with industry reports",
      "potential_sources": ["Gartner", "McKinsey"],
      "flags": [],
      "needs_review": false,
      "seo_value": "high",
      "seo_reasoning": "Specific statistic good for featured snippets",
      "validated_at": "2024-10-11T06:30:00"
    }
  ]
}
```

### SEO Report
```json
{
  "seo_report": {
    "seo_score": 0.75,
    "total_claims": 5,
    "seo_distribution": {
      "high": 3,
      "medium": 1,
      "low": 1,
      "unknown": 0
    },
    "high_value_claims": [
      {
        "claim": "Market reached $150 billion",
        "reasoning": "Concrete data point for featured snippet"
      }
    ],
    "recommendations": [
      "Strong SEO foundation - claims are specific and valuable"
    ],
    "featured_snippet_potential": true
  }
}
```

### Recommendations
```json
{
  "recommendations": [
    {
      "claim": "Some unverified statistic",
      "issue": "Cannot find verification source",
      "action": "Verify with sources: Industry reports, Official data",
      "confidence": 0.45
    }
  ]
}
```

## Configuration

### Confidence Threshold
The agent uses a confidence threshold of 0.7 by default. Claims below this threshold are flagged for review.

```python
agent = FactCheckerAgent()
agent.confidence_threshold = 0.8  # Adjust as needed
```

### SEO Scoring

SEO values are calculated based on:
- **High (1.0)**: Specific statistics, verifiable data, featured snippet potential
- **Medium (0.6)**: General facts with some verification potential
- **Low (0.3)**: Vague statements or opinions

Overall SEO score: `(high_count × 1.0 + medium_count × 0.6 + low_count × 0.3) / total_claims`

## Best Practices

### 1. Pre-Publication Validation
Always validate content before publishing:

```python
# Generate content
content = orchestrator.generate_complete_content()

# Validate
report = fact_checker.process(content["post_data"])

# Check quality
if report["summary"]["overall_status"] != "pass":
    print("Review needed:", report["flagged_claims"])
```

### 2. Automated Quality Gates
Set up quality thresholds:

```python
quality = fact_checker.check_article_quality(content)

if quality["quality_score"] >= 0.8:
    # Publish immediately
    orchestrator.publish_content(content)
elif quality["quality_score"] >= 0.6:
    # Save as draft for review
    publisher.create_draft_post(content)
else:
    # Regenerate content
    content = orchestrator.generate_complete_content()
```

### 3. SEO Optimization
Use SEO recommendations to improve content:

```python
report = fact_checker.process(content)
seo_report = report["seo_report"]

if not seo_report["featured_snippet_potential"]:
    print("Add more specific statistics")
    print("Recommendations:", seo_report["recommendations"])
```

### 4. Iterative Improvement
Track validation over time:

```python
# Store validation results
validations = []

for post in generated_posts:
    result = fact_checker.check_article_quality(post)
    validations.append({
        "title": post["title"],
        "quality_score": result["quality_score"],
        "timestamp": datetime.now()
    })

# Analyze trends
avg_quality = sum(v["quality_score"] for v in validations) / len(validations)
```

## Claim Types

The agent categorizes claims into four types:

1. **Statistic**: Numerical data or percentages
   - Example: "AI adoption increased by 47%"
   - SEO Value: Typically high

2. **Fact**: Verifiable factual statement
   - Example: "Python is a programming language"
   - SEO Value: Medium to high

3. **Prediction**: Future-oriented claims
   - Example: "AI will transform healthcare by 2025"
   - SEO Value: Medium (less verifiable)

4. **Opinion**: Subjective statements
   - Example: "AI is the most exciting technology"
   - SEO Value: Low (not verifiable)

## Error Handling

The agent includes robust error handling:

```python
try:
    report = fact_checker.process(content)
except Exception as e:
    print(f"Validation error: {e}")
    # Agent returns conservative results on error
```

On validation errors, the agent returns:
- `is_valid: False`
- `confidence_score: 0.0`
- `needs_review: True`
- Appropriate error flags

## Performance Considerations

### Processing Time
- Claim extraction: ~2-5 seconds
- Validation per claim: ~1-3 seconds
- Total for 5 claims: ~10-20 seconds

### API Usage
The agent uses OpenAI API calls:
- 1 call for claim extraction
- 1 call per claim for validation
- For 5 claims: ~6 API calls total

### Optimization Tips
1. Use `check_article_quality()` for quick assessments (fewer API calls)
2. Cache validation results for similar claims
3. Batch process multiple articles
4. Set appropriate confidence thresholds to reduce false positives

## Troubleshooting

### Common Issues

**Issue: No claims extracted**
- Content may be too short or lack factual statements
- Solution: Ensure content includes specific facts or statistics

**Issue: Low confidence scores**
- Claims may be too vague or unverifiable
- Solution: Add more specific, concrete data points

**Issue: All claims flagged**
- Content may contain misinformation or unverifiable claims
- Solution: Review and update claims with accurate sources

**Issue: Low SEO scores**
- Content lacks specific statistics or verifiable facts
- Solution: Add concrete data points and specific numbers

## Examples

### Example 1: High-Quality Article
```python
content = {
    "title": "Python Adoption in 2024",
    "content": """
    Python usage grew by 27% in 2023, according to the TIOBE Index.
    The language now has over 8 million developers worldwide.
    Stack Overflow's 2023 survey ranked Python as the 3rd most popular
    language, with 49.3% of developers using it regularly.
    """
}

report = fact_checker.process(content)
# Result: high confidence, strong SEO, pass status
```

### Example 2: Article Needing Review
```python
content = {
    "title": "The Best Programming Language",
    "content": """
    Everyone knows Python is the best language. It's obviously
    superior to all others and will replace everything soon.
    Most developers agree it's perfect.
    """
}

report = fact_checker.process(content)
# Result: low confidence, weak SEO, review_needed status
```

## Integration Examples

### With Content Orchestrator
```python
from main import ContentOrchestrator
from agents.fact_checker_agent import FactCheckerAgent

class QualityAwareOrchestrator(ContentOrchestrator):
    def __init__(self):
        super().__init__()
        self.fact_checker = FactCheckerAgent()
    
    def create_and_publish_post(self):
        # Generate content
        content = self.generate_complete_content()
        
        # Validate
        validation = self.fact_checker.process(content["post_data"])
        
        # Only publish if passes quality check
        if validation["summary"]["overall_status"] == "pass":
            return self.publish_content(content)
        else:
            self.logger.warning("Content failed validation")
            return {
                "success": False,
                "reason": "quality_check_failed",
                "validation": validation
            }
```

### With Custom Thresholds
```python
class StrictFactChecker(FactCheckerAgent):
    def __init__(self):
        super().__init__()
        self.confidence_threshold = 0.85  # Stricter threshold
    
    def meets_publication_standards(self, content):
        quality = self.check_article_quality(content)
        
        return (
            quality["quality_score"] >= 0.85 and
            quality["seo_score"] >= 0.7 and
            quality["issues_count"] == 0
        )
```

## Future Enhancements

Planned improvements for the Fact-Checker Agent:

1. **External Source Integration**
   - Google Search API integration
   - Wikipedia API for fact verification
   - Academic database connections

2. **Enhanced SEO Analysis**
   - Keyword optimization suggestions
   - Meta description recommendations
   - Schema markup suggestions

3. **Machine Learning**
   - Training on verified claims database
   - Pattern recognition for common misinformation
   - Improved confidence scoring

4. **Real-Time Verification**
   - Live fact-checking during content generation
   - Automatic claim correction suggestions
   - Source citation generation

## Support and Contributing

For issues or questions about the Fact-Checker Agent:
1. Review this documentation
2. Check the test suite for examples
3. Open an issue on GitHub with:
   - Agent version
   - Content sample (anonymized)
   - Expected vs actual behavior
   - Validation report

## License

This agent is part of the Substack Auto project and is licensed under the MIT License.

---

**Version:** 1.0.0  
**Last Updated:** October 11, 2024  
**Agent Name:** FactCheckerAgent
