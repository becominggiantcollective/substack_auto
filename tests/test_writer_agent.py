"""
Test suite for the Writer Agent.
"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.writer_agent import WriterAgent


class TestWriterAgent(unittest.TestCase):
    """Test the Writer Agent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        }):
            self.writer = WriterAgent(openai_api_key='test_key')
    
    def test_initialization(self):
        """Test that Writer Agent initializes correctly."""
        self.assertIsNotNone(self.writer.client)
        self.assertEqual(self.writer.model, "gpt-4")
        self.assertEqual(self.writer.target_word_count_min, 800)
        self.assertEqual(self.writer.target_word_count_max, 1200)
        self.assertEqual(self.writer.target_keyword_density, 0.02)
    
    def test_calculate_keyword_density(self):
        """Test keyword density calculation."""
        content = "AI and machine learning are transforming technology. " * 20  # ~200 words
        content += "The future of AI is bright with machine learning advances."
        
        keywords = ["AI", "machine learning", "technology"]
        densities = self.writer.calculate_keyword_density(content, keywords)
        
        self.assertIn("AI", densities)
        self.assertIn("machine learning", densities)
        self.assertIn("technology", densities)
        
        # AI appears more frequently so should have higher density
        self.assertGreater(densities["AI"], 0)
        self.assertGreater(densities["machine learning"], 0)
    
    def test_calculate_keyword_density_empty_content(self):
        """Test keyword density calculation with empty content."""
        densities = self.writer.calculate_keyword_density("", ["test", "keywords"])
        self.assertEqual(densities["test"], 0.0)
        self.assertEqual(densities["keywords"], 0.0)
    
    def test_validate_content_structure(self):
        """Test content structure validation."""
        # Good content structure
        good_content = """
This is an opening paragraph with more than thirty words to meet the minimum requirement for a proper opening section that clearly engages readers effectively and provides very valuable information.

This is a second paragraph that adds more detail and information.

This is a third paragraph continuing the discussion.

More content here in a fourth paragraph.

And a final fifth paragraph to conclude.
        """.strip()
        
        validation = self.writer.validate_content_structure(good_content)
        
        self.assertTrue(validation["has_paragraphs"])
        self.assertTrue(validation["has_opening"])
        self.assertTrue(validation["has_sections"])
    
    def test_validate_content_structure_insufficient(self):
        """Test content structure validation with insufficient content."""
        poor_content = "Short content."
        
        validation = self.writer.validate_content_structure(poor_content)
        
        self.assertFalse(validation["has_paragraphs"])
        self.assertFalse(validation["has_sufficient_length"])
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_article(self, mock_openai):
        """Test article generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_message = Mock()
        mock_message.content = " ".join(["Test article content."] * 150)  # ~450 words
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        writer = WriterAgent(openai_api_key='test_key')
        writer.client = mock_client
        
        result = writer.generate_article(
            topic="The Future of AI",
            keywords=["AI", "machine learning", "technology"],
            research_summary="AI is advancing rapidly with new developments in machine learning."
        )
        
        self.assertIn("article", result)
        self.assertIn("word_count", result)
        self.assertIn("keyword_densities", result)
        self.assertIn("structure_validation", result)
        self.assertGreater(result["word_count"], 0)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_meta_title(self, mock_openai):
        """Test meta title generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_message = Mock()
        mock_message.content = "AI Revolution: The Future of Technology"
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        writer = WriterAgent(openai_api_key='test_key')
        writer.client = mock_client
        
        meta_title = writer.generate_meta_title(
            topic="The Future of AI",
            keywords=["AI", "technology", "innovation"]
        )
        
        self.assertIsInstance(meta_title, str)
        self.assertLessEqual(len(meta_title), 60)
        self.assertGreater(len(meta_title), 0)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_meta_title_truncation(self, mock_openai):
        """Test meta title truncation for long titles."""
        # Mock OpenAI response with very long title
        mock_response = Mock()
        mock_message = Mock()
        mock_message.content = "A" * 100  # Very long title
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        writer = WriterAgent(openai_api_key='test_key')
        writer.client = mock_client
        
        meta_title = writer.generate_meta_title(
            topic="Test Topic",
            keywords=["test"]
        )
        
        self.assertLessEqual(len(meta_title), 60)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_meta_description(self, mock_openai):
        """Test meta description generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_message = Mock()
        mock_message.content = "Discover how AI is transforming technology and what it means for the future."
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        writer = WriterAgent(openai_api_key='test_key')
        writer.client = mock_client
        
        meta_desc = writer.generate_meta_description(
            topic="The Future of AI",
            keywords=["AI", "technology"],
            article_preview="AI is advancing rapidly..." * 50
        )
        
        self.assertIsInstance(meta_desc, str)
        self.assertLessEqual(len(meta_desc), 155)
        self.assertGreater(len(meta_desc), 0)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_tags(self, mock_openai):
        """Test tag generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_message = Mock()
        mock_message.content = "AI, machine learning, technology, innovation, future tech"
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        writer = WriterAgent(openai_api_key='test_key')
        writer.client = mock_client
        
        tags = writer.generate_tags(
            topic="The Future of AI",
            keywords=["AI", "technology"],
            article="Article content about AI and technology..."
        )
        
        self.assertIsInstance(tags, list)
        self.assertLessEqual(len(tags), 8)
        self.assertGreater(len(tags), 0)
    
    @patch('agents.writer_agent.OpenAI')
    def test_create_complete_content(self, mock_openai):
        """Test complete content generation."""
        # Mock OpenAI responses for all calls
        article_content = " ".join(["Test article about AI."] * 150)  # ~450 words
        
        def create_side_effect(*args, **kwargs):
            mock_response = Mock()
            mock_message = Mock()
            mock_choice = Mock()
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            
            # Check max_tokens to determine which call this is
            max_tokens = kwargs.get('max_tokens', 1800)
            if max_tokens >= 1800:  # Article generation
                mock_message.content = article_content
            elif max_tokens <= 50:  # Meta title
                mock_message.content = "AI Revolution: The Future"
            elif max_tokens == 100:  # Could be meta description or tags
                messages = kwargs.get('messages', [{}])
                if messages and 'meta description' in messages[0].get('content', '').lower():
                    mock_message.content = "Discover the future of AI and technology."
                else:  # Tags
                    mock_message.content = "AI, technology, innovation"
            
            return mock_response
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = create_side_effect
        mock_openai.return_value = mock_client
        
        writer = WriterAgent(openai_api_key='test_key')
        writer.client = mock_client
        
        result = writer.create_complete_content(
            topic="The Future of AI",
            keywords=["AI", "machine learning", "technology"],
            research_summary="AI is advancing rapidly with new developments."
        )
        
        # Verify all required fields are present
        self.assertIn("title", result)
        self.assertIn("article", result)
        self.assertIn("meta_title", result)
        self.assertIn("meta_description", result)
        self.assertIn("tags", result)
        self.assertIn("word_count", result)
        self.assertIn("keyword_densities", result)
        self.assertIn("structure_validation", result)
        self.assertIn("seo_score", result)
        self.assertIn("ai_generated", result)
        
        # Verify types
        self.assertIsInstance(result["title"], str)
        self.assertIsInstance(result["article"], str)
        self.assertIsInstance(result["meta_title"], str)
        self.assertIsInstance(result["meta_description"], str)
        self.assertIsInstance(result["tags"], list)
        self.assertIsInstance(result["word_count"], int)
        self.assertIsInstance(result["keyword_densities"], dict)
        self.assertIsInstance(result["structure_validation"], dict)
        self.assertIsInstance(result["seo_score"], int)
        self.assertTrue(result["ai_generated"])
        
        # Verify SEO score is in valid range
        self.assertGreaterEqual(result["seo_score"], 0)
        self.assertLessEqual(result["seo_score"], 100)
    
    def test_calculate_seo_score_perfect(self):
        """Test SEO score calculation with perfect metrics."""
        keyword_densities = {
            "AI": 0.02,
            "technology": 0.02,
            "innovation": 0.02
        }
        structure_validation = {
            "has_paragraphs": True,
            "has_sufficient_length": True,
            "has_opening": True,
            "has_sections": True
        }
        word_count = 1000
        
        score = self.writer._calculate_seo_score(
            keyword_densities,
            structure_validation,
            word_count
        )
        
        # Should be close to 100 with perfect metrics
        self.assertGreaterEqual(score, 90)
        self.assertLessEqual(score, 100)
    
    def test_calculate_seo_score_poor(self):
        """Test SEO score calculation with poor metrics."""
        keyword_densities = {}
        structure_validation = {
            "has_paragraphs": False,
            "has_sufficient_length": False,
            "has_opening": False,
            "has_sections": False
        }
        word_count = 100  # Too short
        
        score = self.writer._calculate_seo_score(
            keyword_densities,
            structure_validation,
            word_count
        )
        
        # Should be low with poor metrics
        self.assertLess(score, 50)
    
    def test_calculate_seo_score_moderate(self):
        """Test SEO score calculation with moderate metrics."""
        keyword_densities = {
            "AI": 0.01,  # Slightly low density
            "technology": 0.015
        }
        structure_validation = {
            "has_paragraphs": True,
            "has_sufficient_length": True,
            "has_opening": False,
            "has_sections": True
        }
        word_count = 850  # In range but not centered
        
        score = self.writer._calculate_seo_score(
            keyword_densities,
            structure_validation,
            word_count
        )
        
        # Should be moderate
        self.assertGreaterEqual(score, 50)
        self.assertLess(score, 90)


if __name__ == '__main__':
    unittest.main()
