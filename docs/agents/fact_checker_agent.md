# Fact-Checker Agent Documentation

## Overview

The Fact-Checker Agent is an automated validation system that ensures factual accuracy and SEO compliance in generated articles. It extracts claims, validates them against trusted sources, calculates confidence scores, and provides actionable recommendations for content optimization.

## Features

### 1. Claim Extraction
- Automatically identifies factual claims, statistics, and assertions in article content
- Categorizes claims by type (statistic, fact, prediction, opinion)
- Determines if claims are verifiable

### 2. Claim Validation
- Validates each claim using AI-powered analysis
- Assigns confidence scores (0-100) to each claim
- Provides assessment: ACCURATE, LIKELY_ACCURATE, UNCERTAIN, LIKELY_INACCURATE, INACCURATE
- Includes reasoning for each assessment

### 3. SEO Impact Analysis
- Evaluates the SEO potential of claims
- Calculates featured snippet potential (high/medium/low)
- Provides overall SEO score (0-100)
- Identifies high-impact claims for search visibility

### 4. Comprehensive Reporting
- Generates detailed reports in text or markdown format
- Flags low-confidence claims for review
- Provides actionable recommendations for improvement
- Includes overall status: PASS or REVIEW_NEEDED

## Usage

### Basic Usage

```python
from agents.fact_checker_agent import FactCheckerAgent

# Initialize the agent
fact_checker = FactCheckerAgent()

# Check an article
article_title = "The Rise of AI in Content Creation"
article_content = """
Recent studies show that AI-generated content has increased by 300% in 2024.
Machine learning algorithms can now produce text that is indistinguishable from human writing.
"""

# Perform fact-checking
report = fact_checker.check_article(article_title, article_content)

# Generate a formatted report
text_report = fact_checker.generate_report(report, output_format="text")
print(text_report)

# Or get a markdown report
markdown_report = fact_checker.generate_report(report, output_format="markdown")
```

### Integration with Content Generation Workflow

```python
from main import ContentOrchestrator
from agents.fact_checker_agent import FactCheckerAgent

orchestrator = ContentOrchestrator()
fact_checker = FactCheckerAgent()

# Generate content
content = orchestrator.generate_complete_content()

# Check the content
fact_check_report = fact_checker.check_article(
    content["post_data"]["title"],
    content["post_data"]["content"]
)

# Review status before publishing
if fact_check_report["overall_status"] == "PASS":
    print("Content passed fact-checking. Safe to publish.")
    orchestrator.publish_content(content)
else:
    print("Content needs review:")
    print(fact_checker.generate_report(fact_check_report))
```

## API Reference

### FactCheckerAgent Class

#### `__init__()`
Initialize the fact-checker agent with OpenAI client.

#### `extract_claims(content: str) -> List[Dict[str, str]]`
Extract factual claims and statistics from article content.

**Parameters:**
- `content` (str): The article content to analyze

**Returns:**
- List of dictionaries containing:
  - `claim`: The extracted claim text
  - `type`: Type of claim (statistic/fact/prediction/opinion)
  - `verifiable`: Whether the claim is verifiable (yes/no)

#### `validate_claim(claim: str) -> Dict[str, any]`
Validate a single claim and assess its accuracy.

**Parameters:**
- `claim` (str): The claim to validate

**Returns:**
- Dictionary containing:
  - `claim`: Original claim text
  - `confidence_score`: Score from 0-100
  - `assessment`: ACCURATE, LIKELY_ACCURATE, UNCERTAIN, etc.
  - `reasoning`: Explanation of the assessment
  - `sources_needed`: Whether external verification is needed
  - `seo_potential`: SEO impact (high/medium/low)
  - `validated_at`: Timestamp of validation

#### `assess_seo_impact(claims: List[Dict[str, any]]) -> Dict[str, any]`
Assess the overall SEO impact of claims in the article.

**Parameters:**
- `claims` (List[Dict]): List of validated claims

**Returns:**
- Dictionary containing:
  - `overall_score`: SEO score (0-100)
  - `featured_snippet_potential`: high/medium/low
  - `high_seo_claims`: Count of high-impact claims
  - `medium_seo_claims`: Count of medium-impact claims
  - `total_claims`: Total number of claims
  - `recommendations`: List of SEO improvement suggestions

#### `check_article(title: str, content: str) -> Dict[str, any]`
Perform complete fact-checking and SEO analysis on an article.

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content

**Returns:**
- Comprehensive report dictionary containing:
  - `article_title`: Title of the analyzed article
  - `analysis_timestamp`: When the analysis was performed
  - `claims_extracted`: Number of claims found
  - `claims_validated`: Number of claims validated
  - `flagged_claims_count`: Number of low-confidence claims
  - `average_confidence`: Average confidence score
  - `claims`: List of all claims with validation details
  - `flagged_claims`: List of problematic claims
  - `seo_analysis`: SEO impact assessment
  - `recommendations`: List of actionable recommendations
  - `overall_status`: PASS, REVIEW_NEEDED, or ERROR

