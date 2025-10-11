#!/usr/bin/env python3
"""
Example script demonstrating the Writer Agent functionality.

This script shows how to use the WriterAgent to generate SEO-optimized articles
with research summaries and keyword integration.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.writer_agent import WriterAgent


def main():
    """Run Writer Agent examples."""
    print("=" * 80)
    print("Writer Agent Example")
    print("=" * 80)
    print()
    
    # Initialize the Writer Agent
    print("🤖 Initializing Writer Agent...")
    writer = WriterAgent()
    print("✅ Writer Agent initialized")
    print()
    
    # Example 1: Basic keyword density calculation
    print("-" * 80)
    print("Example 1: Keyword Density Calculation")
    print("-" * 80)
    
    sample_content = """
    Artificial intelligence is transforming healthcare in unprecedented ways.
    AI systems are enabling faster diagnoses and personalized treatments.
    The integration of AI in medical practice represents a paradigm shift.
    Healthcare providers are increasingly adopting AI technologies.
    """
    
    keyword = "AI"
    density = writer.calculate_keyword_density(sample_content, keyword)
    
    print(f"Sample content: {sample_content.strip()[:100]}...")
    print(f"Keyword: '{keyword}'")
    print(f"Keyword density: {density:.2%}")
    print()
    
    # Example 2: Demonstrate the expected input/output format
    print("-" * 80)
    print("Example 2: Writer Agent Input/Output Format")
    print("-" * 80)
    print()
    
    print("📝 Expected Input Format:")
    example_input = {
        "topic": "The Future of Artificial Intelligence in Healthcare",
        "keywords": [
            "AI healthcare",
            "artificial intelligence",
            "medical AI",
            "healthcare technology",
            "diagnosis"
        ],
        "research_summary": """
        Recent studies show that AI diagnostic tools achieve 95% accuracy in 
        detecting certain cancers. Healthcare providers are increasingly adopting 
        AI systems for patient triage, treatment planning, and drug discovery.
        The global AI healthcare market is expected to reach $188 billion by 2030.
        """
    }
    
    print(f"  Topic: {example_input['topic']}")
    print(f"  Keywords: {', '.join(example_input['keywords'])}")
    print(f"  Research Summary: {example_input['research_summary'].strip()[:150]}...")
    print()
    
    print("📤 Expected Output Format:")
    print("""
    {
        "title": "The Future of Artificial Intelligence in Healthcare",
        "content": "## Introduction\\n\\n[Article content 800-1200 words]...",
        "meta_title": "AI Healthcare: Transform Your Medical Practice",
        "meta_description": "Discover how AI is revolutionizing healthcare...",
        "tags": ["AI", "healthcare", "medical technology", "diagnosis", ...],
        "word_count": 1050,
        "keyword_density": 0.021,
        "keywords_used": ["AI healthcare", "artificial intelligence", ...],
        "seo_optimized": true,
        "ai_generated": true
    }
    """)
    print()
    
    # Example 3: Show configuration options
    print("-" * 80)
    print("Example 3: Configuration Options")
    print("-" * 80)
    print()
    print("The Writer Agent respects these environment variables:")
    print("  • CONTENT_TONE: e.g., 'professional and engaging'")
    print("  • TARGET_AUDIENCE: e.g., 'tech-savvy professionals'")
    print("  • CONTENT_STYLE: e.g., 'informative and thought-provoking'")
    print("  • CUSTOM_INSTRUCTIONS: e.g., 'Include real-world examples'")
    print()
    print("Set these in your .env file to customize content generation.")
    print()
    
    # Example 4: Integration with other agents
    print("-" * 80)
    print("Example 4: Integration with Other Agents")
    print("-" * 80)
    print()
    print("Writer Agent Pipeline:")
    print()
    print("  Research Agent → Writer Agent → Editor Agent → SEO Specialist → Publisher")
    print()
    print("  1️⃣  Research Agent provides:")
    print("     - Topic suggestion")
    print("     - Keyword list")
    print("     - Research summary")
    print()
    print("  2️⃣  Writer Agent generates:")
    print("     - SEO-optimized article (800-1200 words)")
    print("     - Meta title and description")
    print("     - Suggested tags")
    print()
    print("  3️⃣  Editor Agent (future) will:")
    print("     - Review and refine content")
    print("     - Check grammar and style")
    print("     - Ensure quality standards")
    print()
    print("  4️⃣  SEO Specialist Agent (future) will:")
    print("     - Optimize keyword placement")
    print("     - Enhance meta descriptions")
    print("     - Validate SEO best practices")
    print()
    
    # Summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print("✅ Writer Agent Features:")
    print("   • SEO-optimized content generation (800-1200 words)")
    print("   • Keyword density management (~2% target)")
    print("   • Meta title and description generation")
    print("   • Tag suggestions for content discovery")
    print("   • Research summary integration")
    print("   • Configurable tone, style, and audience")
    print("   • Compatible with existing and future agents")
    print()
    print("📚 For detailed documentation, see: docs/writer_agent.md")
    print()
    print("⚠️  Note: To generate actual content, you need a valid OPENAI_API_KEY")
    print("   in your .env file. This example demonstrates the interface only.")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
