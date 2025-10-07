#!/usr/bin/env python3
"""
Example script demonstrating the Fact-Checker Agent.

This script shows how to use the FactCheckerAgent to validate claims
and assess SEO impact of article content.
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.fact_checker_agent import FactCheckerAgent


def example_basic_usage():
    """Demonstrate basic fact-checking usage."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Fact-Checking")
    print("=" * 70)
    print()
    
    # Initialize the agent
    fact_checker = FactCheckerAgent()
    
    # Sample article
    article_title = "The Rise of AI in Content Creation"
    article_content = """
    Recent studies show that AI-generated content has increased by 300% in 2024.
    Machine learning algorithms can now produce text that is indistinguishable 
    from human writing in most contexts.
    
    Over 60% of digital content creators are now using AI tools in their workflow,
    according to industry surveys. This trend is expected to continue growing as
    the technology becomes more accessible and affordable.
    
    AI has the potential to revolutionize content creation, making it faster and
    more efficient than ever before.
    """
    
    # Perform fact-checking
    print(f"Analyzing article: '{article_title}'")
    print()
    report = fact_checker.check_article(article_title, article_content)
    
    # Generate and display report
    text_report = fact_checker.generate_report(report, output_format="text")
    print(text_report)


def example_seo_analysis():
    """Demonstrate SEO impact analysis."""
    print("=" * 70)
    print("EXAMPLE 2: SEO Impact Analysis")
    print("=" * 70)
    print()
    
    fact_checker = FactCheckerAgent()
    
    # Article with various types of claims
    article_title = "5 Data-Driven Marketing Strategies for 2024"
    article_content = """
    Email marketing has an average ROI of 4200%, making it one of the most
    cost-effective marketing channels available. Companies that segment their
    email lists see a 760% increase in revenue.
    
    Video content is 50x more likely to drive organic search results than
    plain text. Mobile video consumption rises by 100% every year, according
    to recent analytics.
    
    Personalized marketing campaigns can increase conversion rates by up to 202%.
    Marketing automation can save businesses an average of 6 hours per week on
    repetitive tasks.
    """
    
    print(f"Analyzing article: '{article_title}'")
    print()
    report = fact_checker.check_article(article_title, article_content)
    
    # Display SEO-specific insights
    print("SEO ANALYSIS RESULTS:")
    print("-" * 70)
    seo = report.get("seo_analysis", {})
    print(f"Overall SEO Score: {seo.get('overall_score', 0)}/100")
    print(f"Featured Snippet Potential: {seo.get('featured_snippet_potential', 'N/A').upper()}")
    print(f"High-Impact Claims: {seo.get('high_seo_claims', 0)}")
    print(f"Medium-Impact Claims: {seo.get('medium_seo_claims', 0)}")
    print()
    print("Recommendations:")
    for rec in seo.get("recommendations", []):
        print(f"  • {rec}")
    print()


def example_markdown_report():
    """Demonstrate markdown report generation."""
    print("=" * 70)
    print("EXAMPLE 3: Markdown Report Generation")
    print("=" * 70)
    print()
    
    fact_checker = FactCheckerAgent()
    
    article_title = "Understanding Climate Change Statistics"
    article_content = """
    Global temperatures have risen by 1.1°C since pre-industrial times.
    Arctic sea ice is declining at a rate of 13% per decade.
    
    Scientists agree that human activities are the primary cause of
    recent climate change. This consensus is supported by multiple
    independent studies and research institutions worldwide.
    """
    
    print(f"Analyzing article: '{article_title}'")
    print()
    report = fact_checker.check_article(article_title, article_content)
    
    # Generate markdown report
    markdown_report = fact_checker.generate_report(report, output_format="markdown")
    print("Markdown Report Generated:")
    print("-" * 70)
    print(markdown_report)


def example_integration_workflow():
    """Demonstrate integration with content generation workflow."""
    print("=" * 70)
    print("EXAMPLE 4: Integration with Content Workflow")
    print("=" * 70)
    print()
    
    print("This example shows how fact-checking integrates with content generation:")
    print()
    print("1. Generate content using TextGenerator")
    print("2. Run fact-checker on generated content")
    print("3. Review fact-check report")
    print("4. Decide whether to publish or revise based on report")
    print()
    print("Sample workflow code:")
    print("-" * 70)
    print("""
from main import ContentOrchestrator

orchestrator = ContentOrchestrator()

# Generate content
content = orchestrator.generate_complete_content()

# Fact-check the content
fact_check_report = orchestrator.fact_check_content(content)

# Check status before publishing
if fact_check_report["overall_status"] == "PASS":
    print("Content passed fact-checking. Publishing...")
    orchestrator.publish_content(content)
else:
    print("Content needs review. See report for details.")
    print(orchestrator.fact_checker.generate_report(fact_check_report))
    """)
    print("-" * 70)


def main():
    """Run all examples."""
    print()
    print("🔍 Fact-Checker Agent Examples")
    print("=" * 70)
    print()
    print("This script demonstrates various features of the FactCheckerAgent.")
    print("Note: These examples use mock data for demonstration purposes.")
    print()
    
    try:
        # Run examples in sequence
        example_basic_usage()
        print("\n" * 2)
        
        example_seo_analysis()
        print("\n" * 2)
        
        example_markdown_report()
        print("\n" * 2)
        
        example_integration_workflow()
        print("\n" * 2)
        
        print("=" * 70)
        print("✅ All examples completed!")
        print("=" * 70)
        print()
        print("For more information, see:")
        print("  - docs/agents/fact_checker_agent.md")
        print("  - src/agents/fact_checker_agent.py")
        print()
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("  1. Set OPENAI_API_KEY in your environment")
        print("  2. Installed all required dependencies (pip install -r requirements.txt)")
        sys.exit(1)


if __name__ == "__main__":
    main()
