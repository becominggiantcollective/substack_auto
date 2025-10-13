#!/usr/bin/env python3
"""
Command-line interface for Substack Auto content generation system.
"""
import os
import sys
import argparse
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_environment():
    """Check if required environment variables are set."""
    required_vars = [
        'OPENAI_API_KEY',
        'SUBSTACK_EMAIL', 
        'SUBSTACK_PASSWORD',
        'SUBSTACK_PUBLICATION'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print("💡 To fix this:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env with your API keys and credentials")
        print("   3. Run: source .env (or load environment variables)")
        return False
    
    print("✅ Environment variables configured")
    return True

def setup_wizard():
    """Interactive setup wizard."""
    print("🧙 Substack Auto Setup Wizard")
    print("=" * 40)
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("📁 Found existing .env file")
        response = input("Do you want to update it? (y/N): ").lower().strip()
        if response != 'y':
            print("Setup cancelled.")
            return
    else:
        print("📝 Creating new .env file from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file from template")
        else:
            print("❌ .env.example not found")
            return
    
    print()
    print("🔑 Please edit the .env file with your credentials:")
    print("   - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys")
    print("   - SUBSTACK_EMAIL: Your Substack account email")
    print("   - SUBSTACK_PASSWORD: Your Substack account password") 
    print("   - SUBSTACK_PUBLICATION: Your publication name")
    print()
    print("⚙️ Optional settings:")
    print("   - MAX_POSTS_PER_DAY: Number of posts per day (default: 3)")
    print("   - CONTENT_TOPICS: Comma-separated topics (default: technology,AI,innovation,science)")
    print("   - IMAGE_STYLE: Image generation style (default: digital art,modern,professional)")
    print()
    print("🎨 AI Content Shaping Options:")
    print("   - CONTENT_TONE: Tone of the content (default: professional and engaging)")
    print("   - TARGET_AUDIENCE: Target audience (default: intelligent general audience)")
    print("   - CONTENT_STYLE: Content style (default: informative and thought-provoking)")
    print("   - CUSTOM_INSTRUCTIONS: Additional custom instructions for AI content generation")
    print()
    print("💾 Save the .env file and run this command again to continue.")

def run_demo():
    """Run the demonstration."""
    print("🎬 Running Substack Auto Demo...")
    os.system(f"{sys.executable} demo.py")

def run_innovative_demo():
    """Run the innovative features demonstration."""
    print("🚀 Running Innovative Features Demo...")
    os.system(f"{sys.executable} demo_innovative_features.py")

def generate_single_post():
    """Generate a single post."""
    if not check_environment():
        return
    
    print("📝 Generating single blog post...")
    try:
        from main import ContentOrchestrator
        orchestrator = ContentOrchestrator()
        result = orchestrator.create_and_publish_post()
        
        print("\n📊 Generation Result:")
        print(json.dumps(result, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ Error generating post: {e}")
        print("💡 Make sure your API keys are valid and you have internet access")

def start_scheduler():
    """Start the automated scheduler."""
    if not check_environment():
        return
    
    print("⏰ Starting automated scheduler...")
    print("📅 Posts will be generated and published according to schedule")
    print("⚠️ Press Ctrl+C to stop")
    
    try:
        from main import ContentOrchestrator
        orchestrator = ContentOrchestrator()
        orchestrator.setup_scheduled_publishing()
        orchestrator.run_scheduler()
        
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
    except Exception as e:
        print(f"❌ Error in scheduler: {e}")

def show_status():
    """Show system status."""
    if not check_environment():
        return
    
    try:
        from main import ContentOrchestrator
        orchestrator = ContentOrchestrator()
        status = orchestrator.get_status()
        
        print("📊 Substack Auto Status")
        print("=" * 30)
        print(json.dumps(status, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ Error getting status: {e}")

def show_analytics():
    """Show analytics dashboard."""
    if not check_environment():
        return
    
    try:
        from main import ContentOrchestrator
        orchestrator = ContentOrchestrator()
        dashboard = orchestrator.get_analytics_dashboard()
        
        print("📊 Analytics Dashboard")
        print("=" * 50)
        
        # Quick stats
        quick_stats = dashboard.get("quick_stats", {})
        print("\n📈 Quick Stats:")
        print(f"  • Total Posts: {quick_stats.get('total_posts', 0)}")
        print(f"  • Avg Word Count: {quick_stats.get('avg_word_count', 0):.0f}")
        print(f"  • Avg Fact Check: {quick_stats.get('avg_fact_score', 0):.2f}")
        print(f"  • Avg SEO Score: {quick_stats.get('avg_seo_score', 0):.2f}")
        print(f"  • Overall Performance: {quick_stats.get('overall_performance', 0):.2f}")
        
        # Insights
        insights = dashboard.get("insights", {})
        recommendations = insights.get("recommendations", [])
        if recommendations:
            print(f"\n💡 Top Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"  {i}. [{rec.get('priority', 'medium')}] {rec.get('message', '')}")
        
        alerts = insights.get("alerts", [])
        if alerts:
            print(f"\n⚠️  Alerts:")
            for alert in alerts:
                print(f"  • {alert.get('message', '')}")
        
        print("\n✅ Full dashboard exported to analytics_report.json")
        
        # Export full report
        orchestrator.analytics.export_report()
        
    except Exception as e:
        print(f"❌ Error getting analytics: {e}")

def predict_performance():
    """Predict content performance."""
    if not check_environment():
        return
    
    print("🔮 Content Performance Predictor")
    print("=" * 50)
    
    try:
        from main import ContentOrchestrator
        orchestrator = ContentOrchestrator()
        
        # Generate content with prediction
        print("\nGenerating content with performance prediction...")
        content = orchestrator.generate_with_prediction()
        
        prediction = content.get("performance_prediction", {})
        
        print(f"\n📊 Performance Prediction:")
        print(f"  • Overall Score: {prediction.get('overall_score', 0):.2f}/1.0")
        
        overall = prediction.get("overall_prediction", {})
        print(f"  • Success Probability: {overall.get('success_probability', 0):.2f}")
        print(f"  • Expected Audience: {overall.get('expected_audience_size', 'unknown')}")
        
        recommendations = prediction.get("recommendations", {})
        improvements = recommendations.get("improvements", [])
        if improvements:
            print(f"\n✅ Suggested Improvements:")
            for i, improvement in enumerate(improvements[:3], 1):
                print(f"  {i}. {improvement}")
        
    except Exception as e:
        print(f"❌ Error predicting performance: {e}")

def get_trending_topics():
    """Get trending topic suggestions."""
    if not check_environment():
        return
    
    print("🔥 Trending Topics")
    print("=" * 50)
    
    try:
        from main import ContentOrchestrator
        orchestrator = ContentOrchestrator()
        
        print("\nAnalyzing trending topics...")
        suggestions = orchestrator.suggest_trending_topics(count=5)
        
        print(f"\n💡 Content Suggestions ({len(suggestions)}):")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {suggestion.get('title_suggestion', 'Unknown')}")
            print(f"   Priority: {suggestion.get('priority', 'medium').upper()}")
            print(f"   Topic: {suggestion.get('topic', 'N/A')}")
            print(f"   Relevance: {suggestion.get('relevance_score', 0):.2f}")
        
    except Exception as e:
        print(f"❌ Error getting trending topics: {e}")

def manage_ab_tests():
    """Manage A/B tests."""
    if not check_environment():
        return
    
    print("🧪 A/B Testing Management")
    print("=" * 50)
    
    try:
        from main import ContentOrchestrator
        orchestrator = ContentOrchestrator()
        
        # List active tests
        active_tests = orchestrator.ab_testing.list_active_tests()
        
        print(f"\n📋 Active Tests ({len(active_tests)}):")
        for i, test in enumerate(active_tests, 1):
            print(f"\n{i}. {test['test_name']}")
            print(f"   ID: {test['test_id']}")
            print(f"   Type: {test['test_type']}")
            print(f"   Variations: {test['variations_count']}")
            print(f"   Created: {test['created_at']}")
        
        if not active_tests:
            print("  No active tests")
            print("\n💡 Create a test with orchestrator.create_ab_test() in Python")
        
    except Exception as e:
        print(f"❌ Error managing A/B tests: {e}")

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Substack Auto - AI-Powered Content Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s setup          # Run setup wizard
  %(prog)s demo           # Run demonstration
  %(prog)s innovative     # Run innovative features demo
  %(prog)s generate       # Generate one post
  %(prog)s schedule       # Start automated scheduler
  %(prog)s status         # Show system status
  %(prog)s analytics      # View analytics dashboard
  %(prog)s predict        # Predict content performance
  %(prog)s trends         # Get trending topics
  %(prog)s abtest         # Manage A/B tests
        """
    )
    
    parser.add_argument('command', 
                       choices=['setup', 'demo', 'innovative', 'generate', 'schedule', 
                               'status', 'analytics', 'predict', 'trends', 'abtest'],
                       help='Command to execute')
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    print("🤖 Substack Auto - AI Content Generation System")
    print("=" * 50)
    
    if args.command == 'setup':
        setup_wizard()
    elif args.command == 'demo':
        run_demo()
    elif args.command == 'innovative':
        run_innovative_demo()
    elif args.command == 'generate':
        generate_single_post()
    elif args.command == 'schedule':
        start_scheduler()
    elif args.command == 'status':
        show_status()
    elif args.command == 'analytics':
        show_analytics()
    elif args.command == 'predict':
        predict_performance()
    elif args.command == 'trends':
        get_trending_topics()
    elif args.command == 'abtest':
        manage_ab_tests()

if __name__ == "__main__":
    main()