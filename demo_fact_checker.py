#!/usr/bin/env python3
"""
Demo script showcasing the Fact-Checker Agent functionality.

This demonstrates how the agent validates claims, assesses SEO, and generates reports.
"""
import os
import sys
import json
from datetime import datetime

# Set up test environment
os.environ.update({
    'OPENAI_API_KEY': 'demo_key_not_functional',
    'SUBSTACK_EMAIL': 'demo@example.com',
    'SUBSTACK_PASSWORD': 'demo_password',
    'SUBSTACK_PUBLICATION': 'demo_publication'
})

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.fact_checker_agent import FactCheckerAgent


def demo_fact_checker():
    """Demonstrate fact-checker capabilities."""
    print("✅ Fact-Checker Agent Demo")
    print("=" * 50)
    print()
    
    # Sample article with various types of claims
    sample_article = {
        "title": "The Evolution of AI in 2024",
        "content": """
        The artificial intelligence industry has experienced remarkable growth.
        According to recent market analysis, AI adoption increased by 47% in 2023,
        with the global market reaching $150 billion. Industry experts predict
        the market will grow to $500 billion by 2027.
        
        Machine learning algorithms can now process over 1 million data points
        per second, a 300% improvement from 2022. The technology has been adopted
        by 75% of Fortune 500 companies, transforming how businesses operate.
        
        Python remains the most popular language for AI development, with
        8.2 million developers worldwide using it for machine learning projects.
        The programming language saw a 27% increase in usage according to
        the TIOBE Index.
        
        Experts believe that AI will revolutionize healthcare, with some claiming
        it could save millions of lives. The future of AI is incredibly exciting
        and will change everything we know about technology.
        """
    }
    
    print("📄 Sample Article")
    print("-" * 50)
    print(f"Title: {sample_article['title']}")
    print(f"Content: {len(sample_article['content'])} characters")
    print()
    
    # Initialize fact-checker
    print("🔍 Initializing Fact-Checker Agent...")
    fact_checker = FactCheckerAgent()
    print("✓ Agent initialized")
    print()
    
    # Extract claims (demonstration mode - using fallback)
    print("📊 Extracting Claims...")
    print("-" * 50)
    claims = fact_checker._extract_claims_fallback(sample_article['content'])
    print(f"✓ Extracted {len(claims)} statistical claims")
    
    for i, claim in enumerate(claims[:5], 1):  # Show first 5
        print(f"\n{i}. Type: {claim['type']}")
        print(f"   Claim: {claim['text']}")
        print(f"   Context: {claim['context'][:80]}...")
    
    print()
    print()
    
    # Demonstrate validation results (mock data for demo)
    print("✅ Validation Results (Demo Mode)")
    print("-" * 50)
    
    demo_validations = [
        {
            "claim": "AI adoption increased by 47% in 2023",
            "is_valid": True,
            "confidence": 0.85,
            "seo_value": "high",
            "reasoning": "Specific statistic with verifiable sources"
        },
        {
            "claim": "Market reached $150 billion",
            "is_valid": True,
            "confidence": 0.80,
            "seo_value": "high",
            "reasoning": "Concrete data point good for featured snippets"
        },
        {
            "claim": "75% of Fortune 500 companies",
            "is_valid": True,
            "confidence": 0.75,
            "seo_value": "medium",
            "reasoning": "Plausible but needs source verification"
        },
        {
            "claim": "Could save millions of lives",
            "is_valid": False,
            "confidence": 0.40,
            "seo_value": "low",
            "reasoning": "Too vague, unverifiable prediction"
        }
    ]
    
    for i, val in enumerate(demo_validations, 1):
        status = "✓ VALID" if val['is_valid'] else "⚠ NEEDS REVIEW"
        print(f"\n{i}. {status}")
        print(f"   Claim: {val['claim']}")
        print(f"   Confidence: {val['confidence']:.0%}")
        print(f"   SEO Value: {val['seo_value'].upper()}")
        print(f"   Reasoning: {val['reasoning']}")
    
    print()
    print()
    
    # SEO Assessment
    print("🎯 SEO Assessment")
    print("-" * 50)
    
    seo_report = {
        "seo_score": 0.72,
        "total_claims": 4,
        "seo_distribution": {
            "high": 2,
            "medium": 1,
            "low": 1
        },
        "featured_snippet_potential": True,
        "recommendations": [
            "Strong foundation with specific statistics",
            "Replace vague predictions with concrete facts",
            "Add sources for medium-confidence claims"
        ]
    }
    
    print(f"Overall SEO Score: {seo_report['seo_score']:.0%}")
    print(f"Featured Snippet Potential: {'✓ Yes' if seo_report['featured_snippet_potential'] else '✗ No'}")
    print()
    print("SEO Value Distribution:")
    for level, count in seo_report['seo_distribution'].items():
        print(f"  {level.capitalize()}: {count} claims")
    
    print()
    print("Recommendations:")
    for i, rec in enumerate(seo_report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print()
    print()
    
    # Quality Summary
    print("📋 Quality Summary")
    print("-" * 50)
    
    summary = {
        "total_claims": 4,
        "valid_claims": 3,
        "flagged_claims": 1,
        "average_confidence": 0.70,
        "quality_score": 0.77,
        "recommendation": "Review before publishing"
    }
    
    print(f"Total Claims Extracted: {summary['total_claims']}")
    print(f"Valid Claims: {summary['valid_claims']}")
    print(f"Flagged for Review: {summary['flagged_claims']}")
    print(f"Average Confidence: {summary['average_confidence']:.0%}")
    print(f"Quality Score: {summary['quality_score']:.0%}")
    print(f"\nRecommendation: {summary['recommendation']}")
    
    print()
    print()
    
    # Integration Example
    print("🔗 Integration Example")
    print("-" * 50)
    print("""
    # In your content workflow:
    
    from main import ContentOrchestrator
    from agents.fact_checker_agent import FactCheckerAgent
    
    orchestrator = ContentOrchestrator()
    fact_checker = FactCheckerAgent()
    
    # Generate content
    content = orchestrator.generate_complete_content()
    
    # Validate with fact-checker (automatic in orchestrator)
    report = content['fact_check']
    
    # Check quality before publishing
    if report['summary']['overall_status'] == 'pass':
        orchestrator.publish_content(content)
    else:
        print("Review needed:", report['recommendations'])
    """)
    
    print()
    print("=" * 50)
    print("✅ Demo Complete!")
    print()
    print("For full documentation, see: docs/fact_checker_agent.md")
    print()


def demo_api_reference():
    """Show quick API reference."""
    print()
    print("📚 Quick API Reference")
    print("=" * 50)
    print()
    
    print("Initialize:")
    print("  agent = FactCheckerAgent()")
    print()
    
    print("Process article:")
    print("  report = agent.process({")
    print("      'title': 'Article Title',")
    print("      'content': 'Article content...'")
    print("  })")
    print()
    
    print("Quick quality check:")
    print("  quality = agent.check_article_quality(content)")
    print("  if quality['passes_quality_check']:")
    print("      # Good to publish")
    print()
    
    print("Report structure:")
    print("  report = {")
    print("      'summary': {...},           # Overall statistics")
    print("      'claims': [...],            # Extracted claims")
    print("      'validations': [...],       # Validation results")
    print("      'flagged_claims': [...],    # Claims needing review")
    print("      'recommendations': [...],   # Actionable suggestions")
    print("      'seo_report': {...}         # SEO assessment")
    print("  }")
    print()


if __name__ == "__main__":
    demo_fact_checker()
    demo_api_reference()
