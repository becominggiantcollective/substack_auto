"""
Integration example for Visual Director Agent.

This example demonstrates how to integrate the Visual Director Agent
into your content generation workflow.
"""
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.visual_director_agent import VisualDirectorAgent
from content_generators.text_generator import TextGenerator


def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("Basic Visual Director Agent Usage")
    print("=" * 60)
    
    # Initialize the Visual Director Agent
    visual_director = VisualDirectorAgent()
    
    # Sample article data
    title = "The Future of Artificial Intelligence in Healthcare"
    content = """
    Artificial intelligence is revolutionizing healthcare delivery, from diagnostic
    accuracy to personalized treatment plans. Machine learning algorithms analyze
    vast amounts of patient data to identify patterns and predict outcomes with
    unprecedented precision. As we move forward, AI-powered tools will become
    integral to medical decision-making, improving patient care and reducing costs.
    """
    tags = ["AI", "healthcare", "technology", "innovation"]
    
    print("\nGenerating SEO-optimized image...")
    print(f"Title: {title}")
    print(f"Tags: {', '.join(tags)}")
    
    # Generate SEO-optimized image with complete metadata
    result = visual_director.generate_seo_optimized_image(
        title=title,
        content=content,
        tags=tags
    )
    
    # Display results
    print("\n✅ Image Generated Successfully!")
    print("-" * 60)
    print(f"📁 Image Path: {result['image_path']}")
    print(f"📝 Filename: {result['filename']}")
    print(f"🏷️  Alt Text: {result['alt_text']}")
    print(f"💬 Caption: {result['caption']}")
    print(f"🔑 Keywords: {', '.join(result['keywords'])}")
    print(f"🎯 Theme: {result['theme']}")
    print(f"🎨 Mood: {result['mood']}")
    print("-" * 60)
    
    return result


def example_with_post_data():
    """Example using post data structure."""
    print("\n" + "=" * 60)
    print("Integration with Post Data")
    print("=" * 60)
    
    visual_director = VisualDirectorAgent()
    
    # Post data from content generator
    post_data = {
        "title": "Machine Learning: A Beginner's Guide",
        "content": """
        Machine learning is a subset of artificial intelligence that enables
        systems to learn and improve from experience. This guide covers the
        fundamentals of ML algorithms, training processes, and real-world
        applications. Whether you're new to tech or looking to expand your
        knowledge, understanding ML is essential in today's digital landscape.
        """,
        "tags": ["machine learning", "AI", "tutorial", "beginners"]
    }
    
    print("\nGenerating featured image with SEO optimization...")
    
    # Generate featured image with SEO
    result = visual_director.generate_featured_image_with_seo(post_data)
    
    # Display results
    print("\n✅ Featured Image Generated!")
    print("-" * 60)
    print(f"📁 Image: {result['image_path']}")
    print(f"📁 Thumbnail: {result['thumbnail_path']}")
    print(f"🏷️  Alt Text: {result['alt_text']}")
    print(f"💬 Caption: {result['caption']}")
    print(f"🔑 SEO Keywords: {', '.join(result['keywords'][:3])}")
    print("-" * 60)
    
    return result


def example_seo_analysis_only():
    """Example of SEO analysis without image generation."""
    print("\n" + "=" * 60)
    print("SEO Analysis Only (No Image Generation)")
    print("=" * 60)
    
    visual_director = VisualDirectorAgent()
    
    # Analyze content for SEO
    metadata = visual_director.analyze_seo_metadata(
        title="Blockchain Technology Explained",
        content="""
        Blockchain is a distributed ledger technology that ensures secure and
        transparent transactions. It's the foundation of cryptocurrencies but
        has applications far beyond digital currency, including supply chain
        management, healthcare records, and voting systems.
        """,
        tags=["blockchain", "technology", "cryptocurrency"]
    )
    
    print("\n📊 SEO Analysis Results:")
    print("-" * 60)
    print(f"Title: {metadata['title']}")
    print(f"Keywords: {', '.join(metadata['keywords'])}")
    print(f"Theme: {metadata['theme']}")
    print(f"Mood: {metadata['mood']}")
    print(f"Style: {metadata['style']}")
    print("-" * 60)
    
    return metadata


