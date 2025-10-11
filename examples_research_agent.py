#!/usr/bin/env python3
"""
Example usage of the Research Agent for topic discovery and SEO keyword analysis.

This script demonstrates how to use the Research Agent to:
1. Discover trending topics
2. Analyze SEO keywords
3. Generate complete research summaries
4. Integrate with content generation
"""
import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def example_basic_usage():
    """Demonstrate basic usage of Research Agent."""
    print("=" * 60)
    print("Research Agent - Basic Usage Example")
    print("=" * 60)
    print()
    
    from agents.research_agent import ResearchAgent
    
    # Initialize the agent
    research_agent = ResearchAgent()
    
    print("📊 Discovering trending topics...")
    print()
    
    # Note: This is a simulated example. In production, it would make OpenAI API calls.
    # For demonstration, we'll show the expected output format.
    
    simulated_topics = [
        {
            "topic": "The Rise of Autonomous AI Agents",
            "rationale": "Autonomous AI agents are becoming more sophisticated, handling complex tasks with minimal human intervention. This trend is accelerating across industries.",
            "trend_score": 9,
            "discovered_at": datetime.now().isoformat(),
            "source": "ai_trend_analysis"
        },
        {
            "topic": "Quantum Computing Breakthroughs in 2024",
            "rationale": "Recent advances in quantum error correction and qubit stability are bringing practical quantum computing closer to reality.",
            "trend_score": 8,
            "discovered_at": datetime.now().isoformat(),
            "source": "ai_trend_analysis"
        }
    ]
    
    print("✅ Discovered Topics:\n")
    for i, topic in enumerate(simulated_topics, 1):
        print(f"{i}. {topic['topic']}")
        print(f"   Trend Score: {topic['trend_score']}/10")
        print(f"   Rationale: {topic['rationale']}")
        print()


def example_seo_analysis():
    """Demonstrate SEO keyword analysis."""
    print("=" * 60)
    print("Research Agent - SEO Keyword Analysis")
    print("=" * 60)
    print()
    
    topic = "The Future of Artificial Intelligence in Healthcare"
    
    print(f"📊 Analyzing SEO keywords for: '{topic}'")
    print()
    
    # Simulated SEO analysis output
    simulated_seo = {
        "primary_keywords": [
            "AI healthcare",
            "artificial intelligence medicine",
            "medical AI"
        ],
        "secondary_keywords": [
            "healthcare technology",
            "AI diagnosis",
            "machine learning healthcare",
            "patient care AI",
            "medical automation"
        ],
        "long_tail_keywords": [
            "artificial intelligence in healthcare applications",
            "how AI is transforming healthcare",
            "AI medical diagnosis accuracy",
            "future of AI in patient care",
            "implementing AI in hospitals"
        ],
        "search_intent": "informational",
        "content_recommendations": "Focus on practical use cases, patient outcomes, and real-world implementation examples. Include statistics on AI accuracy and cost savings.",
        "estimated_monthly_searches": "10k-100k",
        "analyzed_at": datetime.now().isoformat(),
        "topic": topic
    }
    
    print("✅ SEO Analysis Results:\n")
    print(f"Primary Keywords: {', '.join(simulated_seo['primary_keywords'])}")
    print(f"\nSecondary Keywords: {', '.join(simulated_seo['secondary_keywords'])}")
    print(f"\nLong-tail Keywords:")
    for kw in simulated_seo['long_tail_keywords']:
        print(f"  - {kw}")
    print(f"\nSearch Intent: {simulated_seo['search_intent']}")
    print(f"Estimated Monthly Searches: {simulated_seo['estimated_monthly_searches']}")
    print(f"\nContent Recommendations:")
    print(f"  {simulated_seo['content_recommendations']}")
    print()


def example_complete_research():
    """Demonstrate complete research summary generation."""
    print("=" * 60)
    print("Research Agent - Complete Research Summary")
    print("=" * 60)
    print()
    
    print("📊 Generating complete research summary with 3 topics...")
    print()
    
    # Simulated complete research summary
    simulated_summary = {
        "research_date": datetime.now().isoformat(),
        "topic_count": 3,
        "base_topics": ["technology", "AI", "innovation"],
        "research_results": [
            {
                "topic": "Generative AI in Enterprise: Practical Applications",
                "rationale": "Enterprises are rapidly adopting generative AI for content creation, code generation, and business automation.",
                "trend_score": 9,
                "seo_keywords": {
                    "primary": ["generative AI", "enterprise AI", "business automation"],
                    "secondary": ["AI tools", "content generation", "code generation", "AI adoption"],
                    "long_tail": ["generative AI for enterprise", "how to implement generative AI", "enterprise AI use cases"]
                },
                "search_intent": "informational",
                "content_recommendations": "Focus on ROI, practical use cases, and implementation strategies. Include case studies.",
                "estimated_monthly_searches": "10k-100k",
                "discovered_at": datetime.now().isoformat()
            },
            {
                "topic": "The Evolution of Edge Computing and IoT",
                "rationale": "Edge computing is enabling real-time processing for IoT devices, reducing latency and bandwidth costs.",
                "trend_score": 8,
                "seo_keywords": {
                    "primary": ["edge computing", "IoT", "real-time processing"],
                    "secondary": ["edge devices", "distributed computing", "IoT platforms"],
                    "long_tail": ["edge computing vs cloud computing", "edge computing benefits", "IoT edge computing"]
                },
                "search_intent": "informational",
                "content_recommendations": "Explain technical concepts clearly, provide comparison charts, and discuss future trends.",
                "estimated_monthly_searches": "5k-50k",
                "discovered_at": datetime.now().isoformat()
            },
            {
                "topic": "Blockchain Beyond Cryptocurrency: Real-World Uses",
                "rationale": "Blockchain technology is finding applications in supply chain, healthcare, and identity management.",
                "trend_score": 7,
                "seo_keywords": {
                    "primary": ["blockchain applications", "blockchain technology", "distributed ledger"],
                    "secondary": ["supply chain blockchain", "blockchain healthcare", "smart contracts"],
                    "long_tail": ["blockchain use cases beyond crypto", "practical blockchain applications", "enterprise blockchain"]
                },
                "search_intent": "informational",
                "content_recommendations": "Move beyond cryptocurrency hype, focus on tangible business value and real implementations.",
                "estimated_monthly_searches": "5k-50k",
                "discovered_at": datetime.now().isoformat()
            }
        ],
        "agent_version": "1.0.0",
        "status": "success"
    }
    
    print("✅ Research Summary Generated:\n")
    print(f"Research Date: {simulated_summary['research_date']}")
    print(f"Topics Researched: {simulated_summary['topic_count']}")
    print(f"Status: {simulated_summary['status']}")
    print()
    
    for i, result in enumerate(simulated_summary['research_results'], 1):
        print(f"Topic #{i}: {result['topic']}")
        print(f"  Trend Score: {result['trend_score']}/10")
        print(f"  Primary Keywords: {', '.join(result['seo_keywords']['primary'])}")
        print(f"  Search Intent: {result['search_intent']}")
        print(f"  Est. Monthly Searches: {result['estimated_monthly_searches']}")
        print()


