"""
Tests for innovative features.
"""
import unittest
import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.analytics_agent import AnalyticsAgent
from agents.ab_testing import ABTestingFramework


class TestAnalyticsAgent(unittest.TestCase):
    """Test analytics agent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = "/tmp/test_analytics"
        os.makedirs(self.test_dir, exist_ok=True)
        self.agent = AnalyticsAgent(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.data_dir, self.test_dir)
    
    def test_collect_metrics_empty(self):
        """Test metrics collection with no data."""
        metrics = self.agent.collect_metrics()
        self.assertEqual(metrics['total_posts'], 0)
        self.assertEqual(len(metrics['posts_by_date']), 0)
    
    def test_collect_metrics_with_data(self):
        """Test metrics collection with sample data."""
        # Create sample publication record
        sample_record = {
            "title": "Test Post",
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "content_stats": {
                "text_word_count": 500,
                "video_duration": 30
            }
        }
        
        record_file = os.path.join(self.test_dir, "publication_record_test.json")
        with open(record_file, 'w') as f:
            json.dump(sample_record, f)
        
        metrics = self.agent.collect_metrics()
        self.assertEqual(metrics['total_posts'], 1)
        self.assertIn(500, metrics['word_counts'])
    
    def test_generate_insights(self):
        """Test insights generation."""
        insights = self.agent.generate_insights()
        self.assertIn('summary', insights)
        self.assertIn('recommendations', insights)
        self.assertIn('alerts', insights)
    
    def test_dashboard_data(self):
        """Test dashboard data generation."""
        dashboard = self.agent.get_dashboard_data()
        self.assertIn('metrics', dashboard)
        self.assertIn('insights', dashboard)
        self.assertIn('quick_stats', dashboard)


class TestABTestingFramework(unittest.TestCase):
    """Test A/B testing framework."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = "/tmp/test_abtesting"
        os.makedirs(self.test_dir, exist_ok=True)
        self.framework = ABTestingFramework(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test framework initializes correctly."""
        self.assertIsNotNone(self.framework)
        self.assertTrue(os.path.exists(self.framework.tests_dir))
    
    def test_create_test(self):
        """Test creating a new test."""
        variations = [
            {"name": "Variation A", "content": "Content A"},
            {"name": "Variation B", "content": "Content B"}
        ]
        
        test = self.framework.create_test(
            test_name="test_example",
            variations=variations,
            test_type="title"
        )
        
        self.assertIn('test_id', test)
        self.assertEqual(len(test['variations']), 2)
        self.assertEqual(test['status'], 'active')
    
    def test_create_test_insufficient_variations(self):
        """Test creating test with insufficient variations fails."""
        with self.assertRaises(ValueError):
            self.framework.create_test(
                test_name="test_fail",
                variations=[{"name": "Only one"}],
                test_type="title"
            )
    
    def test_record_result(self):
        """Test recording results."""
        variations = [
            {"name": "Variation A", "content": "A"},
            {"name": "Variation B", "content": "B"}
        ]
        
        test = self.framework.create_test("test_record", variations, "title")
        test_id = test['test_id']
        variation_id = test['variations'][0]['variation_id']
        
        # Record some metrics
        self.framework.record_result(test_id, variation_id, {
            "views": 100,
            "engagement": 25
        })
        
        # Verify metrics were recorded
        loaded_test = self.framework._load_test(test_id)
        self.assertEqual(loaded_test['variations'][0]['metrics']['views'], 100)
    
    def test_analyze_test(self):
        """Test analyzing test results."""
        variations = [
            {"name": "Variation A", "content": "A"},
            {"name": "Variation B", "content": "B"}
        ]
        
        test = self.framework.create_test("test_analyze", variations, "title")
        test_id = test['test_id']
        
        # Record results for both variations
        self.framework.record_result(test_id, test['variations'][0]['variation_id'], {
            "views": 100, "engagement": 20, "conversions": 5
        })
        self.framework.record_result(test_id, test['variations'][1]['variation_id'], {
            "views": 150, "engagement": 40, "conversions": 12
        })
        
        # Analyze
        analysis = self.framework.analyze_test(test_id)
        
        self.assertIn('winner', analysis)
        self.assertIn('confidence', analysis)
        self.assertIn('rankings', analysis)
        self.assertEqual(len(analysis['rankings']), 2)
    
    def test_list_active_tests(self):
        """Test listing active tests."""
        variations = [
            {"name": "Variation A", "content": "A"},
            {"name": "Variation B", "content": "B"}
        ]
        
        self.framework.create_test("test1", variations, "title")
        self.framework.create_test("test2", variations, "title")
        
        active = self.framework.list_active_tests()
        self.assertEqual(len(active), 2)
    
    def test_get_test_status(self):
        """Test getting test status."""
        variations = [
            {"name": "Variation A", "content": "A"},
            {"name": "Variation B", "content": "B"}
        ]
        
        test = self.framework.create_test("test_status", variations, "title")
        test_id = test['test_id']
        
        status = self.framework.get_test_status(test_id)
        
        self.assertIn('progress', status)
        self.assertIn('status', status)
        self.assertIn('variations_count', status)
        self.assertEqual(status['variations_count'], 2)


class TestIntegration(unittest.TestCase):
    """Test integration of innovative features."""
    
    def test_agents_can_be_imported(self):
        """Test that all agents can be imported."""
        from agents.analytics_agent import AnalyticsAgent
        from agents.ab_testing import ABTestingFramework
        
        # These require API keys, so just test import
        # from agents.performance_predictor import PerformancePredictorAgent
        # from agents.topic_trending import TopicTrendingAgent
        
        self.assertTrue(True)  # If we get here, imports worked
    
    def test_workflow_compatibility(self):
        """Test that agents work together."""
        test_dir = "/tmp/test_integration"
        os.makedirs(test_dir, exist_ok=True)
        
        try:
            analytics = AnalyticsAgent(data_dir=test_dir)
            ab_testing = ABTestingFramework(data_dir=test_dir)
            
            # Both agents can work with same directory
            metrics = analytics.collect_metrics()
            active_tests = ab_testing.list_active_tests()
            
            self.assertIsNotNone(metrics)
            self.assertIsNotNone(active_tests)
        
        finally:
            import shutil
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestAnalyticsAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestABTestingFramework))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