def example_custom_workflow():
    """Example of a custom workflow with all components."""
    print("\n" + "=" * 60)
    print("Custom Workflow: Generate Complete Content with SEO")
    print("=" * 60)
    
    # Initialize generators
    text_gen = TextGenerator()
    visual_director = VisualDirectorAgent()
    
    print("\n1️⃣  Generating article content...")
    # Generate complete post
    post_data = text_gen.create_complete_post()
    print(f"   ✅ Generated: {post_data['title']}")
    print(f"   📏 Word Count: {post_data['word_count']}")
    
    print("\n2️⃣  Analyzing SEO metadata...")
    # Analyze SEO
    seo_metadata = visual_director.analyze_seo_metadata(
        title=post_data['title'],
        content=post_data['content'],
        tags=post_data.get('tags', [])
    )
    print(f"   ✅ Extracted {len(seo_metadata['keywords'])} keywords")
    
    print("\n3️⃣  Generating SEO-optimized filename...")
    # Generate filename
    filename = visual_director.generate_seo_friendly_filename(
        title=post_data['title'],
        keywords=seo_metadata['keywords']
    )
    print(f"   ✅ Filename: {filename}.png")
    
    print("\n4️⃣  Generating alt text and caption...")
    # Generate alt text and caption
    alt_text = visual_director.generate_alt_text(
        title=post_data['title'],
        seo_metadata=seo_metadata
    )
    caption = visual_director.generate_caption(
        title=post_data['title'],
        seo_metadata=seo_metadata
    )
    print(f"   ✅ Alt Text: {alt_text[:60]}...")
    print(f"   ✅ Caption: {caption[:60]}...")
    
    print("\n5️⃣  Generating final image...")
    # Generate image
    image_result = visual_director.generate_featured_image_with_seo(post_data)
    print(f"   ✅ Image: {image_result['image_path']}")
    
    # Compile complete package
    complete_package = {
        "post": post_data,
        "media": {
            "image": image_result['image_path'],
            "thumbnail": image_result['thumbnail_path'],
            "alt_text": image_result['alt_text'],
            "caption": image_result['caption']
        },
        "seo": {
            "keywords": seo_metadata['keywords'],
            "theme": seo_metadata['theme'],
            "metadata": seo_metadata
        }
    }
    
    print("\n✅ Complete Content Package Ready!")
    print("-" * 60)
    print(f"📝 Title: {post_data['title']}")
    print(f"📏 Words: {post_data['word_count']}")
    print(f"🖼️  Image: {image_result['filename']}")
    print(f"🔑 Keywords: {', '.join(seo_metadata['keywords'][:5])}")
    print("-" * 60)
    
    return complete_package


def example_batch_processing():
    """Example of batch processing multiple articles."""
    print("\n" + "=" * 60)
    print("Batch Processing Multiple Articles")
    print("=" * 60)
    
    visual_director = VisualDirectorAgent()
    
    # Sample articles
    articles = [
        {
            "title": "5G Technology: The Next Generation",
            "content": "5G networks promise faster speeds and lower latency...",
            "tags": ["5G", "technology", "networking"]
        },
        {
            "title": "Sustainable Energy Solutions for 2024",
            "content": "Renewable energy sources are becoming more efficient...",
            "tags": ["sustainability", "energy", "climate"]
        },
        {
            "title": "Cybersecurity Best Practices",
            "content": "Protecting your digital assets requires vigilance...",
            "tags": ["cybersecurity", "security", "technology"]
        }
    ]
    
    results = []
    
    for i, article in enumerate(articles, 1):
        print(f"\n📄 Processing Article {i}/{len(articles)}: {article['title']}")
        
        # Generate SEO-optimized image
        result = visual_director.generate_seo_optimized_image(
            title=article['title'],
            content=article['content'],
            tags=article['tags']
        )
        
        results.append({
            "article": article,
            "image_result": result
        })
        
        print(f"   ✅ Image: {result['filename']}")
        print(f"   🔑 Keywords: {', '.join(result['keywords'][:3])}")
    
    print("\n" + "=" * 60)
    print(f"✅ Batch Processing Complete! Generated {len(results)} images")
    print("=" * 60)
    
    return results


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Visual Director Agent Examples" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        # Run examples
        example_basic_usage()
        example_with_post_data()
        example_seo_analysis_only()
        example_custom_workflow()
        example_batch_processing()
        
        print("\n" + "=" * 60)
        print("✅ All Examples Completed Successfully!")
        print("=" * 60)
        print("\n💡 Integration Tips:")
        print("   • Use generate_featured_image_with_seo() for standard workflow")
        print("   • Analyze SEO first to preview keywords before generation")
        print("   • Generate filenames separately for custom naming schemes")
        print("   • Batch process for efficiency with multiple articles")
        print("\n📖 See docs/visual_director_agent.md for more details")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Note: Examples require valid OPENAI_API_KEY to run")
        print("Set environment variables and try again.")


if __name__ == "__main__":
    main()
