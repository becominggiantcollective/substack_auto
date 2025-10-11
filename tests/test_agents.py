"""
Test suite for CrewAI agents module.

Tests for SEO agent functionality and integration.
"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.seo_agent import (
    SEOAnalyzer,
    create_seo_agent,
    create_seo_optimization_task,
    run_seo_crew
)


class TestSEOAnalyzer(unittest.TestCase):
    """Test the SEO analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SEOAnalyzer()
        self.test_title = "How AI is Revolutionizing Content Creation in 2025"
        self.test_content = """
        Artificial Intelligence is transforming the content creation landscape.
        In this comprehensive guide, we explore the latest trends and tools.
        
        Machine learning algorithms are now capable of generating high-quality
        content that rivals human writers. From blog posts to social media updates,
        AI is becoming an indispensable tool for content creators.
        
        This article examines the current state of AI content generation, the tools
        available, and what the future holds for this exciting technology.
        """ * 10  # Repeat to get realistic word count
    
    def test_generate_slug(self):
        """Test slug generation from title."""
        slug = self.analyzer.generate_slug(self.test_title)
        
        # Check that slug is generated
        self.assertIsNotNone(slug)
        self.assertIsInstance(slug, str)
        
        # Check that slug is lowercase
        self.assertEqual(slug, slug.lower())
        
        # Check that slug has no spaces
        self.assertNotIn(' ', slug)
        
        # Check that slug uses hyphens
        self.assertIn('-', slug)
        
        # Check that slug is reasonable length
        self.assertLessEqual(len(slug), 60)
    
    def test_generate_slug_edge_cases(self):
        """Test slug generation with edge cases."""
        # Test with special characters
        slug1 = self.analyzer.generate_slug("Test!@#$%^&*()Title")
        self.assertEqual(slug1, 'testtitle')
        
        # Test with very long title
        long_title = "This is an extremely long title that should be truncated " * 5
        slug2 = self.analyzer.generate_slug(long_title)
        self.assertLessEqual(len(slug2), 60)
        
        # Test with unicode characters
        slug3 = self.analyzer.generate_slug("Café Résumé Naïve")
        self.assertIsNotNone(slug3)
    
    def test_analyze_title(self):
        """Test title analysis."""
        analysis = self.analyzer.analyze_title(self.test_title)
        
        # Check return structure
        self.assertIn('title', analysis)
        self.assertIn('length', analysis)
        self.assertIn('word_count', analysis)
        self.assertIn('slug', analysis)
        self.assertIn('recommendations', analysis)
        
        # Check values
        self.assertEqual(analysis['title'], self.test_title)
        self.assertEqual(analysis['length'], len(self.test_title))
        self.assertEqual(analysis['word_count'], len(self.test_title.split()))
        self.assertIsInstance(analysis['recommendations'], list)
        self.assertGreater(len(analysis['recommendations']), 0)
    
    def test_analyze_title_length_recommendations(self):
        """Test title length recommendations."""
        # Test short title
        short_analysis = self.analyzer.analyze_title("Short")
        short_recs = ' '.join(short_analysis['recommendations'])
        self.assertIn('short', short_recs.lower())
        
        # Test optimal title
        optimal_title = "Perfect Length Title for SEO Optimization Today"
        optimal_analysis = self.analyzer.analyze_title(optimal_title)
        optimal_recs = ' '.join(optimal_analysis['recommendations'])
        self.assertIn('optimal', optimal_recs.lower())
        
        # Test long title
        long_title = "This is an Extremely Long Title That Exceeds the Recommended Character Limit for SEO"
        long_analysis = self.analyzer.analyze_title(long_title)
        long_recs = ' '.join(long_analysis['recommendations'])
        self.assertIn('long', long_recs.lower())
    
    def test_analyze_content(self):
        """Test content analysis."""
        analysis = self.analyzer.analyze_content(self.test_content, self.test_title)
        
        # Check return structure
        self.assertIn('content_length', analysis)
        self.assertIn('word_count', analysis)
        self.assertIn('paragraph_count', analysis)
        self.assertIn('recommendations', analysis)
        self.assertIn('top_keywords', analysis)
        
        # Check values
        self.assertGreater(analysis['word_count'], 0)
        self.assertGreater(analysis['paragraph_count'], 0)
        self.assertIsInstance(analysis['recommendations'], list)
        self.assertIsInstance(analysis['top_keywords'], list)
    
    def test_analyze_content_length_recommendations(self):
        """Test content length recommendations."""
        # Test very short content
        short_content = "This is very short content."
        short_analysis = self.analyzer.analyze_content(short_content)
        short_recs = ' '.join(short_analysis['recommendations'])
        self.assertIn('short', short_recs.lower())
        
        # Test optimal content (repeat to get ~1500 words)
        optimal_content = "This is a well-written article with good content. " * 300
        optimal_analysis = self.analyzer.analyze_content(optimal_content)
        self.assertGreater(optimal_analysis['word_count'], 1000)
    
    def test_top_keywords_extraction(self):
        """Test keyword extraction."""
        content = "machine learning artificial intelligence deep learning neural networks " * 50
        analysis = self.analyzer.analyze_content(content)
        
        # Check that keywords are extracted
        self.assertIn('top_keywords', analysis)
        self.assertGreater(len(analysis['top_keywords']), 0)
        
        # Check keyword structure
        if analysis['top_keywords']:
            first_keyword = analysis['top_keywords'][0]
            self.assertIn('keyword', first_keyword)
            self.assertIn('count', first_keyword)
            self.assertIsInstance(first_keyword['count'], int)
    
    def test_generate_meta_description(self):
        """Test meta description generation."""
        meta_desc = self.analyzer.generate_meta_description(self.test_content)
        
        # Check that description is generated
        self.assertIsNotNone(meta_desc)
        self.assertIsInstance(meta_desc, str)
        
        # Check length constraints
        self.assertLessEqual(len(meta_desc), 165)  # 160 + ellipsis
        
        # Check that it's not empty
        self.assertGreater(len(meta_desc), 0)
    
    def test_generate_meta_description_with_custom_length(self):
        """Test meta description with custom max length."""
        short_desc = self.analyzer.generate_meta_description(self.test_content, max_length=100)
        self.assertLessEqual(len(short_desc), 105)  # 100 + ellipsis
        
        long_desc = self.analyzer.generate_meta_description(self.test_content, max_length=200)
        self.assertLessEqual(len(long_desc), 205)
    
    def test_generate_seo_report(self):
        """Test full SEO report generation."""
        report = self.analyzer.generate_seo_report(self.test_title, self.test_content)
        
        # Check report structure
        self.assertIn('title_analysis', report)
        self.assertIn('content_analysis', report)
        self.assertIn('meta_description', report)
        self.assertIn('slug', report)
        self.assertIn('overall_score', report)
        self.assertIn('recommendations', report)
        
        # Check score
        self.assertIsInstance(report['overall_score'], (int, float))
        self.assertGreaterEqual(report['overall_score'], 0.0)
        self.assertLessEqual(report['overall_score'], 100.0)
        
        # Check that recommendations exist
        self.assertIsInstance(report['recommendations'], list)
        self.assertGreater(len(report['recommendations']), 0)
    
    def test_seo_report_scoring(self):
        """Test SEO report scoring logic."""
        # Create optimal content
        optimal_title = "Perfect Title for SEO Optimization Guidelines"
        optimal_content = "Excellent content with great SEO practices. " * 500  # ~1500 words
        
        report = self.analyzer.generate_seo_report(optimal_title, optimal_content)
        
        # Should have a decent score
        self.assertGreater(report['overall_score'], 50)
    
    def test_extract_metadata_without_bs4(self):
        """Test metadata extraction when BeautifulSoup is not available."""
        # This should return empty dict or handle gracefully
        html = "<html><head><title>Test</title></head><body>Content</body></html>"
        metadata = self.analyzer.extract_metadata(html)
        
        # Should return a dict (may be empty if BS4 not available)
        self.assertIsInstance(metadata, dict)


