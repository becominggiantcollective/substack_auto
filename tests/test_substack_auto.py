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
from agents.writer_agent import WriterAgent


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
    
    def test_content_shaping_settings(self):
        """Test that content shaping settings are properly loaded."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication',
            'CONTENT_TONE': 'casual and friendly',
            'TARGET_AUDIENCE': 'developers and tech enthusiasts',
            'CONTENT_STYLE': 'practical and actionable',
            'CUSTOM_INSTRUCTIONS': 'Always include code examples where relevant'
        }):
            settings = Settings()
            self.assertEqual(settings.content_tone, 'casual and friendly')
            self.assertEqual(settings.target_audience, 'developers and tech enthusiasts')
            self.assertEqual(settings.content_style, 'practical and actionable')
            self.assertEqual(settings.custom_instructions, 'Always include code examples where relevant')


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
    
    @patch('content_generators.text_generator.OpenAI')
    def test_generate_topic_with_custom_instructions(self, mock_openai):
        """Test topic generation incorporates custom instructions."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Custom AI Topic"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Test with custom settings
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication',
            'CONTENT_TONE': 'casual and humorous',
            'TARGET_AUDIENCE': 'beginner developers',
            'CUSTOM_INSTRUCTIONS': 'Include practical examples'
        }):
            # Patch the settings to use the new environment variables
            with patch('content_generators.text_generator.settings') as mock_settings:
                from config.settings import Settings
                test_settings = Settings()
                mock_settings.topics_list = test_settings.topics_list
                mock_settings.content_tone = test_settings.content_tone
                mock_settings.target_audience = test_settings.target_audience
                mock_settings.custom_instructions = test_settings.custom_instructions
                
                # Reinitialize text generator with custom settings
                from content_generators.text_generator import TextGenerator
                custom_generator = TextGenerator()
                custom_generator.client = mock_client
                
                topic = custom_generator.generate_topic()
                
                # Verify the prompt includes custom instructions
                call_args = mock_client.chat.completions.create.call_args
                prompt_content = call_args[1]['messages'][0]['content']
                
                self.assertIn('beginner developers', prompt_content)
                self.assertIn('casual and humorous', prompt_content)
                self.assertIn('Include practical examples', prompt_content)
                self.assertEqual(topic, "Custom AI Topic")


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


