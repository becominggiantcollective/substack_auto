"""
Framework Comparison Script
============================

This script provides a simple interface to test and compare
CrewAI and AutoGen frameworks for content generation.

Usage:
    python comparison_demo.py --framework crewai
    python comparison_demo.py --framework autogen
    python comparison_demo.py --framework both
"""

import sys
import os
import time
import argparse
from typing import Dict, Any

# Add demos to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_crewai_demo(topic: str) -> Dict[str, Any]:
    """Run CrewAI demo and measure performance.
    
    Args:
        topic: The blog post topic
    
    Returns:
        Results dictionary with timing and success metrics
    """
    print("\n" + "="*80)
    print("🤖 Running CrewAI Demo")
    print("="*80)
    
    try:
        from demos.crewai.content_seo_demo import ContentSEOCrew
        
        crew = ContentSEOCrew()
        
        start_time = time.time()
        result = crew.generate_content(topic=topic, target_word_count=1000)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        return {
            "framework": "CrewAI",
            "success": result.get("success", False),
            "execution_time": execution_time,
            "agents_used": result.get("agents_used", 0),
            "tasks_completed": result.get("tasks_completed", 0),
            "output": result.get("result", ""),
            "error": None
        }
    
    except Exception as e:
        return {
            "framework": "CrewAI",
            "success": False,
            "execution_time": 0,
            "agents_used": 0,
            "tasks_completed": 0,
            "output": "",
            "error": str(e)
        }


def run_autogen_demo(topic: str) -> Dict[str, Any]:
    """Run AutoGen demo and measure performance.
    
    Args:
        topic: The blog post topic
    
    Returns:
        Results dictionary with timing and success metrics
    """
    print("\n" + "="*80)
    print("🤖 Running AutoGen Demo")
    print("="*80)
    
    try:
        from demos.autogen.content_demo import ContentAutoGenWorkflow
        
        workflow = ContentAutoGenWorkflow()
        
        start_time = time.time()
        result = workflow.generate_content_sequential(topic=topic)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Estimate output length
        output_length = sum([
            len(result.get("seo_guidance", "")),
            len(result.get("blog_content", "")),
            len(result.get("seo_optimization", "")),
            len(result.get("editorial_review", ""))
        ])
        
        return {
            "framework": "AutoGen",
            "success": result.get("success", False),
            "execution_time": execution_time,
            "agents_used": result.get("agents_used", 0),
            "output_length": output_length,
            "output": result.get("blog_content", "")[:500],  # Sample
            "error": None
        }
    
    except Exception as e:
        return {
            "framework": "AutoGen",
            "success": False,
            "execution_time": 0,
            "agents_used": 0,
            "output_length": 0,
            "output": "",
            "error": str(e)
        }


def print_comparison(crewai_results: Dict[str, Any] = None, 
                    autogen_results: Dict[str, Any] = None):
    """Print comparison table of results.
    
    Args:
        crewai_results: Results from CrewAI demo
        autogen_results: Results from AutoGen demo
    """
    print("\n" + "="*80)
    print("📊 COMPARISON RESULTS")
    print("="*80)
    
    if crewai_results:
        print("\n🟢 CrewAI Results:")
        print(f"   ✓ Success: {crewai_results['success']}")
        print(f"   ⏱️  Execution Time: {crewai_results['execution_time']:.2f}s")
        print(f"   👥 Agents Used: {crewai_results['agents_used']}")
        print(f"   ✅ Tasks Completed: {crewai_results.get('tasks_completed', 'N/A')}")
        if crewai_results['error']:
            print(f"   ❌ Error: {crewai_results['error']}")
    
    if autogen_results:
        print("\n🔵 AutoGen Results:")
        print(f"   ✓ Success: {autogen_results['success']}")
        print(f"   ⏱️  Execution Time: {autogen_results['execution_time']:.2f}s")
        print(f"   👥 Agents Used: {autogen_results['agents_used']}")
        print(f"   📝 Output Length: {autogen_results.get('output_length', 'N/A')} chars")
        if autogen_results['error']:
            print(f"   ❌ Error: {autogen_results['error']}")
    
    if crewai_results and autogen_results and crewai_results['success'] and autogen_results['success']:
        print("\n📈 Comparison:")
        time_diff = autogen_results['execution_time'] - crewai_results['execution_time']
        faster = "CrewAI" if time_diff > 0 else "AutoGen"
        print(f"   ⚡ Faster: {faster} (by {abs(time_diff):.2f}s)")
        
        if crewai_results['execution_time'] > 0:
            efficiency = (autogen_results['execution_time'] / crewai_results['execution_time'] - 1) * 100
            print(f"   📊 Efficiency: CrewAI is {abs(efficiency):.1f}% {'faster' if efficiency > 0 else 'slower'}")
    
    print("\n" + "="*80)


def main():
    """Main function to run comparison."""
    
    parser = argparse.ArgumentParser(description='Compare CrewAI and AutoGen frameworks')
    parser.add_argument('--framework', 
                       choices=['crewai', 'autogen', 'both'], 
                       default='both',
                       help='Which framework(s) to test')
    parser.add_argument('--topic', 
                       type=str,
                       default='The Future of AI-Powered Content Creation',
                       help='Blog post topic to generate')
    
    args = parser.parse_args()
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║           CrewAI vs AutoGen Framework Comparison                       ║
    ║                      for Substack Auto                                 ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    print(f"\n📝 Topic: {args.topic}")
    print(f"🔬 Testing: {args.framework.upper()}")
    
    crewai_results = None
    autogen_results = None
    
    # Run selected framework(s)
    if args.framework in ['crewai', 'both']:
        crewai_results = run_crewai_demo(args.topic)
    
    if args.framework in ['autogen', 'both']:
        autogen_results = run_autogen_demo(args.topic)
    
    # Print comparison
    print_comparison(crewai_results, autogen_results)
    
    # Print recommendation
    if args.framework == 'both':
        print("\n" + "="*80)
        print("💡 RECOMMENDATION")
        print("="*80)
        print("""
Based on comprehensive evaluation (see docs/research/crewai_vs_autogen_evaluation.md):

🏆 CrewAI is recommended for Substack Auto because:

1. ✅ Purpose-built for sequential content workflows
2. ✅ Better SEO integration (built-in tools)
3. ✅ Simpler API and faster implementation
4. ✅ Lower cost (30-40% fewer API calls)
5. ✅ More predictable execution patterns

📖 Full evaluation document: docs/research/crewai_vs_autogen_evaluation.md
        """)
        print("="*80)


if __name__ == "__main__":
    main()