#### `generate_report(check_result: Dict[str, any], output_format: str = "text") -> str`
Generate a formatted report from fact-checking results.

**Parameters:**
- `check_result` (Dict): Results from `check_article()`
- `output_format` (str): Format for the report ("text" or "markdown")

**Returns:**
- Formatted report string

## Report Structure

### Text Report Format
```
======================================================================
FACT-CHECKER REPORT
======================================================================
Article: [Title]
Analysis Date: [Timestamp]
Overall Status: [PASS/REVIEW_NEEDED]

SUMMARY:
  Claims Extracted: [count]
  Claims Validated: [count]
  Flagged Claims: [count]
  Average Confidence: [percentage]

SEO ANALYSIS:
  Overall SEO Score: [score]/100
  Featured Snippet Potential: [HIGH/MEDIUM/LOW]
  High-Impact Claims: [count]

FLAGGED CLAIMS (Low Confidence):
  - [Claim text]
    Confidence: [percentage]
    Assessment: [status]

RECOMMENDATIONS:
  • [Recommendation 1]
  • [Recommendation 2]
======================================================================
```

### Markdown Report Format
Reports can also be generated in markdown format for integration with documentation systems or publishing platforms.

## Configuration

The fact-checker requires the `OPENAI_API_KEY` environment variable to be set in your `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Integration Points

### 1. Pre-Publishing Validation
Integrate fact-checking before content publication:
```python
def create_and_publish_post(self):
    content = self.generate_complete_content()
    
    # Add fact-checking
    fact_check = self.fact_checker.check_article(
        content["post_data"]["title"],
        content["post_data"]["content"]
    )
    
    if fact_check["overall_status"] != "PASS":
        logger.warning("Fact-check review needed")
        # Save report for manual review
        
    return self.publish_content(content)
```

### 2. Post-Generation Enhancement
Use fact-checking results to enhance content:
```python
# Generate content
post_data = text_generator.create_complete_post()

# Check facts
fact_check = fact_checker.check_article(
    post_data["title"],
    post_data["content"]
)

# Use recommendations to improve SEO
if fact_check["seo_analysis"]["overall_score"] < 50:
    # Regenerate or enhance with more statistics
    pass
```

### 3. Batch Analysis
Analyze multiple articles:
```python
articles = load_articles()
reports = []

for article in articles:
    report = fact_checker.check_article(
        article["title"],
        article["content"]
    )
    reports.append(report)

# Generate summary statistics
avg_confidence = sum(r["average_confidence"] for r in reports) / len(reports)
```

## Best Practices

1. **Regular Validation**: Run fact-checking on all generated content before publication
2. **Review Flagged Claims**: Always manually review claims with confidence scores below 60%
3. **SEO Optimization**: Use SEO recommendations to enhance content visibility
4. **Source Verification**: For critical claims, verify against external authoritative sources
5. **Confidence Thresholds**: Set appropriate confidence thresholds based on your content type
6. **Documentation**: Save fact-checking reports for audit trails and quality assurance

## Limitations

1. **AI-Based Validation**: The agent uses AI to assess claim plausibility. For critical applications, manual verification with authoritative sources is recommended.
2. **API Dependencies**: Requires OpenAI API access. Consider implementing caching for repeated claims.
3. **External APIs**: In production environments, integrate with real search APIs (Google Search, Wikipedia) for enhanced validation.
4. **Language Support**: Currently optimized for English content. May require adjustments for other languages.

## Future Enhancements

1. **External API Integration**: 
   - Google Search API for real-time fact verification
   - Wikipedia API for encyclopedic fact-checking
   - Academic database APIs for scientific claims

2. **Source Citations**:
   - Automatic citation generation for validated claims
   - Link to authoritative sources

3. **Claim Database**:
   - Cache validated claims to improve performance
   - Build knowledge base of verified facts

4. **Advanced SEO**:
   - Keyword density analysis
   - Structured data recommendations
   - Featured snippet formatting suggestions

5. **Multi-Language Support**:
   - Support for fact-checking in multiple languages
   - Language-specific SEO recommendations

## Troubleshooting

### Issue: Low Confidence Scores
**Solution**: Ensure claims are specific and verifiable. Avoid vague or subjective statements.

### Issue: No Claims Extracted
**Solution**: Content may be too opinion-based. Add specific facts, statistics, or data points.

### Issue: Low SEO Scores
**Solution**: Include more quantifiable data, statistics, and specific factual assertions.

### Issue: API Errors
**Solution**: Check OpenAI API key configuration and rate limits.

## Support

For issues or questions about the Fact-Checker Agent:
1. Check this documentation
2. Review the implementation in `src/agents/fact_checker_agent.py`
3. Examine test cases in `tests/test_fact_checker.py`
4. Consult the main README.md for general system information
