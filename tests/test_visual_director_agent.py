"""
Test suite for the Visual Director Agent.
"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.visual_director_agent import VisualDirectorAgent


class TestVisualDirectorAgent(unittest.TestCase):
    """Test the Visual Director Agent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication',
            'OUTPUT_DIR': self.temp_dir
        }):
            self.agent = VisualDirectorAgent()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test agent initialization."""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.client)
        self.assertIsNotNone(self.agent.image_generator)
        # Output dir should be set to temp_dir from environment
        self.assertTrue(os.path.exists(self.agent.output_dir))
    
    @patch('agents.visual_director_agent.OpenAI')
    def test_analyze_seo_metadata(self, mock_openai):
        """Test SEO metadata analysis."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        KEYWORDS: AI, machine learning, automation, neural networks, technology
        THEME: The future of artificial intelligence in modern society
        MOOD: innovative
        STYLE: modern
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        metadata = self.agent.analyze_seo_metadata(
            title="The Future of AI",
            content="Artificial intelligence is transforming our world...",
            tags=["AI", "technology"]
        )
        
        self.assertIn("keywords", metadata)
        self.assertIn("theme", metadata)
        self.assertIn("mood", metadata)
        self.assertIn("style", metadata)
        self.assertEqual(metadata["title"], "The Future of AI")
        self.assertGreater(len(metadata["keywords"]), 0)
    
    def test_parse_seo_analysis(self):
        """Test parsing of SEO analysis response."""
        analysis_text = """
        KEYWORDS: AI, machine learning, automation, neural networks, technology
        THEME: The future of artificial intelligence in modern society
        MOOD: innovative
        STYLE: modern
        """
        
        metadata = self.agent._parse_seo_analysis(analysis_text)
        
        self.assertEqual(len(metadata["keywords"]), 5)
        self.assertIn("AI", metadata["keywords"])
        self.assertIn("machine learning", metadata["keywords"])
        self.assertEqual(metadata["theme"], "The future of artificial intelligence in modern society")
        self.assertEqual(metadata["mood"], "innovative")
        self.assertEqual(metadata["style"], "modern")
    
    def test_generate_seo_friendly_filename(self):
        """Test SEO-friendly filename generation."""
        filename = self.agent.generate_seo_friendly_filename(
            title="The Future of Artificial Intelligence",
            keywords=["AI", "machine learning", "innovation"]
        )
        
        # Check that filename is lowercase
        self.assertEqual(filename, filename.lower())
        
        # Check that spaces are replaced with hyphens
        self.assertNotIn(' ', filename)
        self.assertIn('-', filename)
        
        # Check that title words are included
        self.assertIn('future', filename)
        self.assertIn('artificial', filename)
        self.assertIn('intelligence', filename)
        
        # Check length limitation
        self.assertLessEqual(len(filename), 80)
        
        # Check no special characters
        self.assertTrue(all(c.isalnum() or c == '-' for c in filename))
    
    def test_generate_seo_friendly_filename_with_special_chars(self):
        """Test filename generation with special characters."""
        filename = self.agent.generate_seo_friendly_filename(
            title="AI & Machine Learning: The Future!",
            keywords=["AI", "ML", "tech"]
        )
        
        # Special characters should be removed
        self.assertNotIn('&', filename)
        self.assertNotIn(':', filename)
        self.assertNotIn('!', filename)
        
        # Should still be readable
        self.assertIn('ai', filename)
        self.assertIn('machine', filename)
        self.assertIn('learning', filename)
    
    @patch('agents.visual_director_agent.OpenAI')
    def test_generate_alt_text(self, mock_openai):
        """Test alt text generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "AI-powered automation transforming modern workflow and productivity"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        seo_metadata = {
            "keywords": ["AI", "automation", "productivity"],
            "theme": "AI in the workplace"
        }
        
        alt_text = self.agent.generate_alt_text(
            title="The Future of AI at Work",
            seo_metadata=seo_metadata
        )
        
        self.assertIsNotNone(alt_text)
        self.assertGreater(len(alt_text), 20)
        self.assertIsInstance(alt_text, str)
        # Check that quotes are removed
        self.assertNotIn('"', alt_text)
        self.assertNotIn("'", alt_text)
    
    @patch('agents.visual_director_agent.OpenAI')
    def test_generate_caption(self, mock_openai):
        """Test caption generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Exploring the transformative potential of AI in modern workplace."
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        seo_metadata = {
            "theme": "AI in the workplace",
            "mood": "innovative"
        }
        
        caption = self.agent.generate_caption(
            title="The Future of AI at Work",
            seo_metadata=seo_metadata
        )
        
        self.assertIsNotNone(caption)
        self.assertGreater(len(caption), 10)
        self.assertIsInstance(caption, str)
    
    def test_create_seo_optimized_prompt(self):
        """Test SEO-optimized prompt creation."""
        seo_metadata = {
            "keywords": ["AI", "machine learning", "automation"],
            "theme": "The future of AI in business",
            "mood": "innovative",
            "style": "modern"
        }
        
        prompt = self.agent.create_seo_optimized_prompt(
            title="AI in Business",
            content="Long form content...",
            seo_metadata=seo_metadata
        )
        
        self.assertIsNotNone(prompt)
        self.assertIn("AI in Business", prompt)
        self.assertIn("AI", prompt)
        self.assertGreater(len(prompt), 100)
    
    @patch('agents.visual_director_agent.requests.get')
    @patch('agents.visual_director_agent.OpenAI')
    def test_generate_seo_optimized_image(self, mock_openai, mock_requests):
        """Test complete SEO-optimized image generation."""
        # Mock SEO analysis
        mock_analysis_response = Mock()
        mock_analysis_response.choices = [Mock()]
        mock_analysis_response.choices[0].message.content = """
        KEYWORDS: AI, automation, technology, innovation, future
        THEME: The transformative impact of AI on modern society
        MOOD: innovative
        STYLE: modern
        """
        
        # Mock image generation
        mock_image_response = Mock()
        mock_image_response.data = [Mock()]
        mock_image_response.data[0].url = "https://example.com/test_image.png"
        
        # Mock alt text generation
        mock_alt_response = Mock()
        mock_alt_response.choices = [Mock()]
        mock_alt_response.choices[0].message.content = "AI technology transforming modern business workflows"
        
        # Mock caption generation
        mock_caption_response = Mock()
        mock_caption_response.choices = [Mock()]
        mock_caption_response.choices[0].message.content = "Exploring AI's revolutionary impact on business."
        
        mock_client = Mock()
        # Set up side effects for multiple calls
        mock_client.chat.completions.create.side_effect = [
            mock_analysis_response,
            mock_alt_response,
            mock_caption_response
        ]
        mock_client.images.generate.return_value = mock_image_response
        mock_openai.return_value = mock_client
        
        # Mock image download
        mock_requests.return_value.content = b"fake_image_data"
        mock_requests.return_value.raise_for_status = Mock()
        
        self.agent.client = mock_client
        self.agent.image_generator.client = mock_client
        
        result = self.agent.generate_seo_optimized_image(
            title="The Future of AI",
            content="Artificial intelligence is changing everything...",
            tags=["AI", "technology"]
        )
        
        # Verify result structure
        self.assertIn("image_path", result)
        self.assertIn("filename", result)
        self.assertIn("alt_text", result)
        self.assertIn("caption", result)
        self.assertIn("seo_metadata", result)
        self.assertIn("keywords", result)
        self.assertTrue(result["ai_generated"])
        
        # Verify filename is SEO-friendly
        self.assertTrue(result["filename"].endswith('.png'))
        self.assertEqual(result["filename"], result["filename"].lower())
        
        # Verify file was created
        self.assertTrue(os.path.exists(result["image_path"]))
    
    @patch('agents.visual_director_agent.requests.get')
    @patch('agents.visual_director_agent.OpenAI')
    def test_generate_featured_image_with_seo(self, mock_openai, mock_requests):
        """Test featured image generation with SEO."""
        # Mock responses
        mock_analysis_response = Mock()
        mock_analysis_response.choices = [Mock()]
        mock_analysis_response.choices[0].message.content = """
        KEYWORDS: AI, technology, innovation, future, automation
        THEME: AI's impact on society
        MOOD: innovative
        STYLE: modern
        """
        
        mock_image_response = Mock()
        mock_image_response.data = [Mock()]
        mock_image_response.data[0].url = "https://example.com/test_image.png"
        
        mock_alt_response = Mock()
        mock_alt_response.choices = [Mock()]
        mock_alt_response.choices[0].message.content = "AI technology in action"
        
        mock_caption_response = Mock()
        mock_caption_response.choices = [Mock()]
        mock_caption_response.choices[0].message.content = "The future of AI is here."
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [
            mock_analysis_response,
            mock_alt_response,
            mock_caption_response
        ]
        mock_client.images.generate.return_value = mock_image_response
        mock_openai.return_value = mock_client
        
        # Mock image download
        mock_requests.return_value.content = b"fake_image_data"
        mock_requests.return_value.raise_for_status = Mock()
        
        self.agent.client = mock_client
        self.agent.image_generator.client = mock_client
        
        post_data = {
            "title": "The Future of AI",
            "content": "AI is transforming everything...",
            "tags": ["AI", "technology"]
        }
        
        result = self.agent.generate_featured_image_with_seo(post_data)
        
        # Verify result includes thumbnail
        self.assertIn("thumbnail_path", result)
        self.assertIn("image_path", result)
        self.assertIn("alt_text", result)
        self.assertIn("caption", result)
    
    def test_analyze_seo_metadata_fallback(self):
        """Test SEO analysis fallback on error."""
        # Cause an error by not mocking OpenAI
        with patch('agents.visual_director_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = mock_client
            self.agent.client = mock_client
            
            metadata = self.agent.analyze_seo_metadata(
                title="Test Title",
                content="Test content"
            )
            
            # Should return fallback metadata
            self.assertIn("title", metadata)
            self.assertIn("keywords", metadata)
            self.assertEqual(metadata["title"], "Test Title")
    
    def test_generate_alt_text_fallback(self):
        """Test alt text generation fallback on error."""
        with patch('agents.visual_director_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = mock_client
            self.agent.client = mock_client
            
            seo_metadata = {
                "theme": "Test theme",
                "keywords": []
            }
            
            alt_text = self.agent.generate_alt_text(
                title="Test Title",
                seo_metadata=seo_metadata
            )
            
            # Should return fallback alt text
            self.assertIsNotNone(alt_text)
            self.assertIn("Test Title", alt_text)
    
    def test_generate_caption_fallback(self):
        """Test caption generation fallback on error."""
        with patch('agents.visual_director_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = mock_client
            self.agent.client = mock_client
            
            seo_metadata = {"theme": "Test theme"}
            
            caption = self.agent.generate_caption(
                title="Test Title",
                seo_metadata=seo_metadata
            )
            
            # Should return fallback caption
            self.assertIsNotNone(caption)
            self.assertIn("Test Title", caption)
    
    def test_filename_length_limit(self):
        """Test that filenames are properly limited in length."""
        long_title = "This is an extremely long title that should be truncated to meet the filename length requirements and not cause any issues"
        long_keywords = ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
        
        filename = self.agent.generate_seo_friendly_filename(
            title=long_title,
            keywords=long_keywords
        )
        
        # Should be truncated to 80 characters
        self.assertLessEqual(len(filename), 80)
        
        # Should still be valid
        self.assertTrue(all(c.isalnum() or c == '-' for c in filename))
    
    def test_keywords_included_in_filename(self):
        """Test that keywords are included in filename."""
        filename = self.agent.generate_seo_friendly_filename(
            title="Article Title",
            keywords=["seo", "optimization", "testing"]
        )
        
        # Check that at least some keywords are included
        self.assertIn('seo', filename)
        self.assertIn('optimization', filename)


if __name__ == '__main__':
    unittest.main(verbosity=2)
