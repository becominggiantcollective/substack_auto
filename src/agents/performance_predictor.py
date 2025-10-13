"""
Content Performance Predictor Agent.

Uses AI to predict the potential success of content before publishing.
Analyzes factors like title appeal, content quality, SEO potential, and more.
"""
import json
import logging
from typing import Dict, List
from openai import OpenAI

logger = logging.getLogger(__name__)


class PerformancePredictorAgent:
    """Predicts content performance before publishing."""
    
    def __init__(self, api_key: str = None):
        """Initialize the performance predictor agent.
        
        Args:
            api_key: OpenAI API key (if None, will load from settings)
        """
        if api_key is None:
            from config.settings import settings
            api_key = settings.openai_api_key
        
        self.client = OpenAI(api_key=api_key)
        logger.info("PerformancePredictorAgent initialized")
    
    def predict_performance(self, post_data: Dict) -> Dict[str, any]:
        """Predict the performance of a blog post.
        
        Args:
            post_data: Dictionary containing title, subtitle, content, tags
        
        Returns:
            Dictionary with predictions and scores
        """
        try:
            title = post_data.get("title", "")
            subtitle = post_data.get("subtitle", "")
            content = post_data.get("content", "")
            tags = post_data.get("tags", [])
            
            # Validate inputs
            if not title or not content:
                raise ValueError("Title and content are required")
            
            # Create analysis prompt
            analysis_prompt = f"""Analyze this blog post and predict its performance potential.

Title: {title}
Subtitle: {subtitle}
Tags: {', '.join(tags)}

Content (first 500 chars):
{content[:500]}...

Evaluate and score (0.0-1.0) the following factors:
1. Title Appeal - How catchy and compelling is the title?
2. Topic Relevance - How relevant and timely is the topic?
3. Readability - How easy is it to read and understand?
4. Engagement Potential - How likely to generate comments/shares?
5. SEO Potential - How well optimized for search engines?
6. Content Depth - How comprehensive and valuable is the content?

Provide scores and reasoning for each factor.
Also provide:
- Overall success probability (0.0-1.0)
- Expected audience (small/medium/large)
- Best publishing time (morning/afternoon/evening)
- Suggested improvements (list of 3-5 actionable items)

Format your response as JSON with this structure:
{{
  "factors": {{
    "title_appeal": {{"score": 0.0-1.0, "reasoning": "..."}},
    "topic_relevance": {{"score": 0.0-1.0, "reasoning": "..."}},
    "readability": {{"score": 0.0-1.0, "reasoning": "..."}},
    "engagement_potential": {{"score": 0.0-1.0, "reasoning": "..."}},
    "seo_potential": {{"score": 0.0-1.0, "reasoning": "..."}},
    "content_depth": {{"score": 0.0-1.0, "reasoning": "..."}}
  }},
  "overall_prediction": {{
    "success_probability": 0.0-1.0,
    "confidence": 0.0-1.0,
    "expected_audience_size": "small/medium/large"
  }},
  "recommendations": {{
    "best_publish_time": "morning/afternoon/evening",
    "best_publish_day": "weekday/weekend",
    "improvements": ["item1", "item2", "item3"]
  }}
}}"""
            
            logger.info("Requesting performance prediction from AI...")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content strategist and data analyst specializing in predicting content performance."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3
            )
            
            prediction_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            # Remove markdown code blocks if present
            if "```json" in prediction_text:
                prediction_text = prediction_text.split("```json")[1].split("```")[0].strip()
            elif "```" in prediction_text:
                prediction_text = prediction_text.split("```")[1].split("```")[0].strip()
            
            prediction = json.loads(prediction_text)
            
            # Calculate overall score
            factor_scores = []
            for factor, data in prediction.get("factors", {}).items():
                if isinstance(data, dict) and "score" in data:
                    factor_scores.append(data["score"])
            
            if factor_scores:
                prediction["overall_score"] = sum(factor_scores) / len(factor_scores)
            
            # Add metadata
            prediction["analyzed_title"] = title
            prediction["analyzed_at"] = self._get_timestamp()
            prediction["word_count"] = len(content.split())
            
            logger.info(f"Performance predicted: {prediction.get('overall_score', 0):.2f} overall score")
            return prediction
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing AI response: {e}")
            # Return fallback prediction
            return self._get_fallback_prediction(post_data)
        except Exception as e:
            logger.error(f"Error predicting performance: {e}")
            return self._get_fallback_prediction(post_data)
    
    def _get_fallback_prediction(self, post_data: Dict) -> Dict[str, any]:
        """Generate a basic prediction when AI fails.
        
        Args:
            post_data: Post data dictionary
        
        Returns:
            Basic prediction dictionary
        """
        content_length = len(post_data.get("content", ""))
        title_length = len(post_data.get("title", ""))
        has_subtitle = bool(post_data.get("subtitle"))
        tags_count = len(post_data.get("tags", []))
        
        # Simple heuristic scoring
        length_score = min(1.0, content_length / 1500) * 0.8
        title_score = 0.7 if 30 <= title_length <= 80 else 0.5
        structure_score = 0.8 if has_subtitle else 0.6
        tags_score = min(1.0, tags_count / 5) * 0.7
        
        overall_score = (length_score + title_score + structure_score + tags_score) / 4
        
        return {
            "factors": {
                "title_appeal": {"score": title_score, "reasoning": "Based on title length"},
                "topic_relevance": {"score": 0.7, "reasoning": "Default score"},
                "readability": {"score": length_score, "reasoning": "Based on content length"},
                "engagement_potential": {"score": structure_score, "reasoning": "Based on structure"},
                "seo_potential": {"score": tags_score, "reasoning": "Based on tags count"},
                "content_depth": {"score": length_score, "reasoning": "Based on content length"}
            },
            "overall_prediction": {
                "success_probability": overall_score,
                "confidence": 0.5,
                "expected_audience_size": "medium"
            },
            "recommendations": {
                "best_publish_time": "morning",
                "best_publish_day": "weekday",
                "improvements": [
                    "Consider adding more specific examples",
                    "Optimize title for SEO",
                    "Add more tags for better discoverability"
                ]
            },
            "overall_score": overall_score,
            "analyzed_title": post_data.get("title", "Unknown"),
            "analyzed_at": self._get_timestamp(),
            "word_count": len(post_data.get("content", "").split()),
            "note": "Fallback prediction - AI analysis unavailable"
        }
    
    def compare_variations(self, variations: List[Dict]) -> Dict[str, any]:
        """Compare multiple content variations and rank them.
        
        Args:
            variations: List of post_data dictionaries to compare
        
        Returns:
            Comparison report with rankings
        """
        try:
            if not variations:
                raise ValueError("At least one variation is required")
            
            predictions = []
            for i, variation in enumerate(variations):
                logger.info(f"Analyzing variation {i+1}/{len(variations)}...")
                prediction = self.predict_performance(variation)
                prediction["variation_index"] = i
                prediction["variation_label"] = variation.get("label", f"Variation {i+1}")
                predictions.append(prediction)
            
            # Rank by overall score
            ranked = sorted(predictions, key=lambda x: x.get("overall_score", 0), reverse=True)
            
            comparison = {
                "total_variations": len(variations),
                "best_variation": ranked[0]["variation_label"],
                "best_score": ranked[0].get("overall_score", 0),
                "rankings": [
                    {
                        "rank": i + 1,
                        "label": pred["variation_label"],
                        "score": pred.get("overall_score", 0),
                        "success_probability": pred.get("overall_prediction", {}).get("success_probability", 0)
                    }
                    for i, pred in enumerate(ranked)
                ],
                "detailed_predictions": ranked,
                "compared_at": self._get_timestamp()
            }
            
            logger.info(f"Compared {len(variations)} variations. Best: {comparison['best_variation']}")
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing variations: {e}")
            raise
    
    def get_improvement_suggestions(self, post_data: Dict) -> List[str]:
        """Get specific suggestions to improve content performance.
        
        Args:
            post_data: Post data dictionary
        
        Returns:
            List of actionable improvement suggestions
        """
        try:
            prediction = self.predict_performance(post_data)
            
            suggestions = prediction.get("recommendations", {}).get("improvements", [])
            
            # Add factor-specific suggestions for low scores
            factors = prediction.get("factors", {})
            for factor_name, factor_data in factors.items():
                if isinstance(factor_data, dict):
                    score = factor_data.get("score", 1.0)
                    if score < 0.6:
                        if factor_name == "title_appeal":
                            suggestions.append("Consider revising the title to be more compelling and specific")
                        elif factor_name == "topic_relevance":
                            suggestions.append("Research current trends to ensure topic is timely and relevant")
                        elif factor_name == "readability":
                            suggestions.append("Simplify language and break content into shorter paragraphs")
                        elif factor_name == "engagement_potential":
                            suggestions.append("Add questions, calls-to-action, or controversial points to spark engagement")
                        elif factor_name == "seo_potential":
                            suggestions.append("Include more keywords, statistics, and structured content")
                        elif factor_name == "content_depth":
                            suggestions.append("Expand content with more examples, data, and detailed explanations")
            
            return list(set(suggestions))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error getting improvement suggestions: {e}")
            return ["Review content quality and structure", "Consider audience engagement"]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
