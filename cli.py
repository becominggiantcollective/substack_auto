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
    print("💾 Save the .env file and run this command again to continue.")

def run_demo():
    """Run the demonstration."""
    print("🎬 Running Substack Auto Demo...")
    os.system(f"{sys.executable} demo.py")

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

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Substack Auto - AI-Powered Content Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s setup          # Run setup wizard
  %(prog)s demo           # Run demonstration
  %(prog)s generate       # Generate one post
  %(prog)s schedule       # Start automated scheduler
  %(prog)s status         # Show system status
        """
    )
    
    parser.add_argument('command', 
                       choices=['setup', 'demo', 'generate', 'schedule', 'status'],
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
    elif args.command == 'generate':
        generate_single_post()
    elif args.command == 'schedule':
        start_scheduler()
    elif args.command == 'status':
        show_status()

if __name__ == "__main__":
    main()