#!/usr/bin/env python3
"""
Demonstration script for CrewAI and SEO agent functionality.

This script shows how to use the SEO analyzer to optimize content
for search engines.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.seo_agent import SEOAnalyzer, create_seo_agent, run_seo_crew


def demo_seo_analyzer():
    """Demonstrate basic SEO analyzer functionality."""
    print("=" * 70)
    print("SEO ANALYZER DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Create analyzer
    analyzer = SEOAnalyzer()
    
    # Sample blog post
    title = "10 Essential Tips for Mastering AI Content Creation in 2025"
    content = """
    Artificial Intelligence is revolutionizing content creation across all industries.
    From blog posts to social media updates, AI tools are enabling creators to produce
    high-quality content faster than ever before.
    
    In this comprehensive guide, we'll explore the most important strategies for
    leveraging AI in your content creation workflow. Whether you're a beginner or
    an experienced content creator, these tips will help you maximize the potential
    of AI-powered tools.
    
    Understanding the landscape of AI content creation is crucial for success.
    Machine learning algorithms have become sophisticated enough to understand
    context, tone, and audience preferences. This means you can create content
    that truly resonates with your target audience.
    
    The future of content creation lies in the synergy between human creativity
    and artificial intelligence. By combining your unique insights with AI's
    processing power, you can create content that stands out in a crowded
    digital landscape.
    """ * 5  # Repeat to get more realistic word count
    
    print("📝 ANALYZING BLOG POST")
    print("-" * 70)
    print(f"Title: {title}")
    print(f"Content Length: {len(content)} characters")
    print()
    
    # Generate full SEO report
    print("🔍 GENERATING SEO REPORT...")
    print()
    report = analyzer.generate_seo_report(title, content)
    
    # Display results
    print("📊 SEO ANALYSIS RESULTS")
    print("-" * 70)
    print(f"Overall Score: {report['overall_score']}/100")
    print()
    
    print("Title Analysis:")
    print(f"  • Length: {report['title_analysis']['length']} characters")
    print(f"  • Word Count: {report['title_analysis']['word_count']} words")
    print(f"  • URL Slug: {report['title_analysis']['slug']}")
    print()
    
    print("Content Analysis:")
    print(f"  • Word Count: {report['content_analysis']['word_count']} words")
    print(f"  • Paragraph Count: {report['content_analysis']['paragraph_count']}")
    print()
    
    print("Meta Information:")
    print(f"  • Meta Description: {report['meta_description'][:100]}...")
    print(f"  • URL Slug: {report['slug']}")
    print()
    
    print("Top Keywords:")
    for i, kw in enumerate(report['content_analysis']['top_keywords'][:5], 1):
        print(f"  {i}. {kw['keyword']} ({kw['count']} occurrences)")
    print()
    
    print("Recommendations:")
    for i, rec in enumerate(report['recommendations'][:5], 1):
        print(f"  {i}. {rec}")
    print()
    
    return report


def demo_seo_functions():
    """Demonstrate individual SEO functions."""
    print("=" * 70)
    print("INDIVIDUAL SEO FUNCTIONS DEMONSTRATION")
    print("=" * 70)
    print()
    
    analyzer = SEOAnalyzer()
    
    # Test slug generation
    print("🔗 SLUG GENERATION")
    print("-" * 70)
    test_titles = [
        "How to Build Better AI Models",
        "The Future of Machine Learning: What's Next?",
        "Top 10 Python Libraries for Data Science in 2025"
    ]
    
    for title in test_titles:
        slug = analyzer.generate_slug(title)
        print(f"Title: {title}")
        print(f"Slug:  {slug}")
        print()
    
    # Test title analysis
    print("📋 TITLE ANALYSIS")
    print("-" * 70)
    
    titles = [
        ("Short", "Too short title"),
        ("Perfect Length SEO Title for Search Optimization", "Optimal title"),
        ("This is an Extremely Long Title That Exceeds Recommended Character Limits for SEO Best Practices", "Too long title")
    ]
    
    for title, desc in titles:
        analysis = analyzer.analyze_title(title)
        print(f"{desc}:")
        print(f"  Title: {title}")
        print(f"  Length: {analysis['length']} chars")
        print(f"  Assessment: {analysis['recommendations'][0]}")
        print()
    
    # Test meta description
    print("📝 META DESCRIPTION GENERATION")
    print("-" * 70)
    
    sample_content = """
    Learn how to leverage artificial intelligence for content creation.
    This comprehensive guide covers everything from basic concepts to
    advanced techniques. Perfect for beginners and experienced creators alike.
    """
    
    meta = analyzer.generate_meta_description(sample_content, max_length=160)
    print(f"Content: {sample_content.strip()[:100]}...")
    print(f"Meta Description: {meta}")
    print(f"Length: {len(meta)} characters")
    print()


def demo_crewai_integration():
    """Demonstrate CrewAI integration (if available)."""
    print("=" * 70)
    print("CREWAI INTEGRATION DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Try to create a CrewAI agent
    agent = create_seo_agent()
    
    if agent is None:
        print("⚠️  CrewAI is not available in this environment.")
        print("    Install CrewAI with: pip install crewai crewai-tools")
        print()
        print("    When CrewAI is installed, you can:")
        print("    • Create multi-agent workflows")
        print("    • Coordinate complex SEO optimization tasks")
        print("    • Leverage advanced AI capabilities")
        print()
    else:
        print("✅ CrewAI agent created successfully!")
        print(f"   Agent Role: SEO Specialist")
        print()
        
        # Try to run a crew
        result = run_seo_crew(
            "Sample Title for Testing",
            "Sample content for CrewAI testing"
        )
        print("CrewAI Analysis Result:")
        print(result)
        print()


def main():
    """Run all demonstrations."""
    print()
    print("🤖 SUBSTACK AUTO - SEO AGENT DEMONSTRATION")
    print()
    
    # Run basic SEO analyzer demo
    demo_seo_analyzer()
    
    # Run individual functions demo
    demo_seo_functions()
    
    # Run CrewAI integration demo
    demo_crewai_integration()
    
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("📚 Learn More:")
    print("   • See src/agents/seo_agent.py for full API documentation")
    print("   • Run tests with: python -m unittest tests.test_agents")
    print("   • Check README.md for integration examples")
    print()


if __name__ == "__main__":
    main()