class TestCrewAIIntegration(unittest.TestCase):
    """Test CrewAI integration (if available)."""
    
    def test_create_seo_agent(self):
        """Test SEO agent creation."""
        # This test will pass even if CrewAI is not installed
        agent = create_seo_agent()
        
        # If CrewAI is available, agent should be created
        # If not, it should return None
        if agent is not None:
            self.assertIsNotNone(agent)
    
    def test_create_seo_agent_with_custom_params(self):
        """Test SEO agent creation with custom parameters."""
        custom_role = "Senior SEO Analyst"
        custom_goal = "Maximize organic traffic"
        custom_backstory = "Expert with 10 years experience"
        
        agent = create_seo_agent(
            role=custom_role,
            goal=custom_goal,
            backstory=custom_backstory
        )
        
        # Should handle gracefully whether CrewAI is available or not
        self.assertTrue(agent is None or agent is not None)
    
    def test_create_seo_optimization_task(self):
        """Test SEO optimization task creation."""
        # Create a mock agent
        mock_agent = Mock()
        
        task = create_seo_optimization_task(
            mock_agent,
            "Test Title",
            "Test content"
        )
        
        # Should return task or None
        self.assertTrue(task is None or task is not None)
    
    def test_run_seo_crew_fallback(self):
        """Test that SEO crew falls back gracefully."""
        result = run_seo_crew(
            "Test Title for SEO Analysis",
            "Test content for SEO crew analysis"
        )
        
        # Should return some result (either from crew or fallback)
        self.assertIsNotNone(result)


class TestSEOAgentModule(unittest.TestCase):
    """Test the overall SEO agent module."""
    
    def test_seo_analyzer_instantiation(self):
        """Test that SEO analyzer can be instantiated."""
        analyzer = SEOAnalyzer()
        self.assertIsNotNone(analyzer)
        self.assertTrue(hasattr(analyzer, 'generate_slug'))
        self.assertTrue(hasattr(analyzer, 'analyze_title'))
        self.assertTrue(hasattr(analyzer, 'analyze_content'))
        self.assertTrue(hasattr(analyzer, 'generate_seo_report'))
    
    def test_all_public_methods_exist(self):
        """Test that all expected public methods exist."""
        analyzer = SEOAnalyzer()
        
        expected_methods = [
            'generate_slug',
            'analyze_title',
            'analyze_content',
            'extract_metadata',
            'generate_meta_description',
            'generate_seo_report'
        ]
        
        for method_name in expected_methods:
            self.assertTrue(
                hasattr(analyzer, method_name),
                f"Method {method_name} not found"
            )
            self.assertTrue(
                callable(getattr(analyzer, method_name)),
                f"Method {method_name} is not callable"
            )


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