def example_integration_with_writer():
    """Demonstrate integration with content generation."""
    print("=" * 60)
    print("Research Agent - Integration with Writer Agent")
    print("=" * 60)
    print()
    
    print("📊 Workflow: Research → Content Generation → Publishing")
    print()
    
    # Simulated workflow
    print("Step 1: Research Agent discovers trending topic")
    topic_data = {
        "topic": "How AI is Revolutionizing Software Development",
        "trend_score": 9,
        "seo_keywords": {
            "primary": ["AI software development", "AI coding", "developer tools"],
            "secondary": ["code generation", "AI pair programming", "development automation"],
            "long_tail": ["AI tools for developers", "how AI improves coding", "AI code assistants"]
        },
        "search_intent": "informational",
        "content_recommendations": "Include practical examples, tool comparisons, and productivity metrics."
    }
    
    print(f"  ✅ Selected Topic: {topic_data['topic']}")
    print(f"  ✅ Trend Score: {topic_data['trend_score']}/10")
    print()
    
    print("Step 2: Writer Agent generates content using research data")
    print(f"  ✅ Generating blog post for: {topic_data['topic']}")
    print(f"  ✅ Optimizing for keywords: {', '.join(topic_data['seo_keywords']['primary'])}")
    print()
    
    print("Step 3: Content is optimized with SEO keywords")
    print(f"  ✅ Primary keywords integrated into title and headers")
    print(f"  ✅ Long-tail keywords used in body content")
    print(f"  ✅ Content follows recommendations: {topic_data['content_recommendations']}")
    print()
    
    print("Step 4: Ready for publishing")
    print(f"  ✅ SEO-optimized content ready")
    print(f"  ✅ Target search intent: {topic_data['search_intent']}")
    print()


def example_custom_topics():
    """Demonstrate research with custom topic areas."""
    print("=" * 60)
    print("Research Agent - Custom Topic Areas")
    print("=" * 60)
    print()
    
    custom_topics = ["machine learning", "blockchain", "cybersecurity"]
    
    print(f"📊 Researching custom topic areas: {', '.join(custom_topics)}")
    print()
    
    # Simulated results
    print("✅ Research Results:\n")
    
    results = [
        {
            "area": "machine learning",
            "topic": "Transfer Learning: Accelerating ML Model Development",
            "trend_score": 8
        },
        {
            "area": "blockchain",
            "topic": "Zero-Knowledge Proofs: Privacy in Blockchain",
            "trend_score": 7
        },
        {
            "area": "cybersecurity",
            "topic": "AI-Powered Threat Detection and Response",
            "trend_score": 9
        }
    ]
    
    for result in results:
        print(f"Topic Area: {result['area'].title()}")
        print(f"  Trending Topic: {result['topic']}")
        print(f"  Trend Score: {result['trend_score']}/10")
        print()


def main():
    """Run all examples."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         Research Agent - Usage Examples                   ║")
    print("╔════════════════════════════════════════════════════════════╗")
    print("\n")
    
    print("This demonstration shows the Research Agent capabilities.")
    print("Note: These are simulated outputs. In production, the agent")
    print("makes real API calls to OpenAI for trend analysis.\n")
    
    # Run examples
    example_basic_usage()
    input("Press Enter to continue to SEO analysis example...\n")
    
    example_seo_analysis()
    input("Press Enter to continue to complete research example...\n")
    
    example_complete_research()
    input("Press Enter to continue to integration example...\n")
    
    example_integration_with_writer()
    input("Press Enter to continue to custom topics example...\n")
    
    example_custom_topics()
    
    print("=" * 60)
    print("Examples Complete!")
    print("=" * 60)
    print()
    print("📚 For more information, see: docs/research_agent.md")
    print("🧪 To run tests: python -m unittest tests.test_research_agent")
    print()
    
    # Save example output
    output_data = {
        "demo_timestamp": datetime.now().isoformat(),
        "examples_run": [
            "basic_usage",
            "seo_analysis",
            "complete_research",
            "integration_with_writer",
            "custom_topics"
        ],
        "note": "These are simulated outputs for demonstration purposes"
    }
    
    output_dir = "generated_content"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/research_agent_demo.json", "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✅ Demo output saved to {output_dir}/research_agent_demo.json")


if __name__ == "__main__":
    main()