class TestWriterAgent(unittest.TestCase):
    """Test Writer Agent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        }):
            self.writer_agent = WriterAgent()
    
    def test_calculate_keyword_density(self):
        """Test keyword density calculation."""
        content = "AI is transforming healthcare. AI systems are being deployed in hospitals. The AI revolution is here."
        keyword = "AI"
        
        density = self.writer_agent.calculate_keyword_density(content, keyword)
        
        # 3 occurrences of "AI" in 16 words = 0.1875 (18.75%)
        self.assertGreater(density, 0.15)
        self.assertLess(density, 0.20)
    
    def test_calculate_keyword_density_case_insensitive(self):
        """Test that keyword density calculation is case-insensitive."""
        content = "AI is great. ai is powerful. Ai is revolutionary."
        keyword = "AI"
        
        density = self.writer_agent.calculate_keyword_density(content, keyword)
        
        # Should count all variations of "AI"
        self.assertGreater(density, 0.3)  # 3 occurrences in ~9 words
    
    def test_calculate_keyword_density_multiword(self):
        """Test keyword density with multi-word keywords."""
        content = "Machine learning is powerful. Machine learning algorithms are everywhere. Machine learning transforms industries."
        keyword = "machine learning"
        
        density = self.writer_agent.calculate_keyword_density(content, keyword)
        
        # 3 occurrences of "machine learning" in 13 words = ~0.23
        self.assertGreater(density, 0.2)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_article(self, mock_openai):
        """Test article generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        ## Introduction
        
        Artificial intelligence is revolutionizing healthcare in unprecedented ways. AI technologies 
        are enabling faster diagnoses, personalized treatments, and improved patient outcomes.
        
        ## Current Applications
        
        Healthcare AI systems are being deployed across multiple domains. Machine learning algorithms 
        analyze medical images with remarkable accuracy. AI assists doctors in diagnosis and treatment 
        planning.
        
        ## Future Prospects
        
        The future of AI in healthcare looks promising. Emerging technologies will continue to transform 
        medical practice. AI-powered tools will become increasingly sophisticated and accessible.
        
        ## Conclusion
        
        Artificial intelligence represents a paradigm shift in healthcare delivery. As AI technology 
        matures, its impact will only grow stronger.
        """ * 10  # Repeat to get enough words
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.writer_agent.client = mock_client
        
        article = self.writer_agent.generate_article(
            topic="The Future of AI in Healthcare",
            keywords=["AI", "healthcare", "artificial intelligence", "medical technology"]
        )
        
        self.assertIn("title", article)
        self.assertIn("content", article)
        self.assertIn("word_count", article)
        self.assertIn("keyword_density", article)
        self.assertIn("keywords_used", article)
        self.assertEqual(article["title"], "The Future of AI in Healthcare")
        self.assertGreater(article["word_count"], 0)
        self.assertIsInstance(article["keyword_density"], float)
        self.assertIsInstance(article["keywords_used"], list)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_article_with_research_summary(self, mock_openai):
        """Test article generation with research summary."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test article content with research data." * 100
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.writer_agent.client = mock_client
        
        research_summary = "Studies show that AI diagnostic tools achieve 95% accuracy."
        
        article = self.writer_agent.generate_article(
            topic="AI Diagnostics",
            keywords=["AI", "diagnostics", "accuracy"],
            research_summary=research_summary
        )
        
        self.assertIn("title", article)
        self.assertIn("content", article)
        # Verify that OpenAI was called with the research summary in the prompt
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args[1]["messages"][0]["content"]
        self.assertIn("Research Summary", prompt)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_meta_title(self, mock_openai):
        """Test meta title generation."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "AI Healthcare: Transform Your Practice"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.writer_agent.client = mock_client
        
        meta_title = self.writer_agent.generate_meta_title(
            title="The Future of AI in Healthcare",
            keywords=["AI", "healthcare"]
        )
        
        self.assertEqual(meta_title, "AI Healthcare: Transform Your Practice")
        self.assertLessEqual(len(meta_title), 70)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_meta_title_truncation(self, mock_openai):
        """Test that overly long meta titles are truncated."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is a very long meta title that exceeds the maximum character limit and should be truncated properly"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.writer_agent.client = mock_client
        
        meta_title = self.writer_agent.generate_meta_title(
            title="Test Title",
            keywords=["test"]
        )
        
        self.assertLessEqual(len(meta_title), 70)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_meta_description(self, mock_openai):
        """Test meta description generation."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Discover how AI is transforming healthcare with cutting-edge diagnostics, personalized treatments, and improved patient outcomes."
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.writer_agent.client = mock_client
        
        meta_description = self.writer_agent.generate_meta_description(
            title="AI in Healthcare",
            content="AI is revolutionizing healthcare...",
            keywords=["AI", "healthcare"]
        )
        
        self.assertGreater(len(meta_description), 100)
        self.assertLessEqual(len(meta_description), 160)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_meta_description_truncation(self, mock_openai):
        """Test that overly long meta descriptions are truncated."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is an extremely long meta description that far exceeds the maximum character limit of 160 characters and should definitely be truncated to ensure it fits within the optimal length for search engine results pages."
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.writer_agent.client = mock_client
        
        meta_description = self.writer_agent.generate_meta_description(
            title="Test",
            content="Test content",
            keywords=["test"]
        )
        
        self.assertLessEqual(len(meta_description), 160)
    
    @patch('agents.writer_agent.OpenAI')
    def test_generate_tags(self, mock_openai):
        """Test tag generation."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "AI, healthcare, machine learning, diagnostics, medical technology"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.writer_agent.client = mock_client
        
        tags = self.writer_agent.generate_tags(
            title="AI in Healthcare",
            content="AI is revolutionizing healthcare with machine learning...",
            keywords=["AI", "healthcare"]
        )
        
        self.assertIsInstance(tags, list)
        self.assertGreater(len(tags), 0)
        self.assertLessEqual(len(tags), 8)
    
    @patch('agents.writer_agent.OpenAI')
    def test_create_complete_article(self, mock_openai):
        """Test complete article creation with all metadata."""
        # Mock multiple OpenAI responses for different calls
        mock_article_response = Mock()
        mock_article_response.choices = [Mock()]
        mock_article_response.choices[0].message.content = """
        ## Introduction
        
        Artificial intelligence is revolutionizing healthcare. AI systems provide advanced diagnostics
        and personalized treatment plans.
        
        ## Body
        
        Healthcare AI applications span multiple domains. Machine learning algorithms analyze complex
        medical data with unprecedented accuracy. AI-powered tools assist medical professionals in
        making informed decisions.
        
        ## Conclusion
        
        The future of AI in healthcare is bright and transformative.
        """ * 20  # Repeat to meet word count
        
        mock_meta_title_response = Mock()
        mock_meta_title_response.choices = [Mock()]
        mock_meta_title_response.choices[0].message.content = "AI Healthcare Revolution"
        
        mock_meta_desc_response = Mock()
        mock_meta_desc_response.choices = [Mock()]
        mock_meta_desc_response.choices[0].message.content = "Discover how AI is transforming healthcare with advanced diagnostics and personalized care."
        
        mock_tags_response = Mock()
        mock_tags_response.choices = [Mock()]
        mock_tags_response.choices[0].message.content = "AI, healthcare, machine learning, diagnostics, medical"
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [
            mock_article_response,
            mock_meta_title_response,
            mock_meta_desc_response,
            mock_tags_response
        ]
        mock_openai.return_value = mock_client
        
        self.writer_agent.client = mock_client
        
        complete_article = self.writer_agent.create_complete_article(
            topic="The Future of AI in Healthcare",
            keywords=["AI", "healthcare", "machine learning", "diagnostics"],
            research_summary="Recent studies show significant improvements in diagnostic accuracy."
        )
        
        # Verify all required fields are present
        self.assertIn("title", complete_article)
        self.assertIn("content", complete_article)
        self.assertIn("meta_title", complete_article)
        self.assertIn("meta_description", complete_article)
        self.assertIn("tags", complete_article)
        self.assertIn("word_count", complete_article)
        self.assertIn("keyword_density", complete_article)
        self.assertIn("keywords_used", complete_article)
        self.assertIn("seo_optimized", complete_article)
        self.assertIn("ai_generated", complete_article)
        
        # Verify data types and values
        self.assertEqual(complete_article["title"], "The Future of AI in Healthcare")
        self.assertIsInstance(complete_article["content"], str)
        self.assertIsInstance(complete_article["meta_title"], str)
        self.assertIsInstance(complete_article["meta_description"], str)
        self.assertIsInstance(complete_article["tags"], list)
        self.assertIsInstance(complete_article["word_count"], int)
        self.assertIsInstance(complete_article["keyword_density"], float)
        self.assertIsInstance(complete_article["keywords_used"], list)
        self.assertTrue(complete_article["seo_optimized"])
        self.assertTrue(complete_article["ai_generated"])
        
        # Verify reasonable values
        self.assertGreater(complete_article["word_count"], 0)
        self.assertGreaterEqual(len(complete_article["tags"]), 1)
        self.assertLessEqual(len(complete_article["tags"]), 8)
    
    @patch('agents.writer_agent.OpenAI')
    @patch('agents.writer_agent.settings')
    def test_writer_agent_with_custom_settings(self, mock_settings, mock_openai):
        """Test that WriterAgent respects custom settings."""
        # Mock the settings object with custom values
        mock_settings.openai_api_key = 'test_key'
        mock_settings.content_tone = 'professional and technical'
        mock_settings.target_audience = 'software engineers'
        mock_settings.content_style = 'detailed and code-heavy'
        mock_settings.custom_instructions = ''
        
        writer = WriterAgent()
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test content" * 100
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        writer.client = mock_client
        
        writer.generate_article(
            topic="Python Best Practices",
            keywords=["Python", "best practices", "coding"]
        )
        
        # Verify that the custom settings were used in the prompt
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args[1]["messages"][0]["content"]
        self.assertIn("professional and technical", prompt)
        self.assertIn("software engineers", prompt)
        self.assertIn("detailed and code-heavy", prompt)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)