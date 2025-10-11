#!/usr/bin/env python3
"""
Example script demonstrating the Editor Agent integration.

This script shows how to use the Editor Agent in the content generation pipeline.
"""
import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def example_basic_editing():
    """Basic example of using the Editor Agent."""
    from agents.editor_agent import EditorAgent
    
    print("=" * 60)
    print("BASIC EDITOR AGENT EXAMPLE")
    print("=" * 60)
    print()
    
    # Initialize the editor
    editor = EditorAgent()
    
    # Sample article (simulating output from Writer Agent)
    article_data = {
        "title": "The AI Revolution",
        "subtitle": "How artificial intelligence is transforming content creation",
        "content": """
        Artificial intelligence is rapidly changing the landscape of content creation.
        From automated writing to intelligent editing, AI tools are becoming 
        indispensable for modern content creators.
        
        The impact of AI extends beyond simple automation. These systems can now
        understand context, maintain tone consistency, and even optimize content
        for search engines. This revolution is making high-quality content creation
        accessible to more people than ever before.
        
        As we look to the future, the integration of AI in content workflows will
        only deepen, offering new possibilities for creativity and efficiency.
        """,
        "tags": ["AI", "technology", "content"]
    }
    
    print("Original Article:")
    print(f"  Title: {article_data['title']}")
    print(f"  Tags: {', '.join(article_data['tags'])}")
    print()
    
    # Edit and optimize the article
    print("Editing article...")
    result = editor.edit_article(article_data)
    
    # Display results
    edited = result["edited_article"]
    print("\nEdited Article:")
    print(f"  Title: {edited['title']}")
    print(f"  Meta Description: {edited['meta_description']}")
    print(f"  Tags: {', '.join(edited['tags'])}")
    print()
    
    # Display quality metrics
    metrics = result["quality_metrics"]
    print(f"Quality Score: {metrics['overall_score']}/10")
    print(f"SEO Score: {result['seo_report']['overall_seo_score']}/10")
    print()
    
    # Display improvements
    improvements = result["improvements_made"]
    print("Improvements Made:")
    for key, value in improvements.items():
        print(f"  - {key.replace('_', ' ').title()}: {'Yes' if value else 'No'}")
    print()


def example_with_writer_integration():
    """Example integrating Writer Agent with Editor Agent."""
    print("=" * 60)
    print("WRITER + EDITOR INTEGRATION EXAMPLE")
    print("=" * 60)
    print()
    
    # This would normally use the actual TextGenerator
    # For demo purposes, we'll simulate the writer output
    simulated_writer_output = {
        "title": "Understanding Machine Learning in 2024",
        "subtitle": "A comprehensive guide to modern ML techniques",
        "content": """
        Machine learning has evolved significantly in recent years. What once
        required extensive expertise is now accessible through user-friendly
        frameworks and tools.
        
        Today's ML practitioners have access to powerful libraries like TensorFlow
        and PyTorch, making it easier to build and deploy sophisticated models.
        The democratization of these tools has led to an explosion of innovation
        across industries.
        
        As we move forward, understanding the fundamentals of machine learning
        becomes increasingly important for anyone working in technology.
        """,
        "tags": ["machine learning", "AI", "technology"],
        "word_count": 95,
        "ai_generated": True
    }
    
    print("Step 1: Writer Agent generates draft")
    print(f"  Generated: {simulated_writer_output['title']}")
    print(f"  Word count: {simulated_writer_output['word_count']}")
    print()
    
    # Edit the draft
    from agents.editor_agent import EditorAgent
    editor = EditorAgent()
    
    print("Step 2: Editor Agent refines content")
    result = editor.edit_article(simulated_writer_output)
    
    edited = result["edited_article"]
    print(f"  Optimized title: {edited['title']}")
    print(f"  Added meta description: {edited['meta_description'][:60]}...")
    print(f"  Optimized tags: {', '.join(edited['tags'])}")
    print()
    
    print("Step 3: Ready for Publisher")
    print("  Article is now optimized and ready for publication")
    print()


def example_individual_checks():
    """Example using individual Editor Agent functions."""
    from agents.editor_agent import EditorAgent
    
    print("=" * 60)
    print("INDIVIDUAL CHECK FUNCTIONS EXAMPLE")
    print("=" * 60)
    print()
    
    editor = EditorAgent()
    
    # Sample content
    title = "The Future of Automation"
    content = """
    Automation is transforming how we work and live. From smart homes to
    autonomous vehicles, automated systems are becoming increasingly prevalent
    in our daily lives.
    """
    
    print("Running individual checks on sample content...")
    print()
    
    # Grammar check
    print("1. Grammar Check:")
    grammar_result = editor.check_grammar_and_spelling(content)
    print(f"   Errors found: {grammar_result['has_errors']}")
    if grammar_result['suggestions']:
        print(f"   Suggestions: {grammar_result['suggestions'][0]}")
    print()
    
    # SEO keyword optimization
    print("2. SEO Keywords:")
    keywords = editor.optimize_seo_keywords(title, content)
    print(f"   Primary: {', '.join(keywords['primary_keywords'][:3])}")
    print(f"   Long-tail: {keywords['long_tail_keywords'][0] if keywords['long_tail_keywords'] else 'None'}")
    print()
    
    # Meta title refinement
    print("3. Title Optimization:")
    title_result = editor.refine_meta_title(title, content[:100])
    print(f"   Original: {title_result['original_title']}")
    print(f"   Optimized: {title_result['optimized_title']}")
    print(f"   SEO Score: {title_result['seo_score']}/10")
    print()


def example_full_summary_report():
    """Example showing the detailed summary report."""
    from agents.editor_agent import EditorAgent
    
    print("=" * 60)
    print("DETAILED SUMMARY REPORT EXAMPLE")
    print("=" * 60)
    print()
    
    editor = EditorAgent()
    
    article_data = {
        "title": "Cloud Computing Trends",
        "subtitle": "Exploring the future of cloud infrastructure",
        "content": """
        Cloud computing continues to evolve at a rapid pace. Organizations of all
        sizes are embracing cloud-native architectures to improve scalability and
        reduce operational costs.
        
        The shift to cloud has been accelerated by advancements in containerization,
        serverless computing, and edge computing. These technologies are reshaping
        how applications are built and deployed.
        
        Looking ahead, we can expect continued innovation in areas like multi-cloud
        strategies, cloud security, and sustainable computing practices.
        """,
        "tags": ["cloud", "technology", "infrastructure"]
    }
    
    print("Editing article and generating detailed report...")
    print()
    
    result = editor.edit_article(article_data)
    
    # Get and display the summary report
    summary = editor.get_editing_summary(result)
    print(summary)
    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "EDITOR AGENT INTEGRATION EXAMPLES" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # Example 1: Basic editing
        example_basic_editing()
        input("Press Enter to continue to next example...")
        print("\n")
        
        # Example 2: Integration with Writer
        example_with_writer_integration()
        input("Press Enter to continue to next example...")
        print("\n")
        
        # Example 3: Individual checks
        example_individual_checks()
        input("Press Enter to continue to next example...")
        print("\n")
        
        # Example 4: Full summary report
        example_full_summary_report()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print()
        print("For more information, see docs/editor_agent.md")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nNote: Examples require OpenAI API key in environment variables")
        print("Set OPENAI_API_KEY and other required variables in .env file")


if __name__ == "__main__":
    main()
