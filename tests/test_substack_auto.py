"""
Test suite for the automated Substack content generation system.
"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.settings import Settings
from content_generators.text_generator import TextGenerator
from content_generators.image_generator import ImageGenerator
from content_generators.video_generator import VideoGenerator
from publishers.substack_publisher import SubstackPublisher
from main import ContentOrchestrator


class TestSettings(unittest.TestCase):
    """Test configuration settings."""
    
    def test_settings_initialization(self):
        """Test that settings can be initialized with defaults."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        }):
            settings = Settings()
            self.assertEqual(settings.openai_api_key, 'test_key')
            self.assertEqual(settings.substack_email, 'test@example.com')
            self.assertEqual(settings.max_posts_per_day, 3)
    
    def test_topics_list_property(self):
        """Test that topics list is properly parsed."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication',
            'CONTENT_TOPICS': 'AI,technology,science'
        }):
            settings = Settings()
            topics = settings.topics_list
            self.assertEqual(topics, ['AI', 'technology', 'science'])


class TestTextGenerator(unittest.TestCase):
    """Test text generation functionality."""
    
    def setUp(self):
        """Set up test environment."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        }):
            self.text_generator = TextGenerator()
    
    @patch('content_generators.text_generator.OpenAI')
    def test_generate_topic(self, mock_openai):
        """Test topic generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "The Future of Artificial Intelligence"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.text_generator.client = mock_client
        
        topic = self.text_generator.generate_topic()
        self.assertEqual(topic, "The Future of Artificial Intelligence")
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('content_generators.text_generator.OpenAI')
    def test_generate_blog_post(self, mock_openai):
        """Test blog post generation."""
        # Mock OpenAI responses
        mock_content_response = Mock()
        mock_content_response.choices = [Mock()]
        mock_content_response.choices[0].message.content = "This is a test blog post content."
        
        mock_subtitle_response = Mock()
        mock_subtitle_response.choices = [Mock()]
        mock_subtitle_response.choices[0].message.content = "A test subtitle"
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [mock_content_response, mock_subtitle_response]
        mock_openai.return_value = mock_client
        
        self.text_generator.client = mock_client
        
        post = self.text_generator.generate_blog_post("Test Topic")
        
        self.assertEqual(post["title"], "Test Topic")
        self.assertEqual(post["subtitle"], "A test subtitle")
        self.assertEqual(post["content"], "This is a test blog post content.")
        self.assertIn("word_count", post)


class TestImageGenerator(unittest.TestCase):
    """Test image generation functionality."""
    
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
            self.image_generator = ImageGenerator()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_create_image_prompt(self):
        """Test image prompt creation."""
        prompt = self.image_generator._create_image_prompt(
            "Test Title",
            "Test content about AI and technology"
        )
        self.assertIn("Test Title", prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 50)
    
    @patch('content_generators.image_generator.requests.get')
    @patch('content_generators.image_generator.OpenAI')
    def test_generate_image(self, mock_openai, mock_requests):
        """Test image generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/test_image.png"
        
        mock_client = Mock()
        mock_client.images.generate.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Mock image download
        mock_requests.return_value.content = b"fake_image_data"
        mock_requests.return_value.raise_for_status = Mock()
        
        self.image_generator.client = mock_client
        
        image_path = self.image_generator.generate_image("Test Title", "Test content")
        
        self.assertIsNotNone(image_path)
        self.assertTrue(image_path.endswith('.png'))
        mock_client.images.generate.assert_called_once()


class TestVideoGenerator(unittest.TestCase):
    """Test video generation functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        
        with patch.dict(os.environ, {
            'OUTPUT_DIR': self.temp_dir,
            'VIDEO_DURATION': '30'
        }):
            self.video_generator = VideoGenerator()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_create_title_slide(self):
        """Test title slide creation."""
        slide_path = self.video_generator.create_title_slide(
            "Test Title",
            "Test Subtitle"
        )
        
        self.assertIsNotNone(slide_path)
        self.assertTrue(os.path.exists(slide_path))
        self.assertTrue(slide_path.endswith('.png'))
    
    def test_create_content_slides(self):
        """Test content slide creation."""
        content = "This is a test sentence. This is another test sentence. And this is a third test sentence for testing purposes."
        
        slides = self.video_generator.create_content_slides(content, num_slides=2)
        
        self.assertEqual(len(slides), 2)
        for slide in slides:
            self.assertTrue(os.path.exists(slide))


class TestSubstackPublisher(unittest.TestCase):
    """Test Substack publishing functionality."""
    
    def setUp(self):
        """Set up test environment."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        }):
            self.publisher = SubstackPublisher()
    
    def test_validate_content(self):
        """Test content validation."""
        # Valid content
        valid_post = {
            "title": "Test Title",
            "content": "This is a test content that is long enough to pass validation checks.",
            "ai_generated": True
        }
        
        result = self.publisher.validate_content(valid_post)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)
        
        # Invalid content
        invalid_post = {
            "title": "",
            "content": "",
            "ai_generated": False
        }
        
        result = self.publisher.validate_content(invalid_post)
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["errors"]), 0)
    
    def test_authentication(self):
        """Test authentication process."""
        # Since we're using simulated auth for demo purposes
        result = self.publisher.authenticate()
        self.assertTrue(result)
        self.assertTrue(self.publisher._authenticated)


class TestContentOrchestrator(unittest.TestCase):
    """Test the main content orchestrator."""
    
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
            self.orchestrator = ContentOrchestrator()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_get_status(self):
        """Test status reporting."""
        status = self.orchestrator.get_status()
        
        self.assertIn("posts_today", status)
        self.assertIn("max_posts_per_day", status)
        self.assertIn("system_status", status)
        self.assertEqual(status["system_status"], "operational")
    
    @patch('main.TextGenerator.create_complete_post')
    @patch('main.ImageGenerator.generate_featured_image')
    @patch('main.VideoGenerator.generate_blog_video')
    def test_generate_complete_content(self, mock_video, mock_image, mock_text):
        """Test complete content generation."""
        # Mock responses
        mock_text.return_value = {
            "title": "Test Post",
            "content": "Test content",
            "word_count": 100,
            "ai_generated": True
        }
        
        mock_image.return_value = {
            "image_path": "/fake/path/image.png",
            "thumbnail_path": "/fake/path/thumb.png"
        }
        
        mock_video.return_value = {
            "video_path": "/fake/path/video.mp4",
            "duration": 30,
            "slides_created": 3
        }
        
        content = self.orchestrator.generate_complete_content()
        
        self.assertIn("post_data", content)
        self.assertIn("media_files", content)
        self.assertIn("generation_stats", content)
        self.assertTrue(content["ai_generated"])


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_environment_setup(self):
        """Test that required environment variables are handled properly."""
        required_vars = [
            'OPENAI_API_KEY',
            'SUBSTACK_EMAIL',
            'SUBSTACK_PASSWORD',
            'SUBSTACK_PUBLICATION'
        ]
        
        # Test with missing variables
        for var in required_vars:
            with patch.dict(os.environ, {v: 'test_value' for v in required_vars if v != var}, clear=True):
                with self.assertRaises(Exception):
                    Settings()
    
    def test_output_directory_creation(self):
        """Test that output directories are created properly."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication',
            'OUTPUT_DIR': self.temp_dir
        }):
            orchestrator = ContentOrchestrator()
            self.assertTrue(os.path.exists(self.temp_dir))


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)