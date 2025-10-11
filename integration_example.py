"""
Integration example: Using Research Agent with Content Generators

This script demonstrates how to integrate the Research Agent with
the existing content generation pipeline for SEO-optimized posts.
"""
import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.research_agent import ResearchAgent
from content_generators.text_generator import TextGenerator
from content_generators.image_generator import ImageGenerator


def create_seo_optimized_post():
    """
    Create a blog post optimized for SEO using the Research Agent.
    
    This workflow demonstrates:
    1. Using Research Agent to find trending topics
    2. Getting SEO keywords for the topic
    3. Generating content with the Writer Agent
    4. Creating images with the Image Generator
    5. Adding SEO metadata to the final post
    """
    print("=" * 70)
    print("SEO-Optimized Content Generation with Research Agent")
    print("=" * 70)
    print()
    
    # Initialize agents
    print("🔧 Initializing agents...")
    research_agent = ResearchAgent()
    text_generator = TextGenerator()
    image_generator = ImageGenerator()
    print("✅ Agents initialized\n")
    
    # Step 1: Research trending topics
    print("📊 Step 1: Discovering trending topics...")
    try:
        # Get the top trending topic with SEO analysis
        top_topic = research_agent.get_top_topic_with_seo()
        
        print(f"✅ Selected topic: {top_topic['topic']}")
        print(f"   Trend score: {top_topic['trend_score']}/10")
        print(f"   Primary keywords: {', '.join(top_topic['seo_keywords']['primary'][:3])}")
        print()
    except Exception as e:
        print(f"⚠️  Using fallback topic due to: {e}")
        # Fallback to manual topic
        topic_title = text_generator.generate_topic()
        print(f"✅ Generated topic: {topic_title}\n")
        
        # Analyze SEO for the fallback topic
        top_topic = {
            'topic': topic_title,
            'trend_score': 7,
            'seo_keywords': research_agent.analyze_seo_keywords(topic_title)
        }
    
    # Step 2: Generate content
    print("📝 Step 2: Generating blog post content...")
    post_data = text_generator.generate_blog_post(top_topic['topic'])
    print(f"✅ Generated {post_data['word_count']} words")
    print(f"   Title: {post_data['title']}")
    print(f"   Subtitle: {post_data['subtitle'][:80]}...")
    print()
    
    # Step 3: Generate featured image
    print("🖼️  Step 3: Generating featured image...")
    image_result = image_generator.generate_featured_image(post_data)
    if 'image_path' in image_result:
        print(f"✅ Image generated: {image_result['image_path']}")
    else:
        print("⚠️  Image generation skipped (API key required)")
    print()
    
    # Step 4: Add SEO metadata
    print("🔍 Step 4: Adding SEO metadata...")
    seo_keywords = top_topic.get('seo_keywords', {})
    
    # Extract keywords from the complex structure
    if isinstance(seo_keywords, dict):
        primary_keywords = seo_keywords.get('primary', [])
        secondary_keywords = seo_keywords.get('secondary', [])
        long_tail_keywords = seo_keywords.get('long_tail', [])
    else:
        # Handle if it's already in the analyzed format
        primary_keywords = seo_keywords.get('primary_keywords', [])
        secondary_keywords = seo_keywords.get('secondary_keywords', [])
        long_tail_keywords = seo_keywords.get('long_tail_keywords', [])
    
    # Create complete post with SEO metadata
    complete_post = {
        "post_data": post_data,
        "image_result": image_result,
        "seo_metadata": {
            "primary_keywords": primary_keywords,
            "secondary_keywords": secondary_keywords,
            "long_tail_keywords": long_tail_keywords,
            "search_intent": top_topic.get('search_intent', 'informational'),
            "content_recommendations": top_topic.get('content_recommendations', ''),
            "trend_score": top_topic.get('trend_score', 0)
        },
        "research_data": {
            "topic": top_topic['topic'],
            "rationale": top_topic.get('rationale', ''),
            "discovered_at": datetime.now().isoformat()
        },
        "generation_timestamp": datetime.now().isoformat(),
        "ai_generated": True,
        "seo_optimized": True
    }
    
    print(f"✅ SEO metadata added")
    print(f"   Primary keywords: {len(primary_keywords)}")
    print(f"   Secondary keywords: {len(secondary_keywords)}")
    print(f"   Long-tail keywords: {len(long_tail_keywords)}")
    print()
    
    # Step 5: Save the complete post
    print("💾 Step 5: Saving SEO-optimized post...")
    output_dir = "generated_content"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"seo_optimized_post_{timestamp}.json")
    
    with open(output_file, 'w') as f:
        json.dump(complete_post, f, indent=2, default=str)
    
    print(f"✅ Post saved to: {output_file}")
    print()
    
    # Display summary
    print("=" * 70)
    print("✅ SEO-Optimized Post Generated Successfully!")
    print("=" * 70)
    print()
    print("📊 Post Summary:")
    print(f"   Topic: {complete_post['post_data']['title']}")
    print(f"   Word Count: {complete_post['post_data']['word_count']}")
    print(f"   Trend Score: {complete_post['seo_metadata']['trend_score']}/10")
    print(f"   Search Intent: {complete_post['seo_metadata']['search_intent']}")
    print(f"   SEO Keywords: {len(primary_keywords) + len(secondary_keywords) + len(long_tail_keywords)}")
    print()
    print("📝 Top SEO Keywords:")
    for kw in primary_keywords[:5]:
        print(f"   • {kw}")
    print()
    print("💡 Content Recommendations:")
    print(f"   {complete_post['seo_metadata']['content_recommendations'][:200]}")
    print()
    
    return complete_post


