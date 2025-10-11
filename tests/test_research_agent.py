"""
Test suite for the Research Agent.
"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.research_agent import ResearchAgent


class TestResearchAgent(unittest.TestCase):
    """Test the Research Agent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        }):
            self.research_agent = ResearchAgent()
    
    @patch('agents.research_agent.OpenAI')
    def test_discover_trending_topics(self, mock_openai):
        """Test trending topic discovery."""
        # Mock OpenAI response with JSON
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps([
            {
                "topic": "The Future of AI Agents",
                "rationale": "AI agents are becoming more sophisticated and autonomous",
                "trend_score": 9
            },
            {
                "topic": "Quantum Computing Breakthroughs",
                "rationale": "Recent advances in quantum computing are making headlines",
                "trend_score": 8
            }
        ])
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        topics = self.research_agent.discover_trending_topics(count=2)
        
        self.assertEqual(len(topics), 2)
        self.assertEqual(topics[0]["topic"], "The Future of AI Agents")
        self.assertEqual(topics[0]["trend_score"], 9)
        self.assertIn("discovered_at", topics[0])
        self.assertIn("source", topics[0])
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('agents.research_agent.OpenAI')
    def test_discover_trending_topics_with_code_blocks(self, mock_openai):
        """Test handling of JSON wrapped in code blocks."""
        # Mock OpenAI response with code block formatting
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """```json
[
    {
        "topic": "Test Topic",
        "rationale": "Test rationale",
        "trend_score": 7
    }
]
```"""
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        topics = self.research_agent.discover_trending_topics(count=1)
        
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0]["topic"], "Test Topic")
    
    @patch('agents.research_agent.OpenAI')
    def test_discover_trending_topics_custom_base_topics(self, mock_openai):
        """Test topic discovery with custom base topics."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps([
            {
                "topic": "Custom Topic",
                "rationale": "Custom rationale",
                "trend_score": 8
            }
        ])
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        custom_topics = ["blockchain", "cryptocurrency"]
        topics = self.research_agent.discover_trending_topics(
            base_topics=custom_topics,
            count=1
        )
        
        self.assertEqual(len(topics), 1)
        
        # Verify the prompt includes custom topics
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args[1]['messages'][0]['content']
        self.assertIn("blockchain", prompt)
        self.assertIn("cryptocurrency", prompt)
    
    def test_discover_trending_topics_fallback(self):
        """Test fallback topic generation when API fails."""
        topics = self.research_agent._generate_fallback_topics(
            ["AI", "technology"],
            count=2
        )
        
        self.assertEqual(len(topics), 2)
        self.assertIn("topic", topics[0])
        self.assertIn("rationale", topics[0])
        self.assertIn("trend_score", topics[0])
        self.assertIn("discovered_at", topics[0])
        self.assertEqual(topics[0]["source"], "fallback_generation")
    
    @patch('agents.research_agent.OpenAI')
    def test_analyze_seo_keywords(self, mock_openai):
        """Test SEO keyword analysis."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "primary_keywords": ["artificial intelligence", "AI trends", "machine learning"],
            "secondary_keywords": ["deep learning", "neural networks", "AI applications"],
            "long_tail_keywords": [
                "artificial intelligence in business",
                "how to implement AI",
                "AI trends 2024"
            ],
            "search_intent": "informational",
            "content_recommendations": "Focus on practical use cases and real-world examples",
            "estimated_monthly_searches": "10k-100k"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        seo_data = self.research_agent.analyze_seo_keywords(
            "The Future of Artificial Intelligence"
        )
        
        self.assertIn("primary_keywords", seo_data)
        self.assertIn("secondary_keywords", seo_data)
        self.assertIn("long_tail_keywords", seo_data)
        self.assertIn("search_intent", seo_data)
        self.assertIn("content_recommendations", seo_data)
        self.assertIn("analyzed_at", seo_data)
        self.assertIn("topic", seo_data)
        
        self.assertEqual(len(seo_data["primary_keywords"]), 3)
        self.assertEqual(seo_data["search_intent"], "informational")
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('agents.research_agent.OpenAI')
    def test_analyze_seo_keywords_with_targets(self, mock_openai):
        """Test SEO analysis with target keywords."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "primary_keywords": ["target keyword", "AI", "technology"],
            "secondary_keywords": ["related keyword"],
            "long_tail_keywords": ["long tail phrase"],
            "search_intent": "informational",
            "content_recommendations": "Use target keywords naturally",
            "estimated_monthly_searches": "1k-10k"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        target_keywords = ["target keyword", "specific phrase"]
        seo_data = self.research_agent.analyze_seo_keywords(
            "Test Topic",
            target_keywords=target_keywords
        )
        
        # Verify target keywords were included in prompt
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args[1]['messages'][0]['content']
        self.assertIn("target keyword", prompt)
        self.assertIn("specific phrase", prompt)
    
    def test_analyze_seo_keywords_fallback(self):
        """Test fallback keyword generation when API fails."""
        topic = "Machine Learning Applications"
        keywords = self.research_agent._generate_fallback_keywords(topic)
        
        self.assertIn("primary_keywords", keywords)
        self.assertIn("secondary_keywords", keywords)
        self.assertIn("long_tail_keywords", keywords)
        self.assertIn("search_intent", keywords)
        self.assertIn("content_recommendations", keywords)
        self.assertIn("analyzed_at", keywords)
        self.assertIn("topic", keywords)
        
        self.assertGreater(len(keywords["long_tail_keywords"]), 0)
        self.assertEqual(keywords["topic"], topic)
    
    @patch('agents.research_agent.OpenAI')
    def test_generate_research_summary(self, mock_openai):
        """Test complete research summary generation."""
        # Mock responses for both trending topics and SEO analysis
        topic_response = Mock()
        topic_response.choices = [Mock()]
        topic_response.choices[0].message.content = json.dumps([
            {
                "topic": "AI in Healthcare",
                "rationale": "Healthcare is being transformed by AI",
                "trend_score": 9
            }
        ])
        
        seo_response = Mock()
        seo_response.choices = [Mock()]
        seo_response.choices[0].message.content = json.dumps({
            "primary_keywords": ["AI healthcare", "medical AI"],
            "secondary_keywords": ["diagnosis AI", "healthcare technology"],
            "long_tail_keywords": ["AI in medical diagnosis"],
            "search_intent": "informational",
            "content_recommendations": "Focus on patient outcomes",
            "estimated_monthly_searches": "10k-100k"
        })
        
        mock_client = Mock()
        # First call returns topics, second call returns SEO data
        mock_client.chat.completions.create.side_effect = [topic_response, seo_response]
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        summary = self.research_agent.generate_research_summary(topic_count=1)
        
        self.assertIn("research_date", summary)
        self.assertIn("topic_count", summary)
        self.assertIn("base_topics", summary)
        self.assertIn("research_results", summary)
        self.assertIn("agent_version", summary)
        self.assertIn("status", summary)
        
        self.assertEqual(summary["status"], "success")
        self.assertEqual(len(summary["research_results"]), 1)
        
        result = summary["research_results"][0]
        self.assertEqual(result["topic"], "AI in Healthcare")
        self.assertEqual(result["trend_score"], 9)
        self.assertIn("seo_keywords", result)
        self.assertIn("primary", result["seo_keywords"])
        self.assertIn("secondary", result["seo_keywords"])
        self.assertIn("long_tail", result["seo_keywords"])
        self.assertIn("search_intent", result)
        self.assertIn("content_recommendations", result)
    
    @patch('agents.research_agent.OpenAI')
    def test_generate_research_summary_multiple_topics(self, mock_openai):
        """Test research summary with multiple topics."""
        # Mock trending topics response
        topic_response = Mock()
        topic_response.choices = [Mock()]
        topic_response.choices[0].message.content = json.dumps([
            {
                "topic": "Topic 1",
                "rationale": "Rationale 1",
                "trend_score": 8
            },
            {
                "topic": "Topic 2",
                "rationale": "Rationale 2",
                "trend_score": 7
            }
        ])
        
        # Mock SEO responses
        seo_response_1 = Mock()
        seo_response_1.choices = [Mock()]
        seo_response_1.choices[0].message.content = json.dumps({
            "primary_keywords": ["keyword1"],
            "secondary_keywords": ["keyword2"],
            "long_tail_keywords": ["long tail 1"],
            "search_intent": "informational",
            "content_recommendations": "Tips 1",
            "estimated_monthly_searches": "1k-10k"
        })
        
        seo_response_2 = Mock()
        seo_response_2.choices = [Mock()]
        seo_response_2.choices[0].message.content = json.dumps({
            "primary_keywords": ["keyword3"],
            "secondary_keywords": ["keyword4"],
            "long_tail_keywords": ["long tail 2"],
            "search_intent": "informational",
            "content_recommendations": "Tips 2",
            "estimated_monthly_searches": "10k-100k"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [
            topic_response,
            seo_response_1,
            seo_response_2
        ]
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        summary = self.research_agent.generate_research_summary(topic_count=2)
        
        self.assertEqual(summary["topic_count"], 2)
        self.assertEqual(len(summary["research_results"]), 2)
        self.assertEqual(summary["research_results"][0]["topic"], "Topic 1")
        self.assertEqual(summary["research_results"][1]["topic"], "Topic 2")
    
    @patch('agents.research_agent.OpenAI')
    def test_get_top_topic_with_seo(self, mock_openai):
        """Test getting single top topic with SEO."""
        # Mock responses
        topic_response = Mock()
        topic_response.choices = [Mock()]
        topic_response.choices[0].message.content = json.dumps([
            {
                "topic": "Best Topic",
                "rationale": "This is the best topic",
                "trend_score": 10
            }
        ])
        
        seo_response = Mock()
        seo_response.choices = [Mock()]
        seo_response.choices[0].message.content = json.dumps({
            "primary_keywords": ["best", "topic"],
            "secondary_keywords": ["excellent"],
            "long_tail_keywords": ["best topic ever"],
            "search_intent": "informational",
            "content_recommendations": "Write well",
            "estimated_monthly_searches": "100k+"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [topic_response, seo_response]
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        top_topic = self.research_agent.get_top_topic_with_seo()
        
        self.assertEqual(top_topic["topic"], "Best Topic")
        self.assertEqual(top_topic["trend_score"], 10)
        self.assertIn("seo_keywords", top_topic)
        self.assertIn("search_intent", top_topic)
    
    @patch('agents.research_agent.OpenAI')
    def test_research_agent_error_handling(self, mock_openai):
        """Test error handling in research agent."""
        # Mock client that raises an exception
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        # Should fall back to template generation
        topics = self.research_agent.discover_trending_topics(count=2)
        
        # Should get fallback topics
        self.assertEqual(len(topics), 2)
        self.assertEqual(topics[0]["source"], "fallback_generation")
    
    @patch('agents.research_agent.OpenAI')
    def test_research_summary_with_custom_topics(self, mock_openai):
        """Test research summary with custom base topics."""
        topic_response = Mock()
        topic_response.choices = [Mock()]
        topic_response.choices[0].message.content = json.dumps([
            {
                "topic": "Custom Topic",
                "rationale": "Custom rationale",
                "trend_score": 8
            }
        ])
        
        seo_response = Mock()
        seo_response.choices = [Mock()]
        seo_response.choices[0].message.content = json.dumps({
            "primary_keywords": ["custom"],
            "secondary_keywords": ["topic"],
            "long_tail_keywords": ["custom long tail"],
            "search_intent": "informational",
            "content_recommendations": "Custom tips",
            "estimated_monthly_searches": "1k-10k"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [topic_response, seo_response]
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        custom_topics = ["custom1", "custom2"]
        summary = self.research_agent.generate_research_summary(
            topic_count=1,
            base_topics=custom_topics
        )
        
        self.assertEqual(summary["base_topics"], custom_topics)
    
    def test_fallback_keywords_with_short_topic(self):
        """Test fallback keyword generation with short topic."""
        topic = "AI"
        keywords = self.research_agent._generate_fallback_keywords(topic)
        
        # Should still generate reasonable keywords
        self.assertGreater(len(keywords["secondary_keywords"]), 0)
        self.assertGreater(len(keywords["long_tail_keywords"]), 0)
    
    def test_fallback_topics_with_multiple_topics(self):
        """Test fallback generation with multiple base topics."""
        base_topics = ["AI", "blockchain", "IoT", "quantum computing"]
        topics = self.research_agent._generate_fallback_topics(base_topics, count=5)
        
        self.assertEqual(len(topics), 4)  # Limited by base_topics length
        
        # Should use different base topics
        topic_texts = [t["topic"] for t in topics]
        self.assertGreater(len(set(topic_texts)), 1)  # Not all the same


class TestResearchAgentIntegration(unittest.TestCase):
    """Integration tests for Research Agent."""
    
    def setUp(self):
        """Set up test environment."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication',
            'CONTENT_TOPICS': 'AI,technology,innovation'
        }):
            self.research_agent = ResearchAgent()
    
    def test_agent_initialization(self):
        """Test that agent initializes properly."""
        self.assertIsNotNone(self.research_agent)
        self.assertIsNotNone(self.research_agent.client)
        self.assertEqual(self.research_agent.model, "gpt-4")
    
    @patch('agents.research_agent.OpenAI')
    def test_full_workflow(self, mock_openai):
        """Test a complete research workflow."""
        # Mock all necessary responses
        topic_response = Mock()
        topic_response.choices = [Mock()]
        topic_response.choices[0].message.content = json.dumps([
            {
                "topic": "Workflow Topic",
                "rationale": "Great for testing",
                "trend_score": 9
            }
        ])
        
        seo_response = Mock()
        seo_response.choices = [Mock()]
        seo_response.choices[0].message.content = json.dumps({
            "primary_keywords": ["workflow", "test"],
            "secondary_keywords": ["integration"],
            "long_tail_keywords": ["workflow integration test"],
            "search_intent": "informational",
            "content_recommendations": "Test thoroughly",
            "estimated_monthly_searches": "1k-10k"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [topic_response, seo_response]
        mock_openai.return_value = mock_client
        
        self.research_agent.client = mock_client
        
        # Generate research summary
        summary = self.research_agent.generate_research_summary(topic_count=1)
        
        # Verify complete workflow
        self.assertEqual(summary["status"], "success")
        self.assertEqual(len(summary["research_results"]), 1)
        
        result = summary["research_results"][0]
        self.assertIn("topic", result)
        self.assertIn("seo_keywords", result)
        self.assertIn("search_intent", result)
        self.assertIn("content_recommendations", result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
