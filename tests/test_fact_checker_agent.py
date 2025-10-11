"""
Test suite for the Fact-Checker Agent.
"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestFactCheckerAgent(unittest.TestCase):
    """Test the Fact-Checker Agent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Set up environment variables
        self.env_patcher = patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'test_password',
            'SUBSTACK_PUBLICATION': 'test_publication'
        })
        self.env_patcher.start()
        
        # Import after setting environment
        from agents.fact_checker_agent import FactCheckerAgent
        self.agent = FactCheckerAgent()
        
        # Sample content for testing
        self.sample_content = {
            "title": "The Rise of AI in 2024",
            "content": """
            Artificial intelligence has grown dramatically. According to recent studies,
            AI adoption increased by 47% in 2023. The market size reached $150 billion,
            and experts predict it will grow to $500 billion by 2027. Machine learning
            algorithms can now process 1 million data points per second.
            
            This technology is transforming industries across the globe.
            """
        }
    
    def tearDown(self):
        """Clean up test environment."""
        self.env_patcher.stop()
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        self.assertEqual(self.agent.name, "FactCheckerAgent")
        self.assertIsNotNone(self.agent.client)
        self.assertEqual(self.agent.confidence_threshold, 0.7)
    
    def test_validate_input_valid(self):
        """Test input validation with valid content."""
        result = self.agent.validate_input(self.sample_content)
        self.assertTrue(result)
    
    def test_validate_input_invalid(self):
        """Test input validation with invalid content."""
        # Missing required keys
        invalid_content = {"title": "Test"}
        result = self.agent.validate_input(invalid_content)
        self.assertFalse(result)
        
        # Not a dictionary
        result = self.agent.validate_input("not a dict")
        self.assertFalse(result)
    
    def test_extract_claims_fallback(self):
        """Test fallback claim extraction using regex."""
        text = "AI adoption increased by 47% in 2023. The market reached $150 billion."
        claims = self.agent._extract_claims_fallback(text)
        
        self.assertIsInstance(claims, list)
        self.assertGreater(len(claims), 0)
        
        # Check structure of extracted claims
        for claim in claims:
            self.assertIn("id", claim)
            self.assertIn("text", claim)
            self.assertIn("type", claim)
            self.assertIn("context", claim)
            self.assertEqual(claim["type"], "statistic")
    
    @patch('agents.fact_checker_agent.OpenAI')
    def test_extract_claims_with_ai(self, mock_openai):
        """Test AI-powered claim extraction."""
        # Mock AI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps([
            {
                "text": "AI adoption increased by 47% in 2023",
                "type": "statistic",
                "context": "Recent studies show growth"
            },
            {
                "text": "Market size reached $150 billion",
                "type": "fact",
                "context": "Current market valuation"
            }
        ])
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        claims = self.agent._extract_claims(self.sample_content)
        
        self.assertEqual(len(claims), 2)
        self.assertEqual(claims[0]["type"], "statistic")
        self.assertEqual(claims[1]["type"], "fact")
        
        # Verify AI was called
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('agents.fact_checker_agent.OpenAI')
    def test_validate_claim(self, mock_openai):
        """Test claim validation."""
        # Mock AI validation response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "is_valid": True,
            "confidence_score": 0.85,
            "reasoning": "Claim is consistent with industry reports",
            "potential_sources": ["Gartner", "McKinsey"],
            "flags": [],
            "seo_value": "high",
            "seo_reasoning": "Specific statistic with verification potential"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        claim = {
            "id": 1,
            "text": "AI adoption increased by 47%",
            "type": "statistic",
            "context": "Recent studies"
        }
        
        result = self.agent._validate_claim(claim, self.sample_content)
        
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["confidence_score"], 0.85)
        self.assertFalse(result["needs_review"])
        self.assertEqual(result["seo_value"], "high")
    
    @patch('agents.fact_checker_agent.OpenAI')
    def test_validate_claim_with_flags(self, mock_openai):
        """Test claim validation with flags."""
        # Mock AI validation with concerns
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "is_valid": False,
            "confidence_score": 0.4,
            "reasoning": "Cannot verify this specific statistic",
            "potential_sources": ["Need original study"],
            "flags": ["unverifiable", "needs_source"],
            "seo_value": "low",
            "seo_reasoning": "Too vague without source"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        claim = {
            "id": 1,
            "text": "Some vague claim",
            "type": "fact",
            "context": "No context"
        }
        
        result = self.agent._validate_claim(claim, self.sample_content)
        
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["confidence_score"], 0.4)
        self.assertTrue(result["needs_review"])
        self.assertIn("unverifiable", result["flags"])
    
    def test_assess_seo_impact(self):
        """Test SEO impact assessment."""
        claims = [
            {"id": 1, "text": "Claim 1"},
            {"id": 2, "text": "Claim 2"},
            {"id": 3, "text": "Claim 3"}
        ]
        
        validations = [
            {
                "claim_id": 1,
                "claim_text": "Claim 1",
                "seo_value": "high",
                "seo_reasoning": "Good for featured snippet"
            },
            {
                "claim_id": 2,
                "claim_text": "Claim 2",
                "seo_value": "medium",
                "seo_reasoning": "Moderately useful"
            },
            {
                "claim_id": 3,
                "claim_text": "Claim 3",
                "seo_value": "low",
                "seo_reasoning": "Not very valuable"
            }
        ]
        
        seo_report = self.agent._assess_seo_impact(claims, validations)
        
        self.assertIn("seo_score", seo_report)
        self.assertIn("total_claims", seo_report)
        self.assertIn("seo_distribution", seo_report)
        self.assertIn("recommendations", seo_report)
        self.assertIn("featured_snippet_potential", seo_report)
        
        self.assertEqual(seo_report["total_claims"], 3)
        self.assertEqual(seo_report["seo_distribution"]["high"], 1)
        self.assertEqual(seo_report["seo_distribution"]["medium"], 1)
        self.assertEqual(seo_report["seo_distribution"]["low"], 1)
    
    def test_generate_report(self):
        """Test report generation."""
        claims = [
            {"id": 1, "text": "Claim 1", "type": "statistic"},
            {"id": 2, "text": "Claim 2", "type": "fact"}
        ]
        
        validations = [
            {
                "claim_id": 1,
                "claim_text": "Claim 1",
                "is_valid": True,
                "confidence_score": 0.9,
                "needs_review": False,
                "seo_value": "high"
            },
            {
                "claim_id": 2,
                "claim_text": "Claim 2",
                "is_valid": False,
                "confidence_score": 0.5,
                "needs_review": True,
                "reasoning": "Cannot verify",
                "potential_sources": ["Research needed"],
                "seo_value": "low"
            }
        ]
        
        seo_report = {
            "seo_score": 0.65,
            "total_claims": 2,
            "seo_distribution": {"high": 1, "medium": 0, "low": 1, "unknown": 0},
            "high_value_claims": [],
            "recommendations": ["Add more specific data"],
            "featured_snippet_potential": False
        }
        
        report = self.agent._generate_report(claims, validations, seo_report)
        
        # Check report structure
        self.assertIn("summary", report)
        self.assertIn("claims", report)
        self.assertIn("validations", report)
        self.assertIn("flagged_claims", report)
        self.assertIn("recommendations", report)
        self.assertIn("seo_report", report)
        self.assertIn("generated_at", report)
        self.assertIn("agent", report)
        
        # Check summary content
        summary = report["summary"]
        self.assertEqual(summary["total_claims_extracted"], 2)
        self.assertEqual(summary["flagged_claims"], 1)
        self.assertEqual(summary["valid_claims"], 1)
        self.assertEqual(summary["overall_status"], "review_needed")
        
        # Check flagged claims
        self.assertEqual(len(report["flagged_claims"]), 1)
        self.assertEqual(report["flagged_claims"][0]["claim_text"], "Claim 2")
        
        # Check recommendations
        self.assertGreater(len(report["recommendations"]), 0)
    
    @patch('agents.fact_checker_agent.OpenAI')
    def test_process_complete_workflow(self, mock_openai):
        """Test complete fact-checking workflow."""
        # Mock AI responses for extraction
        extract_response = Mock()
        extract_response.choices = [Mock()]
        extract_response.choices[0].message.content = json.dumps([
            {
                "text": "AI adoption increased by 47%",
                "type": "statistic",
                "context": "Recent studies"
            }
        ])
        
        # Mock AI responses for validation
        validate_response = Mock()
        validate_response.choices = [Mock()]
        validate_response.choices[0].message.content = json.dumps({
            "is_valid": True,
            "confidence_score": 0.85,
            "reasoning": "Verifiable claim",
            "potential_sources": ["Industry reports"],
            "flags": [],
            "seo_value": "high",
            "seo_reasoning": "Specific statistic"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [extract_response, validate_response]
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        report = self.agent.process(self.sample_content)
        
        # Verify report structure
        self.assertIn("summary", report)
        self.assertIn("seo_report", report)
        self.assertEqual(report["agent"], "FactCheckerAgent")
        
        # Verify processing happened
        self.assertGreater(report["summary"]["total_claims_extracted"], 0)
    
    def test_process_invalid_input(self):
        """Test processing with invalid input."""
        invalid_content = {"title": "No content key"}
        
        report = self.agent.process(invalid_content)
        
        self.assertIn("error", report)
        self.assertFalse(report["valid"])
    
    @patch('agents.fact_checker_agent.OpenAI')
    def test_check_article_quality(self, mock_openai):
        """Test quick article quality check."""
        # Mock AI responses
        extract_response = Mock()
        extract_response.choices = [Mock()]
        extract_response.choices[0].message.content = json.dumps([
            {"text": "Claim", "type": "fact", "context": "Context"}
        ])
        
        validate_response = Mock()
        validate_response.choices = [Mock()]
        validate_response.choices[0].message.content = json.dumps({
            "is_valid": True,
            "confidence_score": 0.9,
            "reasoning": "Valid",
            "potential_sources": [],
            "flags": [],
            "seo_value": "high",
            "seo_reasoning": "Good for SEO"
        })
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [extract_response, validate_response]
        mock_openai.return_value = mock_client
        
        self.agent.client = mock_client
        
        quality = self.agent.check_article_quality(self.sample_content)
        
        self.assertIn("quality_score", quality)
        self.assertIn("passes_quality_check", quality)
        self.assertIn("confidence", quality)
        self.assertIn("seo_score", quality)
        self.assertIn("issues_count", quality)
        self.assertIn("recommendation", quality)
        
        self.assertIsInstance(quality["quality_score"], float)
        self.assertIsInstance(quality["passes_quality_check"], bool)


if __name__ == '__main__':
    unittest.main(verbosity=2)
