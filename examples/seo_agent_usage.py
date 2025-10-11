#!/usr/bin/env python3
"""
Example usage of the SEO Specialist Agent.

This script demonstrates how to use the SEO Agent to analyze content
and generate actionable SEO recommendations.
"""
import os
import sys
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.seo_agent import SEOAgent


def example_basic_usage():
    """Demonstrate basic SEO analysis."""
    print("=" * 60)
    print("SEO AGENT - BASIC USAGE EXAMPLE")
    print("=" * 60)
    print()
    
    # Initialize the agent
    seo_agent = SEOAgent()
    
    # Sample article
    title = "Artificial Intelligence in Modern Healthcare Systems"
    subtitle = "Exploring how AI technologies are revolutionizing patient care, diagnosis, and treatment in hospitals worldwide"
    content = """
Artificial intelligence is fundamentally transforming healthcare delivery. Machine learning algorithms now assist doctors in diagnosing diseases, planning treatments, and predicting patient outcomes with unprecedented accuracy.

Medical Imaging Analysis

AI-powered imaging tools can detect abnormalities in X-rays, MRIs, and CT scans faster than traditional methods. These systems identify early signs of cancer, heart disease, and neurological conditions. Radiologists use AI as a second opinion to improve diagnostic accuracy.

Personalized Treatment Plans

Healthcare providers leverage AI to create customized treatment strategies. The technology analyzes patient history, genetic data, and current symptoms. This comprehensive approach leads to more effective interventions and better patient outcomes.

Predictive Analytics

Machine learning models predict disease progression and potential complications. Hospitals use these insights to allocate resources efficiently. Early intervention becomes possible when AI identifies high-risk patients before symptoms appear.

Natural Language Processing

NLP systems extract valuable information from clinical notes and research papers. Doctors spend less time on documentation and more time with patients. The technology helps identify relevant treatment options from vast medical literature.

Challenges and Solutions

Privacy concerns require robust security measures. Healthcare organizations must ensure AI systems comply with regulations. Training staff to work alongside AI tools remains essential for successful implementation.

The Future of AI Healthcare

Continued innovation will bring more sophisticated diagnostic tools. Telemedicine platforms will expand access to quality care in remote areas. The synergy between human expertise and artificial intelligence promises improved healthcare for all.
    """
    tags = ["AI", "healthcare", "medical technology", "machine learning", "digital health"]
    
    # Analyze content
    print("Analyzing content...")
    result = seo_agent.analyze_content(
        title=title,
        subtitle=subtitle,
        content=content,
        tags=tags
    )
    
    # Display results
    print()
    print("=" * 60)
    print("SEO ANALYSIS RESULTS")
    print("=" * 60)
    print()
    print(f"📊 Overall SEO Score: {result['seo_score']}/100")
    print(f"📈 Grade: {result['grade']}")
    print()
    
    print("Score Breakdown:")
    print(f"  • Structure:     {result['structure_analysis']['score']:.1f}/100")
    print(f"  • Keywords:      {result['keyword_analysis']['score']:.1f}/100")
    print(f"  • Readability:   {result['readability_analysis']['score']:.1f}/100")
    print(f"  • Metadata:      {result['metadata_analysis']['score']:.1f}/100")
    print(f"  • Semantic:      {result['semantic_analysis']['score']:.1f}/100")
    print()
    
    print("📝 Summary:")
    print(result['summary'])
    print()
    
    # Show top recommendations
    print("=" * 60)
    print("TOP RECOMMENDATIONS")
    print("=" * 60)
    print()
    
    high_priority = [r for r in result['recommendations'] if r['priority'] == 'high']
    medium_priority = [r for r in result['recommendations'] if r['priority'] == 'medium']
    
    if high_priority:
        print("🔴 High Priority:")
        for rec in high_priority:
            print(f"  • [{rec['category']}] {rec['recommendation']}")
        print()
    
    if medium_priority:
        print("🟡 Medium Priority:")
        for rec in medium_priority[:3]:  # Show top 3
            print(f"  • [{rec['category']}] {rec['recommendation']}")
        print()
    
    return result


