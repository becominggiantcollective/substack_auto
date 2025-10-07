# Substack Auto - Agents Documentation

This directory contains documentation for the various AI agents used in the Substack Auto content generation system.

## Available Agents

### [Fact-Checker Agent](agents/fact_checker_agent.md)
Validates factual accuracy of articles and ensures SEO compliance on claims/statistics.

**Key Features:**
- Extracts and validates claims/statistics from articles
- Cross-references claims using AI-powered analysis
- Checks if statistics/claims enhance SEO (e.g., featured snippets)
- Outputs flagged claims, confidence scores, and SEO impact reports

**Status:** ✅ Implemented

## Future Agents

Additional agents planned for future releases:
- SEO Optimization Agent
- Content Enhancement Agent
- Plagiarism Detection Agent
- Tone Consistency Agent

## Integration

All agents are designed to integrate seamlessly with the ContentOrchestrator in `src/main.py`. Agents can be enabled/disabled based on requirements.

For general system documentation, see the main [README.md](../README.md) in the repository root.
