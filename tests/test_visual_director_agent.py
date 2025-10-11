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
    """Test Visual Director Agent functionality."""
    
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
        self.assertIsNotNone(self.agent.client)
        self.assertTrue(os.path.exists(self.agent.output_dir))
        self.assertEqual(self.agent.max_filename_length, 60)
        self.assertEqual(self.agent.max_alt_text_length, 125)
    
    @patch('agents.visual_director_agent.OpenAI')
    def test_analyze_content_for_seo(self, mock_openai):
        """Test SEO content analysis."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        PRIMARY_KEYWORDS: artificial intelligence, machine learning, AI technology
        VISUAL_THEMES: futuristic, technology, innovation
        TARGET_EMOTION: inspired
        KEY_CONCEPTS: AI advancement, future technology, intelligent systems
        SEO_FOCUS: artificial intelligence
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        analysis = self.agent.analyze_content_for_seo(
            "The Future of Artificial Intelligence",
            "Article content about AI and its impact...",
            ["AI", "technology", "future"]
        )
        
        self.assertIn("primary_keywords", analysis)
        self.assertIn("visual_themes", analysis)
        self.assertIn("target_emotion", analysis)
        self.assertIn("key_concepts", analysis)
        self.assertIn("seo_focus", analysis)
        
        self.assertEqual(analysis["seo_focus"], "artificial intelligence")
        self.assertIn("artificial intelligence", analysis["primary_keywords"])
        self.assertIn("futuristic", analysis["visual_themes"])
    
    def test_extract_list(self):
        """Test list extraction from analysis text."""
        text = "PRIMARY_KEYWORDS: keyword1, keyword2, keyword3\nOTHER: value"
        result = self.agent._extract_list(text, "PRIMARY_KEYWORDS")
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "keyword1")
        self.assertEqual(result[1], "keyword2")
    
    def test_extract_value(self):
        """Test value extraction from analysis text."""
        text = "SEO_FOCUS: artificial intelligence\nOTHER: value"
        result = self.agent._extract_value(text, "SEO_FOCUS")
        
        self.assertEqual(result, "artificial intelligence")
    
    def test_generate_seo_optimized_prompt(self):
        """Test SEO-optimized prompt generation."""
        seo_analysis = {
            "primary_keywords": ["AI", "technology", "future"],
            "visual_themes": ["futuristic", "modern", "digital"],
            "target_emotion": "inspired",
            "key_concepts": ["artificial intelligence", "innovation"]
        }
        
        prompt = self.agent.generate_seo_optimized_prompt(
            "The Future of AI",
            "Content about AI...",
            seo_analysis,
            media_type="featured"
        )
        
        self.assertIn("The Future of AI", prompt)
        self.assertIn("futuristic", prompt)
        self.assertIn("AI", prompt)
        self.assertIn("professional", prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 100)
    
    def test_generate_seo_optimized_prompt_different_types(self):
        """Test prompt generation for different media types."""
        seo_analysis = {
            "primary_keywords": ["test"],
            "visual_themes": ["modern"],
            "target_emotion": "engaged",
            "key_concepts": ["concept"]
        }
        
        # Test featured
        featured_prompt = self.agent.generate_seo_optimized_prompt(
            "Test", "Content", seo_analysis, "featured"
        )
        self.assertIn("blog header", featured_prompt.lower())
        
        # Test thumbnail
        thumbnail_prompt = self.agent.generate_seo_optimized_prompt(
            "Test", "Content", seo_analysis, "thumbnail"
        )
        self.assertIn("compact", thumbnail_prompt.lower())
        
        # Test social
        social_prompt = self.agent.generate_seo_optimized_prompt(
            "Test", "Content", seo_analysis, "social"
        )
        self.assertIn("social", social_prompt.lower())
    
    def test_generate_seo_filename(self):
        """Test SEO-friendly filename generation."""
        filename = self.agent.generate_seo_filename(
            "The Future of Artificial Intelligence: What's Next?",
            "AI technology",
            media_type="featured"
        )
        
        self.assertTrue(filename.startswith("featured-"))
        self.assertTrue(filename.endswith(".png"))
        self.assertNotIn(" ", filename)
        self.assertNotIn("'", filename)
        self.assertNotIn("?", filename)
        self.assertIn("ai-technology", filename.lower())
        self.assertLessEqual(len(filename), self.agent.max_filename_length + 20)  # +20 for prefix and extension
    
    def test_generate_seo_filename_long_title(self):
        """Test filename generation with very long title."""
        long_title = "This is a very long article title that goes on and on with many words " \
                    "that would exceed the maximum filename length if not properly truncated"
        
        filename = self.agent.generate_seo_filename(long_title, "keyword", "image")
        
        self.assertLessEqual(len(filename), self.agent.max_filename_length + 20)
        self.assertTrue(filename.endswith(".png"))
        self.assertNotIn(" ", filename)
    
    def test_generate_alt_text(self):
        """Test alt text generation."""
        seo_analysis = {
            "primary_keywords": ["AI", "technology", "innovation"],
            "seo_focus": "artificial intelligence",
            "key_concepts": ["machine learning", "future tech"]
        }
        
        alt_text = self.agent.generate_alt_text(
            "The Future of AI",
            seo_analysis,
            media_type="featured"
        )
        
        self.assertIsInstance(alt_text, str)
        self.assertGreater(len(alt_text), 10)
        self.assertLessEqual(len(alt_text), self.agent.max_alt_text_length)
        self.assertIn("artificial intelligence", alt_text.lower())
    
    def test_generate_alt_text_different_types(self):
        """Test alt text for different media types."""
        seo_analysis = {
            "primary_keywords": ["test"],
            "seo_focus": "testing",
            "key_concepts": ["concept"]
        }
        
        # Featured
        featured_alt = self.agent.generate_alt_text("Test", seo_analysis, "featured")
        self.assertIn("featured", featured_alt.lower())
        
        # Thumbnail
        thumb_alt = self.agent.generate_alt_text("Test", seo_analysis, "thumbnail")
        self.assertIn("thumbnail", thumb_alt.lower())
        
        # Social
        social_alt = self.agent.generate_alt_text("Test", seo_analysis, "social")
        self.assertIn("social", social_alt.lower())
    
    @patch('agents.visual_director_agent.OpenAI')
    def test_generate_caption(self, mock_openai):
        """Test caption generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Discover the future of AI technology and innovation."
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        seo_analysis = {
            "primary_keywords": ["AI", "technology"],
            "target_emotion": "inspired"
        }
        
        caption = self.agent.generate_caption("The Future of AI", seo_analysis)
        
        self.assertIsInstance(caption, str)
        self.assertGreater(len(caption), 10)
        self.assertLessEqual(len(caption), self.agent.max_caption_length)
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('agents.visual_director_agent.requests.get')
    @patch('agents.visual_director_agent.OpenAI')
    def test_generate_seo_optimized_image(self, mock_openai, mock_requests):
        """Test complete SEO-optimized image generation."""
        # Mock OpenAI responses
        mock_analysis_response = Mock()
        mock_analysis_response.choices = [Mock()]
        mock_analysis_response.choices[0].message.content = """
        PRIMARY_KEYWORDS: AI, technology, future
        VISUAL_THEMES: futuristic, digital
        TARGET_EMOTION: inspired
        KEY_CONCEPTS: artificial intelligence
        SEO_FOCUS: AI technology
        """
        
        mock_image_response = Mock()
        mock_image_response.data = [Mock()]
        mock_image_response.data[0].url = "https://example.com/test_image.png"
        
        mock_caption_response = Mock()
        mock_caption_response.choices = [Mock()]
        mock_caption_response.choices[0].message.content = "Explore AI innovation."
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [
            mock_analysis_response, 
            mock_caption_response
        ]
        mock_client.images.generate.return_value = mock_image_response
        mock_openai.return_value = mock_client
        
        # Mock image download
        mock_requests.return_value.content = b"fake_image_data"
        mock_requests.return_value.raise_for_status = Mock()
        
        self.agent.client = mock_client
        
        result = self.agent.generate_seo_optimized_image(
            "The Future of AI",
            "Content about artificial intelligence...",
            tags=["AI", "technology"],
            media_type="featured"
        )
        
        self.assertIsNotNone(result)
        self.assertIn("image_path", result)
        self.assertIn("filename", result)
        self.assertIn("alt_text", result)
        self.assertIn("caption", result)
        self.assertIn("seo_metadata", result)
        self.assertTrue(result["ai_generated"])
        self.assertTrue(result["seo_optimized"])
        
        # Verify SEO metadata
        seo_meta = result["seo_metadata"]
        self.assertIn("focus_keyword", seo_meta)
        self.assertIn("keywords", seo_meta)
        self.assertIn("visual_themes", seo_meta)
        
        # Verify file was created
        self.assertTrue(os.path.exists(result["image_path"]))
    
    @patch('agents.visual_director_agent.requests.get')
    @patch('agents.visual_director_agent.OpenAI')
    def test_generate_image_set(self, mock_openai, mock_requests):
        """Test generation of complete image set."""
        # Mock OpenAI responses
        mock_analysis_response = Mock()
        mock_analysis_response.choices = [Mock()]
        mock_analysis_response.choices[0].message.content = """
        PRIMARY_KEYWORDS: AI, technology
        VISUAL_THEMES: modern
        TARGET_EMOTION: engaged
        KEY_CONCEPTS: innovation
        SEO_FOCUS: AI
        """
        
        mock_image_response = Mock()
        mock_image_response.data = [Mock()]
        mock_image_response.data[0].url = "https://example.com/test.png"
        
        mock_caption_response = Mock()
        mock_caption_response.choices = [Mock()]
        mock_caption_response.choices[0].message.content = "Test caption"
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [
            mock_analysis_response,  # Initial analysis
            mock_caption_response,   # Featured caption
            mock_caption_response,   # Thumbnail caption
            mock_caption_response    # Social caption
        ]
        mock_client.images.generate.return_value = mock_image_response
        mock_openai.return_value = mock_client
        
        # Mock image download
        mock_requests.return_value.content = b"fake_image_data"
        mock_requests.return_value.raise_for_status = Mock()
        
        self.agent.client = mock_client
        
        result = self.agent.generate_image_set(
            "Test Article",
            "Content about testing...",
            tags=["test"]
        )
        
        self.assertTrue(result["success"])
        self.assertIn("seo_analysis", result)
        self.assertIn("images", result)
        self.assertGreater(result["images_generated"], 0)
        
        # Check that multiple images were generated
        images = result["images"]
        self.assertIn("featured", images)
        self.assertIn("thumbnail", images)
        self.assertIn("social", images)
    
    def test_create_thumbnail_size(self):
        """Test thumbnail resizing."""
        # Create a test image
        from PIL import Image as PILImage
        test_image_path = os.path.join(self.temp_dir, "test_image.png")
        img = PILImage.new('RGB', (1024, 1024), color='red')
        img.save(test_image_path)
        
        # Create thumbnail
        thumb_path = self.agent._create_thumbnail_size(test_image_path, size=(200, 200))
        
        self.assertTrue(os.path.exists(thumb_path))
        self.assertNotEqual(test_image_path, thumb_path)
        
        # Verify thumbnail is smaller
        with PILImage.open(thumb_path) as thumb:
            self.assertLessEqual(thumb.width, 200)
            self.assertLessEqual(thumb.height, 200)
    
    def test_get_seo_report_single_image(self):
        """Test SEO report generation for single image."""
        result = {
            "filename": "test-ai-article.png",
            "alt_text": "Featured image about AI technology",
            "caption": "Exploring the future of AI"
        }
        
        report = self.agent.get_seo_report(result)
        
        self.assertIn("test-ai-article.png", report)
        self.assertIn("Featured image about AI technology", report)
        self.assertIn("Exploring the future of AI", report)
    
    def test_get_seo_report_image_set(self):
        """Test SEO report generation for image set."""
        result = {
            "seo_analysis": {
                "seo_focus": "AI technology",
                "primary_keywords": ["AI", "technology", "innovation"],
                "visual_themes": ["futuristic", "modern"],
                "target_emotion": "inspired"
            },
            "images": {
                "featured": {
                    "filename": "featured-ai.png",
                    "alt_text": "Featured AI image",
                    "caption": "AI innovation"
                },
                "thumbnail": {
                    "filename": "thumbnail-ai.png",
                    "alt_text": "Thumbnail AI image",
                    "caption": "AI tech"
                }
            }
        }
        
        report = self.agent.get_seo_report(result)
        
        self.assertIn("AI technology", report)
        self.assertIn("featured-ai.png", report)
        self.assertIn("thumbnail-ai.png", report)
        self.assertIn("SEO Analysis", report)
        self.assertIn("FEATURED Image", report)
        self.assertIn("THUMBNAIL Image", report)
    
    def test_analyze_content_for_seo_fallback(self):
        """Test SEO analysis fallback on error."""
        # Create agent with invalid client to force error
        with patch('agents.visual_director_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = mock_client
            
            self.agent.client = mock_client
            
            analysis = self.agent.analyze_content_for_seo(
                "Test Title",
                "Test content",
                ["tag1"]
            )
            
            # Should return fallback values
            self.assertIsNotNone(analysis)
            self.assertIn("seo_focus", analysis)
            self.assertIn("primary_keywords", analysis)
    
    def test_generate_caption_fallback(self):
        """Test caption generation fallback on error."""
        with patch('agents.visual_director_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = mock_client
            
            self.agent.client = mock_client
            
            seo_analysis = {"primary_keywords": [], "target_emotion": ""}
            caption = self.agent.generate_caption("Test Title", seo_analysis)
            
            # Should return fallback caption
            self.assertIsNotNone(caption)
            self.assertIn("Test Title", caption)


class TestVisualDirectorAgentIntegration(unittest.TestCase):
    """Integration tests for Visual Director Agent."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_seo_filename_consistency(self):
        """Test that filenames are consistent and valid."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication',
            'OUTPUT_DIR': self.temp_dir
        }):
            agent = VisualDirectorAgent()
            
            test_cases = [
                ("Simple Title", "keyword"),
                ("Title with Special Chars!@#$%", "focus"),
                ("Very Long Title " * 10, "word"),
                ("Title_with_underscores", "key"),
                ("Title-with-hyphens", "term")
            ]
            
            for title, focus in test_cases:
                filename = agent.generate_seo_filename(title, focus, "test")
                
                # Verify no invalid characters
                self.assertNotIn(" ", filename)
                self.assertNotIn("!", filename)
                self.assertNotIn("@", filename)
                
                # Verify reasonable length
                self.assertLessEqual(len(filename), 100)
                
                # Verify format
                self.assertTrue(filename.endswith(".png"))
                self.assertTrue(filename.startswith("test-"))
    
    def test_alt_text_length_limits(self):
        """Test that alt text respects length limits."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication',
            'OUTPUT_DIR': self.temp_dir
        }):
            agent = VisualDirectorAgent()
            
            seo_analysis = {
                "primary_keywords": ["very", "long", "list", "of", "keywords"] * 10,
                "seo_focus": "testing very long content" * 20,
                "key_concepts": ["concept"] * 50
            }
            
            alt_text = agent.generate_alt_text(
                "Very Long Title " * 20,
                seo_analysis,
                "featured"
            )
            
            self.assertLessEqual(len(alt_text), agent.max_alt_text_length)


if __name__ == '__main__':
    unittest.main(verbosity=2)