def example_detailed_analysis():
    """Demonstrate detailed SEO metrics."""
    print("=" * 60)
    print("SEO AGENT - DETAILED ANALYSIS EXAMPLE")
    print("=" * 60)
    print()
    
    seo_agent = SEOAgent()
    
    # Another sample article
    title = "Getting Started with Machine Learning"
    subtitle = "A comprehensive beginner's guide"
    content = """
Machine learning is everywhere. From recommendation systems to self-driving cars, ML powers modern technology. This guide helps you start your journey.

Understanding the basics matters most. Machine learning teaches computers to learn from data. Unlike traditional programming, you don't write explicit rules. The system discovers patterns automatically.

Three main types exist. Supervised learning uses labeled data. Unsupervised learning finds hidden patterns. Reinforcement learning learns through trial and error.

Getting started requires preparation. Learn Python programming first. Understand statistics and linear algebra. Practice with real datasets regularly.
    """
    tags = ["machine learning", "AI", "tutorial"]
    
    result = seo_agent.analyze_content(
        title=title,
        subtitle=subtitle,
        content=content,
        tags=tags
    )
    
    # Show detailed metrics
    print("📊 CONTENT STRUCTURE")
    print("-" * 60)
    structure = result['structure_analysis']
    print(f"Word Count:          {structure['word_count']} (optimal: {structure['word_count_optimal'][0]}-{structure['word_count_optimal'][1]})")
    print(f"Paragraphs:          {structure['paragraph_count']}")
    print(f"Sentences:           {structure['sentence_count']}")
    print(f"Headings:            {structure['heading_count']}")
    print(f"Avg Sentence Length: {structure['avg_sentence_length']:.1f} words")
    print()
    
    print("🔑 KEYWORD ANALYSIS")
    print("-" * 60)
    keywords = result['keyword_analysis']
    print(f"Primary Keyword:     '{keywords['primary_keyword']}'")
    print(f"Keyword Density:     {keywords['keyword_density']:.2f}% (optimal: {keywords['keyword_density_optimal'][0]}-{keywords['keyword_density_optimal'][1]}%)")
    print(f"In Title:            {'✓' if keywords['title_keyword_match'] else '✗'}")
    print(f"Tag Relevance:       {keywords['tag_relevance']:.2%}")
    print()
    print("Top Keywords:")
    for word, count in keywords['top_keywords'][:5]:
        print(f"  • {word}: {count} occurrences")
    print()
    
    print("📖 READABILITY")
    print("-" * 60)
    readability = result['readability_analysis']
    print(f"Flesch Reading Ease: {readability['flesch_reading_ease']:.1f}")
    print(f"Grade Level:         {readability['flesch_kincaid_grade']:.1f}")
    print(f"Reading Level:       {readability['readability_level']}")
    print(f"Avg Sentence Length: {readability['avg_sentence_length']:.1f} words")
    print()
    
    print("🏷️  METADATA")
    print("-" * 60)
    metadata = result['metadata_analysis']
    print(f"Title Length:        {metadata['title_length']} chars (optimal: {metadata['title_optimal_range'][0]}-{metadata['title_optimal_range'][1]})")
    print(f"Subtitle Length:     {metadata['subtitle_length']} chars (optimal: {metadata['subtitle_optimal_range'][0]}-{metadata['subtitle_optimal_range'][1]})")
    print(f"Tag Count:           {metadata['tag_count']} (optimal: {metadata['tag_count_optimal_range'][0]}-{metadata['tag_count_optimal_range'][1]})")
    print(f"Keyword-Rich Title:  {'✓' if metadata['keyword_rich_title'] else '✗'}")
    print()
    
    print("🎯 SEMANTIC ALIGNMENT")
    print("-" * 60)
    semantic = result['semantic_analysis']
    print(f"Title-Content:       {semantic['title_content_alignment']:.1%}")
    print(f"Tag-Content:         {semantic['tag_content_alignment']:.1%}")
    print(f"Topic Distribution:  {semantic['topic_distribution']:.1%}")
    print()


def example_batch_analysis():
    """Demonstrate analyzing multiple articles."""
    print("=" * 60)
    print("SEO AGENT - BATCH ANALYSIS EXAMPLE")
    print("=" * 60)
    print()
    
    seo_agent = SEOAgent()
    
    # Sample articles
    articles = [
        {
            "title": "Python Programming Best Practices",
            "subtitle": "Write clean, maintainable Python code",
            "content": "Python is a powerful programming language. Following best practices helps you write better code. Use meaningful variable names. Write clear comments. Follow PEP 8 style guidelines. Test your code regularly. " * 20,
            "tags": ["python", "programming", "best practices"]
        },
        {
            "title": "Data Science Career Guide",
            "subtitle": "Everything you need to know",
            "content": "Data science is an exciting field. It combines statistics, programming, and domain knowledge. Learn Python and R. Master statistics and machine learning. Build a portfolio of projects. Network with professionals. " * 20,
            "tags": ["data science", "career", "guide"]
        },
        {
            "title": "Web Development Trends",
            "subtitle": "What's new in web development",
            "content": "Web development evolves rapidly. New frameworks and tools emerge constantly. React and Vue remain popular. TypeScript gains adoption. Serverless architectures grow. Progressive web apps improve. " * 20,
            "tags": ["web development", "trends", "technology"]
        }
    ]
    
    print("Analyzing multiple articles...\n")
    
    results = []
    for i, article in enumerate(articles, 1):
        result = seo_agent.analyze_content(
            title=article['title'],
            subtitle=article['subtitle'],
            content=article['content'],
            tags=article['tags']
        )
        
        results.append({
            'title': article['title'],
            'score': result['seo_score'],
            'grade': result['grade'],
            'high_priority_count': len([r for r in result['recommendations'] if r['priority'] == 'high'])
        })
        
        print(f"{i}. {article['title']}")
        print(f"   Score: {result['seo_score']:.1f}/100 (Grade: {result['grade']})")
        print(f"   High Priority Issues: {results[-1]['high_priority_count']}")
        print()
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("=" * 60)
    print("RANKING (Best to Worst)")
    print("=" * 60)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   Score: {result['score']:.1f}/100 (Grade: {result['grade']})")
    print()


def example_save_report():
    """Demonstrate saving SEO report to file."""
    print("=" * 60)
    print("SEO AGENT - SAVE REPORT EXAMPLE")
    print("=" * 60)
    print()
    
    seo_agent = SEOAgent()
    
    # Sample content
    result = seo_agent.analyze_content(
        title="Cloud Computing Fundamentals",
        subtitle="Understanding cloud infrastructure and services",
        content="Cloud computing revolutionizes how businesses operate. " * 50,
        tags=["cloud", "computing", "infrastructure"]
    )
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"seo_report_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ SEO report saved to: {filename}")
    print(f"📊 Score: {result['seo_score']}/100")
    print(f"📝 Recommendations: {len(result['recommendations'])}")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "SEO SPECIALIST AGENT EXAMPLES" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    # Run examples
    example_basic_usage()
    print("\n" * 2)
    
    example_detailed_analysis()
    print("\n" * 2)
    
    example_batch_analysis()
    print("\n" * 2)
    
    example_save_report()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
    print()
    print("For more information, see: docs/seo_agent.md")
    print()


if __name__ == "__main__":
    main()
