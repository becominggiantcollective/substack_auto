#!/usr/bin/env python3
"""
Example script demonstrating the Visual Director Agent.

This script shows how to use the Visual Director Agent to generate
SEO-optimized media for blog posts.
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def example_basic_usage():
    """Basic usage example: Generate a single SEO-optimized image."""
    from agents.visual_director_agent import VisualDirectorAgent
    
    print("=" * 60)
    print("Example 1: Generate Single SEO-Optimized Image")
    print("=" * 60)
    
    # Initialize agent
    agent = VisualDirectorAgent()
    
    # Example article data
    title = "The Future of Artificial Intelligence in Healthcare"
    content = """
    Artificial intelligence is revolutionizing healthcare delivery and patient outcomes.
    From diagnostic imaging to personalized treatment plans, AI technologies are enabling
    medical professionals to provide more accurate, efficient, and cost-effective care.
    
    Machine learning algorithms can now detect diseases earlier, predict patient outcomes,
    and even suggest optimal treatment protocols. As these technologies continue to advance,
    we're seeing unprecedented improvements in healthcare accessibility and quality.
    """
    tags = ["AI", "healthcare", "machine learning", "medical technology"]
    
    print("\nArticle Information:")
    print(f"  Title: {title}")
    print(f"  Tags: {', '.join(tags)}")
    print(f"  Content Length: {len(content)} characters")
    print("\nAnalyzing content and generating SEO-optimized image...")
    print("(Note: This example uses mock data when API keys are not available)")
    
    # Note: In real usage with valid API keys, this would generate an actual image
    # For demo purposes without API keys, this will show the structure
    try:
        result = agent.generate_seo_optimized_image(
            title=title,
            content=content,
            tags=tags,
            media_type="featured"
        )
        
        if result:
            print("\n✓ Image Generated Successfully!")
            print(f"  Filename: {result['filename']}")
            print(f"  Alt Text: {result['alt_text']}")
            print(f"  Caption: {result['caption']}")
            print(f"  SEO Focus: {result['seo_metadata']['focus_keyword']}")
            print(f"  Keywords: {', '.join(result['seo_metadata']['keywords'])}")
    except Exception as e:
        print(f"\n✗ Error (expected without API key): {e}")
        print("\nShowing example structure:")
        example_result = {
            "filename": "featured-ai-healthcare-future-artificial-intelligence.png",
            "alt_text": "Featured image about AI healthcare - transforming medical technology",
            "caption": "Explore how AI is revolutionizing healthcare delivery and patient outcomes.",
            "seo_metadata": {
                "focus_keyword": "AI healthcare",
                "keywords": ["artificial intelligence", "healthcare", "medical technology"],
                "visual_themes": ["medical", "futuristic", "technology"],
                "target_emotion": "hopeful"
            }
        }
        print(f"  Filename: {example_result['filename']}")
        print(f"  Alt Text: {example_result['alt_text']}")
        print(f"  Caption: {example_result['caption']}")
        print(f"  SEO Focus: {example_result['seo_metadata']['focus_keyword']}")


def example_image_set():
    """Example: Generate complete image set for an article."""
    from agents.visual_director_agent import VisualDirectorAgent
    
    print("\n" + "=" * 60)
    print("Example 2: Generate Complete Image Set")
    print("=" * 60)
    
    agent = VisualDirectorAgent()
    
    title = "10 Python Tips Every Developer Should Know"
    content = """
    Python continues to be one of the most popular programming languages.
    Whether you're a beginner or experienced developer, these essential tips
    will help you write cleaner, more efficient code and boost your productivity.
    """
    tags = ["Python", "programming", "development", "coding tips"]
    
    print("\nGenerating featured image, thumbnail, and social media image...")
    print("(Note: This is a demonstration - actual API calls require valid keys)")
    
    try:
        image_set = agent.generate_image_set(title, content, tags)
        
        if image_set["success"]:
            print(f"\n✓ Generated {image_set['images_generated']} images!")
            for media_type, image_data in image_set["images"].items():
                print(f"\n  {media_type.upper()} Image:")
                print(f"    Filename: {image_data['filename']}")
                print(f"    Alt Text: {image_data['alt_text'][:60]}...")
    except Exception as e:
        print(f"\n✗ Error (expected without API key): {e}")
        print("\nExample output structure:")
        print("  FEATURED Image:")
        print("    Filename: featured-python-tips-every-developer-should-know.png")
        print("    Alt Text: Featured image about Python tips - coding best practices")
        print("\n  THUMBNAIL Image:")
        print("    Filename: thumbnail-python-tips-every-developer-should-know.png")
        print("    Alt Text: Thumbnail showing Python tips - developer guide")
        print("\n  SOCIAL Image:")
        print("    Filename: social-python-tips-every-developer-should-know.png")
        print("    Alt Text: Social media image for Python tips - programming guide")


def example_seo_analysis():
    """Example: Perform SEO analysis only."""
    from agents.visual_director_agent import VisualDirectorAgent
    
    print("\n" + "=" * 60)
    print("Example 3: SEO Content Analysis")
    print("=" * 60)
    
    agent = VisualDirectorAgent()
    
    title = "Understanding Blockchain Technology"
    content = """
    Blockchain technology is transforming how we think about data security and
    decentralized systems. This revolutionary approach to data management has
    implications far beyond cryptocurrency, affecting industries from finance
    to healthcare to supply chain management.
    """
    tags = ["blockchain", "technology", "cryptocurrency", "security"]
    
    print("\nAnalyzing content for SEO optimization...")
    
    try:
        analysis = agent.analyze_content_for_seo(title, content, tags)
        
        print("\n✓ SEO Analysis Complete!")
        print(f"  Focus Keyword: {analysis['seo_focus']}")
        print(f"  Primary Keywords: {', '.join(analysis['primary_keywords'])}")
        print(f"  Visual Themes: {', '.join(analysis['visual_themes'])}")
        print(f"  Target Emotion: {analysis['target_emotion']}")
        print(f"  Key Concepts: {', '.join(analysis['key_concepts'])}")
    except Exception as e:
        print(f"\n✗ Error (expected without API key): {e}")
        print("\nExample analysis structure:")
        print("  Focus Keyword: blockchain technology")
        print("  Primary Keywords: blockchain, decentralization, security")
        print("  Visual Themes: digital, network, futuristic")
        print("  Target Emotion: curious")
        print("  Key Concepts: distributed ledger, cryptographic security")


def example_seo_best_practices():
    """Show SEO best practices for filenames and alt text."""
    from agents.visual_director_agent import VisualDirectorAgent
    
    print("\n" + "=" * 60)
    print("Example 4: SEO Best Practices")
    print("=" * 60)
    
    agent = VisualDirectorAgent()
    
    # Example filenames
    print("\nSEO-Friendly Filenames:")
    examples = [
        ("Complete Guide to Machine Learning", "machine learning", "featured"),
        ("Quick Python Tutorial for Beginners", "python tutorial", "tutorial"),
        ("Top 10 JavaScript Frameworks in 2024", "javascript frameworks", "social")
    ]
    
    for title, focus, media_type in examples:
        filename = agent.generate_seo_filename(title, focus, media_type)
        print(f"  {filename}")
    
    # Example alt text
    print("\nSEO-Friendly Alt Text:")
    seo_analysis = {
        "primary_keywords": ["web development", "coding", "frontend"],
        "seo_focus": "web development",
        "key_concepts": ["responsive design", "modern web"]
    }
    
    alt_text = agent.generate_alt_text(
        "Modern Web Development Best Practices",
        seo_analysis,
        "featured"
    )
    print(f"  {alt_text}")
    
    print("\nKey SEO Principles:")
    print("  ✓ Use hyphens (not underscores) in filenames")
    print("  ✓ Include focus keyword early in filename")
    print("  ✓ Keep filenames under 60 characters")
    print("  ✓ Write descriptive alt text (under 125 characters)")
    print("  ✓ Incorporate keywords naturally")
    print("  ✓ Make content accessible for screen readers")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Visual Director Agent - Usage Examples")
    print("=" * 60)
    print("\nThis script demonstrates the Visual Director Agent's capabilities")
    print("for generating SEO-optimized media for blog posts.")
    print("\nNote: These examples show the agent's structure and workflow.")
    print("To generate actual images, set your OPENAI_API_KEY environment variable.")
    
    try:
        example_basic_usage()
        example_image_set()
        example_seo_analysis()
        example_seo_best_practices()
        
        print("\n" + "=" * 60)
        print("Examples Complete!")
        print("=" * 60)
        print("\nFor more information, see:")
        print("  - Documentation: docs/visual_director_agent.md")
        print("  - Tests: tests/test_visual_director_agent.py")
        print("  - Source: src/agents/visual_director_agent.py")
        print()
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
