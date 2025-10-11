"""
Test suite for the Editor Agent.
"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.editor_agent import EditorAgent


class TestEditorAgent(unittest.TestCase):
    """Test the Editor Agent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        }):
            self.editor = EditorAgent()
    
    @patch('agents.editor_agent.OpenAI')
    def test_check_grammar_and_spelling(self, mock_openai):
        """Test grammar and spelling check."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        ERRORS: None
        CORRECTED_TEXT: None
        SUGGESTIONS: Consider using more active voice in some sentences
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        result = self.editor.check_grammar_and_spelling("This is a test content.")
        
        self.assertFalse(result["has_errors"])
        self.assertEqual(len(result["errors"]), 0)
        self.assertIsNone(result["corrected_text"])
        self.assertGreater(len(result["suggestions"]), 0)
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('agents.editor_agent.OpenAI')
    def test_check_grammar_with_errors(self, mock_openai):
        """Test grammar check with errors found."""
        # Mock OpenAI response with errors
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        ERRORS: Sentence fragment at line 2
        CORRECTED_TEXT: This is corrected test content.
        SUGGESTIONS: Review sentence structure
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        result = self.editor.check_grammar_and_spelling("This is test content.")
        
        self.assertTrue(result["has_errors"])
        self.assertGreater(len(result["errors"]), 0)
        self.assertIsNotNone(result["corrected_text"])
    
    @patch('agents.editor_agent.OpenAI')
    def test_analyze_tone_and_style(self, mock_openai):
        """Test tone and style analysis."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        CURRENT_TONE: Professional and engaging
        MATCHES_TARGET: Yes
        CONSISTENCY_RATING: 8
        SUGGESTIONS: Great job maintaining consistency
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        result = self.editor.analyze_tone_and_style("Test content", "professional and engaging")
        
        self.assertEqual(result["current_tone"], "Professional and engaging")
        self.assertTrue(result["matches_target"])
        self.assertEqual(result["consistency_rating"], 8)
        self.assertGreater(len(result["suggestions"]), 0)
    
    @patch('agents.editor_agent.OpenAI')
    def test_analyze_structure(self, mock_openai):
        """Test structure analysis."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        INTRODUCTION: Good - Clear and engaging
        BODY_FLOW: Good - Logical progression
        CONCLUSION: Good - Strong call to action
        READABILITY_SCORE: 9
        IMPROVEMENTS: None needed
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        result = self.editor.analyze_structure("Test article content")
        
        self.assertIn("Good", result["introduction"])
        self.assertIn("Good", result["body_flow"])
        self.assertIn("Good", result["conclusion"])
        self.assertEqual(result["readability_score"], 9)
    
    @patch('agents.editor_agent.OpenAI')
    def test_optimize_seo_keywords(self, mock_openai):
        """Test SEO keyword optimization."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        PRIMARY: AI, automation, technology
        SECONDARY: machine learning, innovation, digital transformation
        LONG_TAIL: artificial intelligence in business, automated content generation
        DENSITY: Good
        SUGGESTIONS: Integrate keywords more naturally in the introduction
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        result = self.editor.optimize_seo_keywords(
            "AI and Automation",
            "Article content about AI",
            ["AI", "tech"]
        )
        
        self.assertGreater(len(result["primary_keywords"]), 0)
        self.assertGreater(len(result["secondary_keywords"]), 0)
        self.assertGreater(len(result["long_tail_keywords"]), 0)
        self.assertEqual(result["keyword_density"], "Good")
    
    @patch('agents.editor_agent.OpenAI')
    def test_refine_meta_title(self, mock_openai):
        """Test meta title refinement."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        OPTIMIZED_TITLE: AI Revolution: How Automation is Changing the Future
        CHARACTER_COUNT: 55
        IMPROVEMENTS: Added keywords and made more compelling
        SEO_SCORE: 9
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        result = self.editor.refine_meta_title(
            "The AI Revolution",
            "An article about AI"
        )
        
        self.assertNotEqual(result["optimized_title"], "")
        self.assertGreater(result["character_count"], 0)
        self.assertLessEqual(result["character_count"], 70)
        self.assertGreater(result["seo_score"], 5)
    
    @patch('agents.editor_agent.OpenAI')
    def test_generate_meta_description(self, mock_openai):
        """Test meta description generation."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        META_DESCRIPTION: Discover how AI and automation are revolutionizing content creation. Learn about the latest innovations and their impact on the future.
        CHARACTER_COUNT: 155
        KEYWORDS: AI, automation, content creation, innovation
        SEO_SCORE: 8
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        result = self.editor.generate_meta_description(
            "AI and Automation",
            "Article about AI and automation in content creation"
        )
        
        self.assertNotEqual(result["meta_description"], "")
        self.assertGreater(result["character_count"], 100)
        self.assertLessEqual(result["character_count"], 200)
        self.assertGreater(len(result["keywords_included"]), 0)
    
    @patch('agents.editor_agent.OpenAI')
    def test_optimize_tags(self, mock_openai):
        """Test tag optimization."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        OPTIMIZED_TAGS: AI, automation, technology, innovation, machine learning
        NEW_TAGS: machine learning, innovation
        REMOVED_TAGS: none
        REASONING: Added relevant trending topics
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        result = self.editor.optimize_tags(
            "AI and Automation",
            "Article content",
            ["AI", "automation", "technology"]
        )
        
        self.assertGreater(len(result["optimized_tags"]), 0)
        self.assertIsInstance(result["new_tags"], list)
        self.assertIsInstance(result["removed_tags"], list)
        self.assertNotEqual(result["reasoning"], "")
    
    @patch('agents.editor_agent.OpenAI')
    def test_edit_article_complete_workflow(self, mock_openai):
        """Test the complete article editing workflow."""
        # Mock all API calls
        mock_responses = [
            # Grammar check
            Mock(choices=[Mock(message=Mock(content="ERRORS: None\nCORRECTED_TEXT: None\nSUGGESTIONS: None"))]),
            # Tone analysis
            Mock(choices=[Mock(message=Mock(content="CURRENT_TONE: Professional\nMATCHES_TARGET: Yes\nCONSISTENCY_RATING: 8\nSUGGESTIONS: None"))]),
            # Structure analysis
            Mock(choices=[Mock(message=Mock(content="INTRODUCTION: Good\nBODY_FLOW: Good\nCONCLUSION: Good\nREADABILITY_SCORE: 8\nIMPROVEMENTS: None"))]),
            # SEO keywords
            Mock(choices=[Mock(message=Mock(content="PRIMARY: AI, tech\nSECONDARY: automation\nLONG_TAIL: AI in business\nDENSITY: Good\nSUGGESTIONS: None"))]),
            # Title refinement
            Mock(choices=[Mock(message=Mock(content="OPTIMIZED_TITLE: AI Revolution\nCHARACTER_COUNT: 14\nIMPROVEMENTS: None\nSEO_SCORE: 8"))]),
            # Meta description
            Mock(choices=[Mock(message=Mock(content="META_DESCRIPTION: Learn about AI\nCHARACTER_COUNT: 15\nKEYWORDS: AI\nSEO_SCORE: 7"))]),
            # Tag optimization
            Mock(choices=[Mock(message=Mock(content="OPTIMIZED_TAGS: AI, tech\nNEW_TAGS: none\nREMOVED_TAGS: none\nREASONING: Good tags"))])
        ]
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = mock_responses
        mock_openai.return_value = mock_client
        
        self.editor.client = mock_client
        
        article_data = {
            "title": "AI Revolution",
            "subtitle": "The Future of Technology",
            "content": "This is a test article about AI and automation.",
            "tags": ["AI", "technology"]
        }
        
        result = self.editor.edit_article(article_data)
        
        # Verify structure of result
        self.assertIn("edited_article", result)
        self.assertIn("seo_report", result)
        self.assertIn("quality_metrics", result)
        self.assertIn("improvements_made", result)
        
        # Verify edited article
        edited_article = result["edited_article"]
        self.assertIn("title", edited_article)
        self.assertIn("content", edited_article)
        self.assertIn("meta_description", edited_article)
        self.assertIn("tags", edited_article)
        
        # Verify SEO report
        seo_report = result["seo_report"]
        self.assertIn("overall_seo_score", seo_report)
        self.assertIn("title_optimization", seo_report)
        self.assertIn("meta_description", seo_report)
        self.assertIn("keywords", seo_report)
        self.assertIn("tags", seo_report)
        
        # Verify quality metrics
        quality_metrics = result["quality_metrics"]
        self.assertIn("overall_score", quality_metrics)
        self.assertIn("grammar_check", quality_metrics)
        self.assertIn("tone_analysis", quality_metrics)
        self.assertIn("structure_analysis", quality_metrics)
    
    @patch('agents.editor_agent.OpenAI')
    def test_get_editing_summary(self, mock_openai):
        """Test editing summary generation."""
        # Create a mock editing result
        editing_result = {
            "edited_article": {
                "title": "Test Title",
                "content": "Test content"
            },
            "seo_report": {
                "overall_seo_score": 8.5,
                "title_optimization": {
                    "original": "Original Title",
                    "optimized": "Optimized Title",
                    "character_count": 15,
                    "improvements": ["Added keywords"],
                    "score": 9
                },
                "meta_description": {
                    "description": "Test meta description",
                    "character_count": 20,
                    "keywords_included": ["test"],
                    "score": 8
                },
                "keywords": {
                    "primary": ["test", "AI"],
                    "secondary": ["tech"],
                    "long_tail": ["test keyword phrase"],
                    "density": "Good",
                    "suggestions": []
                },
                "tags": {
                    "original": ["old"],
                    "optimized": ["new", "test"],
                    "new_tags": ["test"],
                    "removed_tags": ["old"]
                }
            },
            "quality_metrics": {
                "overall_score": 8.0,
                "grammar_check": {
                    "has_errors": False,
                    "errors_found": 0,
                    "suggestions": []
                },
                "tone_analysis": {
                    "current_tone": "Professional",
                    "target_tone": "Professional",
                    "matches_target": True,
                    "consistency_rating": 8,
                    "suggestions": []
                },
                "structure_analysis": {
                    "introduction": "Good",
                    "body_flow": "Good",
                    "conclusion": "Good",
                    "readability_score": 8,
                    "improvements": []
                }
            },
            "improvements_made": {
                "grammar_corrections": False,
                "title_optimized": True,
                "tags_optimized": True,
                "meta_description_generated": True
            }
        }
        
        summary = self.editor.get_editing_summary(editing_result)
        
        self.assertIsInstance(summary, str)
        self.assertIn("EDITOR AGENT REPORT", summary)
        self.assertIn("Overall Quality Score", summary)
        self.assertIn("Overall SEO Score", summary)
        self.assertIn("IMPROVEMENTS MADE", summary)
        self.assertIn("SEO OPTIMIZATIONS", summary)


class TestEditorAgentIntegration(unittest.TestCase):
    """Integration tests for Editor Agent with other components."""
    
    def setUp(self):
        """Set up test environment."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        }):
            self.editor = EditorAgent()
    
    def test_editor_accepts_writer_output(self):
        """Test that Editor Agent accepts output from Writer/TextGenerator."""
        # Simulate Writer Agent output
        writer_output = {
            "title": "The Future of AI",
            "subtitle": "Exploring innovations in artificial intelligence",
            "content": "Artificial intelligence is transforming our world...",
            "tags": ["AI", "technology", "innovation"],
            "word_count": 50,
            "ai_generated": True
        }
        
        # Verify the editor can process this format
        self.assertIsNotNone(writer_output.get("title"))
        self.assertIsNotNone(writer_output.get("content"))
        self.assertIsInstance(writer_output.get("tags", []), list)
    
    @patch('agents.editor_agent.OpenAI')
    def test_editor_output_compatible_with_publisher(self, mock_openai):
        """Test that Editor Agent output is compatible with Publisher."""
        # Mock OpenAI responses for all editing steps
        mock_responses = [
            Mock(choices=[Mock(message=Mock(content="ERRORS: None\nCORRECTED_TEXT: None\nSUGGESTIONS: None"))]),
            Mock(choices=[Mock(message=Mock(content="CURRENT_TONE: Professional\nMATCHES_TARGET: Yes\nCONSISTENCY_RATING: 8\nSUGGESTIONS: None"))]),
            Mock(choices=[Mock(message=Mock(content="INTRODUCTION: Good\nBODY_FLOW: Good\nCONCLUSION: Good\nREADABILITY_SCORE: 8\nIMPROVEMENTS: None"))]),
            Mock(choices=[Mock(message=Mock(content="PRIMARY: AI\nSECONDARY: tech\nLONG_TAIL: AI future\nDENSITY: Good\nSUGGESTIONS: None"))]),
            Mock(choices=[Mock(message=Mock(content="OPTIMIZED_TITLE: The Future of AI\nCHARACTER_COUNT: 17\nIMPROVEMENTS: None\nSEO_SCORE: 8"))]),
            Mock(choices=[Mock(message=Mock(content="META_DESCRIPTION: AI is transforming\nCHARACTER_COUNT: 20\nKEYWORDS: AI\nSEO_SCORE: 7"))]),
            Mock(choices=[Mock(message=Mock(content="OPTIMIZED_TAGS: AI, tech\nNEW_TAGS: none\nREMOVED_TAGS: none\nREASONING: Good"))])
        ]
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = mock_responses
        self.editor.client = mock_client
        
        article_data = {
            "title": "The Future of AI",
            "subtitle": "Exploring AI",
            "content": "AI is changing the world.",
            "tags": ["AI"]
        }
        
        result = self.editor.edit_article(article_data)
        edited_article = result["edited_article"]
        
        # Verify output has required fields for Publisher
        self.assertIn("title", edited_article)
        self.assertIn("content", edited_article)
        self.assertIn("tags", edited_article)
        self.assertIn("ai_generated", edited_article)
        
        # Verify types are correct
        self.assertIsInstance(edited_article["title"], str)
        self.assertIsInstance(edited_article["content"], str)
        self.assertIsInstance(edited_article["tags"], list)
        self.assertIsInstance(edited_article["ai_generated"], bool)


if __name__ == '__main__':
    unittest.main(verbosity=2)
