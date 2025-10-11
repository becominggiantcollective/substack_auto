"""
Example demonstrating the Writer Agent functionality.

This script shows how to use the Writer Agent to generate SEO-optimized content.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.writer_agent import WriterAgent


def demo_basic_usage():
    """Demonstrate basic Writer Agent usage."""
    print("=" * 80)
    print("Writer Agent - Basic Usage Demo")
    print("=" * 80)
    print()
    
    # Initialize the agent (requires OPENAI_API_KEY in .env)
    writer = WriterAgent()
    
    # Example input (as would come from a Research Agent)
    topic = "The Future of Artificial Intelligence in Healthcare"
    keywords = ["AI", "healthcare", "medical technology", "machine learning", "diagnostics"]
    research_summary = """
    Artificial intelligence is revolutionizing healthcare through advanced diagnostics,
    personalized treatment plans, and predictive analytics. AI-powered systems can
    analyze medical images with accuracy rivaling human experts. Machine learning
    algorithms help predict disease progression and optimize treatment protocols.
    The integration of AI in healthcare promises improved patient outcomes and
    reduced costs, though challenges around data privacy and ethical considerations
    remain. Healthcare providers are increasingly adopting AI solutions for
    administrative tasks, clinical decision support, and patient monitoring.
    """
    
    print(f"Topic: {topic}")
    print(f"Keywords: {', '.join(keywords)}")
    print(f"Research Summary: {research_summary.strip()[:100]}...")
    print()
    print("-" * 80)
    print("Generating complete SEO-optimized content...")
    print("-" * 80)
    print()
    
    # Note: This would make real API calls if OPENAI_API_KEY is set
    # For demo purposes, we'll show the structure
    
    print("✓ Content generation would include:")
    print("  • Article (800-1200 words)")
    print("  • Meta Title (max 60 chars)")
    print("  • Meta Description (max 155 chars)")
    print("  • Tags (5-8 suggested tags)")
    print("  • Keyword Density Analysis")
    print("  • Structure Validation")
    print("  • SEO Score (0-100)")
    print()
    
    # Example of what the output would look like
    print("Expected Output Structure:")
    print("-" * 80)
    print("""
    {
        "title": "The Future of Artificial Intelligence in Healthcare",
        "article": "Full article content with 800-1200 words...",
        "meta_title": "AI in Healthcare: Future of Medical Technology",
        "meta_description": "Discover how AI is transforming healthcare with advanced diagnostics...",
        "tags": ["AI", "healthcare", "medical technology", "machine learning"],
        "word_count": 1050,
        "keyword_densities": {
            "AI": 0.021,
            "healthcare": 0.019,
            "medical technology": 0.015
        },
        "structure_validation": {
            "has_paragraphs": True,
            "has_sufficient_length": True,
            "has_opening": True,
            "has_sections": True
        },
        "seo_score": 92,
        "ai_generated": True
    }
    """)
    print()


def demo_keyword_density():
    """Demonstrate keyword density calculation."""
    print("=" * 80)
    print("Writer Agent - Keyword Density Analysis Demo")
    print("=" * 80)
    print()
    
    writer = WriterAgent()
    
    # Sample content
    content = """
    Artificial intelligence is transforming modern healthcare. AI systems can analyze
    medical data with unprecedented accuracy. Healthcare providers use AI for diagnostics,
    treatment planning, and patient monitoring. The integration of AI in healthcare
    continues to grow as technology advances.
    """
    
    keywords = ["AI", "healthcare", "technology"]
    
    print("Sample Content:")
    print("-" * 80)
    print(content.strip())
    print()
    
    print(f"Analyzing keywords: {', '.join(keywords)}")
    print()
    
    densities = writer.calculate_keyword_density(content, keywords)
    
    print("Keyword Density Results:")
    print("-" * 80)
    for keyword, density in densities.items():
        percentage = density * 100
        status = "✓ Optimal" if 1.5 <= percentage <= 2.5 else "⚠ Adjust"
        print(f"  {keyword}: {percentage:.2f}% {status}")
    print()


def demo_structure_validation():
    """Demonstrate content structure validation."""
    print("=" * 80)
    print("Writer Agent - Structure Validation Demo")
    print("=" * 80)
    print()
    
    writer = WriterAgent()
    
    # Good content example
    good_content = """
This is a well-structured opening paragraph with sufficient length to engage readers and provide context for the article that follows with valuable insights.

This is the second paragraph that develops the main ideas further.

Here we continue with additional supporting information and details.

The fourth paragraph adds more depth to the discussion.

Finally, we conclude with a strong closing paragraph that ties everything together.
    """.strip()
    
    print("Validating Content Structure:")
    print("-" * 80)
    
    validation = writer.validate_content_structure(good_content)
    
    print("Validation Results:")
    for check, passed in validation.items():
        status = "✓ Pass" if passed else "✗ Fail"
        print(f"  {check.replace('_', ' ').title()}: {status}")
    print()
    
    all_passed = all(validation.values())
    print(f"Overall: {'✓ Content is well-structured' if all_passed else '⚠ Content needs improvement'}")
    print()


def demo_seo_scoring():
    """Demonstrate SEO scoring calculation."""
    print("=" * 80)
    print("Writer Agent - SEO Scoring Demo")
    print("=" * 80)
    print()
    
    writer = WriterAgent()
    
    # Perfect scenario
    print("Scenario 1: Optimal Content")
    print("-" * 80)
    score1 = writer._calculate_seo_score(
        keyword_densities={"AI": 0.02, "technology": 0.02, "innovation": 0.02},
        structure_validation={
            "has_paragraphs": True,
            "has_sufficient_length": True,
            "has_opening": True,
            "has_sections": True
        },
        word_count=1000
    )
    print(f"SEO Score: {score1}/100 ✓ Excellent")
    print()
    
    # Moderate scenario
    print("Scenario 2: Good Content")
    print("-" * 80)
    score2 = writer._calculate_seo_score(
        keyword_densities={"AI": 0.015, "technology": 0.01},
        structure_validation={
            "has_paragraphs": True,
            "has_sufficient_length": True,
            "has_opening": False,
            "has_sections": True
        },
        word_count=850
    )
    print(f"SEO Score: {score2}/100 ⚠ Needs Improvement")
    print()
    
    # Poor scenario
    print("Scenario 3: Needs Work")
    print("-" * 80)
    score3 = writer._calculate_seo_score(
        keyword_densities={},
        structure_validation={
            "has_paragraphs": False,
            "has_sufficient_length": False,
            "has_opening": False,
            "has_sections": False
        },
        word_count=200
    )
    print(f"SEO Score: {score3}/100 ✗ Poor")
    print()


def main():
    """Run all demos."""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "WRITER AGENT DEMONSTRATION" + " " * 32 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Run demos
    demo_basic_usage()
    demo_keyword_density()
    demo_structure_validation()
    demo_seo_scoring()
    
    print("=" * 80)
    print("Demo Complete!")
    print("=" * 80)
    print()
    print("For full documentation, see: docs/writer_agent.md")
    print("To run tests: python -m unittest tests.test_writer_agent -v")
    print()


if __name__ == "__main__":
    main()
