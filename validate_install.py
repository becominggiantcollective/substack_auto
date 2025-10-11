#!/usr/bin/env python3
"""
Validation script for Substack Auto installation.

This script checks that all components are properly installed and configured.
"""
import sys
import os

def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False

def check_core_dependencies():
    """Check if core dependencies are available."""
    print("\nChecking core dependencies...")
    
    dependencies = {
        'openai': 'OpenAI API client',
        'requests': 'HTTP requests library',
        'dotenv': 'Environment variable management',
        'PIL': 'Image processing (Pillow)',
        'moviepy': 'Video generation',
        'schedule': 'Task scheduling',
        'pydantic': 'Configuration management',
        'tenacity': 'Retry logic'
    }
    
    success = True
    for module, description in dependencies.items():
        try:
            if module == 'dotenv':
                __import__('python_dotenv')
            elif module == 'PIL':
                __import__(module)
            else:
                __import__(module)
            print(f"  ✅ {description} ({module})")
        except ImportError:
            print(f"  ❌ {description} ({module}) - NOT INSTALLED")
            success = False
    
    return success

def check_optional_dependencies():
    """Check optional dependencies."""
    print("\nChecking optional dependencies (SEO & CrewAI)...")
    
    optional_deps = {
        'slugify': ('python-slugify', 'SEO slug generation'),
        'bs4': ('beautifulsoup4', 'HTML parsing'),
        'lxml': ('lxml', 'XML/HTML processing'),
        'crewai': ('crewai', 'Multi-agent AI framework'),
    }
    
    available = []
    unavailable = []
    
    for module, (package, description) in optional_deps.items():
        try:
            __import__(module)
            print(f"  ✅ {description} ({package})")
            available.append(package)
        except ImportError:
            print(f"  ⚠️  {description} ({package}) - NOT INSTALLED (optional)")
            unavailable.append(package)
    
    if unavailable:
        print(f"\n  💡 Install optional dependencies with:")
        print(f"     pip install {' '.join(unavailable)}")
    
    return True

def check_project_structure():
    """Check project structure."""
    print("\nChecking project structure...")
    
    required_paths = [
        ('src', 'directory'),
        ('src/agents', 'directory'),
        ('src/agents/seo_agent.py', 'file'),
        ('src/content_generators', 'directory'),
        ('src/publishers', 'directory'),
        ('src/config', 'directory'),
        ('tests', 'directory'),
        ('tests/test_agents.py', 'file'),
        ('requirements.txt', 'file'),
        ('README.md', 'file'),
    ]
    
    success = True
    for path, path_type in required_paths:
        if path_type == 'directory':
            exists = os.path.isdir(path)
        else:
            exists = os.path.isfile(path)
        
        if exists:
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path} - MISSING")
            success = False
    
    return success

def check_seo_agent():
    """Check SEO agent functionality."""
    print("\nChecking SEO agent functionality...")
    
    try:
        sys.path.insert(0, 'src')
        from agents.seo_agent import SEOAnalyzer
        
        analyzer = SEOAnalyzer()
        print("  ✅ SEOAnalyzer imported successfully")
        
        # Test basic functionality
        slug = analyzer.generate_slug("Test Title")
        if slug:
            print(f"  ✅ Slug generation working: '{slug}'")
        
        analysis = analyzer.analyze_title("Test Title for SEO")
        if 'slug' in analysis and 'recommendations' in analysis:
            print("  ✅ Title analysis working")
        
        content = "Test content " * 50
        content_analysis = analyzer.analyze_content(content)
        if 'word_count' in content_analysis:
            print("  ✅ Content analysis working")
        
        report = analyzer.generate_seo_report("Test", content)
        if 'overall_score' in report:
            print(f"  ✅ SEO report generation working (score: {report['overall_score']}/100)")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def check_tests():
    """Check if tests can run."""
    print("\nChecking test suite...")
    
    try:
        import unittest
        loader = unittest.TestLoader()
        
        # Try to load agent tests
        suite = loader.loadTestsFromName('tests.test_agents')
        test_count = suite.countTestCases()
        
        if test_count > 0:
            print(f"  ✅ Test suite loaded: {test_count} tests found")
            print("  💡 Run tests with: python -m unittest tests.test_agents")
            return True
        else:
            print("  ⚠️  No tests found")
            return False
    except Exception as e:
        print(f"  ❌ Error loading tests: {e}")
        return False

def main():
    """Run all validation checks."""
    print("=" * 70)
    print("SUBSTACK AUTO - INSTALLATION VALIDATION")
    print("=" * 70)
    print()
    
    results = {
        'Python Version': check_python_version(),
        'Core Dependencies': check_core_dependencies(),
        'Optional Dependencies': check_optional_dependencies(),
        'Project Structure': check_project_structure(),
        'SEO Agent': check_seo_agent(),
        'Test Suite': check_tests(),
    }
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check}")
    
    all_passed = all(results.values())
    
    print()
    if all_passed:
        print("🎉 All checks passed! Installation is complete and validated.")
        print()
        print("Next steps:")
        print("  1. Run demo: python demo_seo_agent.py")
        print("  2. Run tests: python -m unittest tests.test_agents")
        print("  3. Configure .env file with your API keys")
        print("  4. Start using: python cli.py generate")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print()
        print("To fix issues:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Ensure you're in the project root directory")
        print("  3. Check that all files were properly cloned")
    
    print()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