def batch_research_for_week():
    """
    Generate a week's worth of research data for content planning.
    """
    print("=" * 70)
    print("Weekly Content Research & Planning")
    print("=" * 70)
    print()
    
    research_agent = ResearchAgent()
    
    print("📊 Generating research for 7 blog posts (one per day)...")
    print()
    
    try:
        # Generate research summary for multiple topics
        summary = research_agent.generate_research_summary(topic_count=7)
        
        print(f"✅ Research completed: {summary['topic_count']} topics discovered")
        print()
        
        # Sort by trend score
        topics = sorted(
            summary['research_results'], 
            key=lambda x: x['trend_score'], 
            reverse=True
        )
        
        print("📅 Weekly Content Plan:")
        print()
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i, (day, topic) in enumerate(zip(days, topics), 1):
            print(f"{day}:")
            print(f"   Topic: {topic['topic']}")
            print(f"   Trend Score: {topic['trend_score']}/10")
            print(f"   Primary Keywords: {', '.join(topic['seo_keywords']['primary'][:3])}")
            print(f"   Search Intent: {topic['search_intent']}")
            print()
        
        # Save weekly plan
        output_dir = "generated_content"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"weekly_content_plan_{timestamp}.json")
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"💾 Weekly plan saved to: {output_file}")
        print()
        
    except Exception as e:
        print(f"⚠️  Error generating weekly research: {e}")
        print()


def main():
    """Run the integration examples."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  Research Agent Integration with Content Generators             ║")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("\n")
    
    print("This example demonstrates integrating the Research Agent with")
    print("existing content generators for SEO-optimized posts.")
    print()
    
    # Example 1: Single SEO-optimized post
    try:
        create_seo_optimized_post()
    except Exception as e:
        print(f"⚠️  Example 1 failed: {e}")
        print()
    
    input("Press Enter to continue to weekly planning example...")
    print()
    
    # Example 2: Weekly content planning
    try:
        batch_research_for_week()
    except Exception as e:
        print(f"⚠️  Example 2 failed: {e}")
        print()
    
    print("=" * 70)
    print("✅ Integration Examples Complete!")
    print("=" * 70)
    print()
    print("📚 For more information:")
    print("   - Research Agent docs: docs/research_agent.md")
    print("   - Research Agent examples: python examples_research_agent.py")
    print("   - Run tests: python -m unittest tests.test_research_agent")
    print()


if __name__ == "__main__":
    main()
