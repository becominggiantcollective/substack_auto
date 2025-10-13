"""
A/B Testing Framework for content optimization.

Allows testing multiple variations of titles, subtitles, and content styles
to determine what performs best.
"""
import json
import logging
import os
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class ABTestingFramework:
    """Framework for A/B testing content variations."""
    
    def __init__(self, data_dir: str = "generated_content"):
        """Initialize the A/B testing framework.
        
        Args:
            data_dir: Directory for storing test data
        """
        self.data_dir = data_dir
        self.tests_dir = os.path.join(data_dir, "ab_tests")
        os.makedirs(self.tests_dir, exist_ok=True)
        self.active_tests = {}
        logger.info("ABTestingFramework initialized")
    
    def create_test(self, 
                   test_name: str,
                   variations: List[Dict],
                   test_type: str = "title",
                   duration_days: int = 7) -> Dict[str, any]:
        """Create a new A/B test.
        
        Args:
            test_name: Unique name for the test
            variations: List of variations to test (each is a dict with content)
            test_type: Type of test (title, subtitle, content_style, full_post)
            duration_days: How many days to run the test
        
        Returns:
            Test configuration dictionary
        """
        try:
            if not variations or len(variations) < 2:
                raise ValueError("At least 2 variations are required")
            
            test_id = f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            test_config = {
                "test_id": test_id,
                "test_name": test_name,
                "test_type": test_type,
                "variations": [
                    {
                        "variation_id": f"{test_id}_v{i}",
                        "variation_name": v.get("name", f"Variation {i+1}"),
                        "content": v,
                        "metrics": {
                            "views": 0,
                            "engagement": 0,
                            "conversions": 0,
                            "performance_score": 0.0
                        }
                    }
                    for i, v in enumerate(variations)
                ],
                "created_at": datetime.now().isoformat(),
                "duration_days": duration_days,
                "status": "active",
                "winner": None,
                "results": {}
            }
            
            # Save test configuration
            self._save_test(test_config)
            self.active_tests[test_id] = test_config
            
            logger.info(f"Created A/B test: {test_name} with {len(variations)} variations")
            return test_config
            
        except Exception as e:
            logger.error(f"Error creating test: {e}")
            raise
    
    def create_title_test(self, base_content: Dict, title_variations: List[str]) -> Dict[str, any]:
        """Create a test specifically for title variations.
        
        Args:
            base_content: Base content that stays the same
            title_variations: List of different titles to test
        
        Returns:
            Test configuration
        """
        try:
            variations = []
            for i, title in enumerate(title_variations):
                variation = base_content.copy()
                variation["title"] = title
                variation["name"] = f"Title {i+1}: {title[:30]}..."
                variations.append(variation)
            
            return self.create_test(
                test_name="title_optimization",
                variations=variations,
                test_type="title",
                duration_days=7
            )
            
        except Exception as e:
            logger.error(f"Error creating title test: {e}")
            raise
    
    def create_style_test(self, topic: str, styles: List[str]) -> Dict[str, any]:
        """Create a test for different content styles.
        
        Args:
            topic: Topic to write about
            styles: List of style descriptors (e.g., "professional", "casual", "technical")
        
        Returns:
            Test configuration
        """
        try:
            variations = []
            for i, style in enumerate(styles):
                variation = {
                    "name": f"Style: {style}",
                    "topic": topic,
                    "style": style,
                    "instructions": f"Write in a {style} style"
                }
                variations.append(variation)
            
            return self.create_test(
                test_name="style_optimization",
                variations=variations,
                test_type="content_style",
                duration_days=14
            )
            
        except Exception as e:
            logger.error(f"Error creating style test: {e}")
            raise
    
    def record_result(self, test_id: str, variation_id: str, metrics: Dict) -> None:
        """Record results for a specific variation.
        
        Args:
            test_id: ID of the test
            variation_id: ID of the variation
            metrics: Dictionary with performance metrics
        """
        try:
            test = self._load_test(test_id)
            if not test:
                logger.error(f"Test not found: {test_id}")
                return
            
            # Find and update variation
            for variation in test["variations"]:
                if variation["variation_id"] == variation_id:
                    # Update metrics
                    for key, value in metrics.items():
                        if key in variation["metrics"]:
                            variation["metrics"][key] += value
                        else:
                            variation["metrics"][key] = value
                    
                    # Update timestamp
                    variation["last_updated"] = datetime.now().isoformat()
                    break
            
            # Save updated test
            self._save_test(test)
            
            logger.info(f"Recorded results for {variation_id}")
            
        except Exception as e:
            logger.error(f"Error recording result: {e}")
    
    def analyze_test(self, test_id: str) -> Dict[str, any]:
        """Analyze test results and determine winner.
        
        Args:
            test_id: ID of the test to analyze
        
        Returns:
            Analysis results with winner
        """
        try:
            test = self._load_test(test_id)
            if not test:
                raise ValueError(f"Test not found: {test_id}")
            
            variations = test["variations"]
            
            # Calculate performance scores for each variation
            for variation in variations:
                metrics = variation["metrics"]
                
                # Weighted score calculation
                # Adjust weights based on what matters most
                score = (
                    metrics.get("views", 0) * 0.2 +
                    metrics.get("engagement", 0) * 0.4 +
                    metrics.get("conversions", 0) * 0.3 +
                    metrics.get("performance_score", 0) * 0.1
                )
                
                variation["calculated_score"] = score
            
            # Sort by score
            ranked = sorted(variations, key=lambda x: x.get("calculated_score", 0), reverse=True)
            
            winner = ranked[0] if ranked else None
            
            # Calculate confidence level
            if len(ranked) >= 2:
                best_score = ranked[0].get("calculated_score", 0)
                second_score = ranked[1].get("calculated_score", 0)
                
                if second_score > 0:
                    confidence = min(1.0, (best_score - second_score) / second_score)
                else:
                    confidence = 1.0 if best_score > 0 else 0.0
            else:
                confidence = 0.5
            
            analysis = {
                "test_id": test_id,
                "test_name": test["test_name"],
                "winner": {
                    "variation_id": winner["variation_id"],
                    "variation_name": winner["variation_name"],
                    "score": winner.get("calculated_score", 0),
                    "metrics": winner["metrics"]
                } if winner else None,
                "confidence": confidence,
                "rankings": [
                    {
                        "rank": i + 1,
                        "variation_name": v["variation_name"],
                        "score": v.get("calculated_score", 0),
                        "metrics": v["metrics"]
                    }
                    for i, v in enumerate(ranked)
                ],
                "total_variations_tested": len(variations),
                "analyzed_at": datetime.now().isoformat(),
                "recommendation": self._generate_recommendation(winner, confidence) if winner else "Insufficient data"
            }
            
            # Update test with results
            test["results"] = analysis
            test["winner"] = winner["variation_id"] if winner else None
            test["status"] = "completed"
            self._save_test(test)
            
            logger.info(f"Analyzed test {test_id}. Winner: {winner['variation_name'] if winner else 'None'}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing test: {e}")
            raise
    
    def get_test_status(self, test_id: str) -> Dict[str, any]:
        """Get current status of a test.
        
        Args:
            test_id: ID of the test
        
        Returns:
            Status dictionary
        """
        try:
            test = self._load_test(test_id)
            if not test:
                return {"error": "Test not found"}
            
            # Calculate progress
            created = datetime.fromisoformat(test["created_at"])
            duration = test["duration_days"]
            elapsed = (datetime.now() - created).days
            progress = min(1.0, elapsed / duration)
            
            status = {
                "test_id": test_id,
                "test_name": test["test_name"],
                "status": test["status"],
                "progress": progress,
                "days_elapsed": elapsed,
                "days_remaining": max(0, duration - elapsed),
                "variations_count": len(test["variations"]),
                "current_leader": self._get_current_leader(test),
                "total_metrics": self._aggregate_metrics(test)
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting test status: {e}")
            return {"error": str(e)}
    
    def list_active_tests(self) -> List[Dict]:
        """List all active tests.
        
        Returns:
            List of active test summaries
        """
        try:
            active_tests = []
            
            for filename in os.listdir(self.tests_dir):
                if filename.endswith(".json"):
                    test_path = os.path.join(self.tests_dir, filename)
                    with open(test_path, 'r') as f:
                        test = json.load(f)
                    
                    if test.get("status") == "active":
                        active_tests.append({
                            "test_id": test["test_id"],
                            "test_name": test["test_name"],
                            "test_type": test["test_type"],
                            "created_at": test["created_at"],
                            "variations_count": len(test["variations"])
                        })
            
            return active_tests
            
        except Exception as e:
            logger.error(f"Error listing active tests: {e}")
            return []
    
    def _save_test(self, test: Dict) -> None:
        """Save test configuration to file.
        
        Args:
            test: Test configuration dictionary
        """
        test_path = os.path.join(self.tests_dir, f"{test['test_id']}.json")
        with open(test_path, 'w') as f:
            json.dump(test, f, indent=2, default=str)
    
    def _load_test(self, test_id: str) -> Optional[Dict]:
        """Load test configuration from file.
        
        Args:
            test_id: Test ID
        
        Returns:
            Test configuration or None if not found
        """
        test_path = os.path.join(self.tests_dir, f"{test_id}.json")
        if not os.path.exists(test_path):
            return None
        
        with open(test_path, 'r') as f:
            return json.load(f)
    
    def _get_current_leader(self, test: Dict) -> Optional[str]:
        """Get current leading variation.
        
        Args:
            test: Test configuration
        
        Returns:
            Name of leading variation
        """
        variations = test["variations"]
        if not variations:
            return None
        
        # Calculate scores
        scored = []
        for v in variations:
            metrics = v["metrics"]
            score = sum(metrics.values())
            scored.append((v["variation_name"], score))
        
        if scored:
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[0][0]
        
        return None
    
    def _aggregate_metrics(self, test: Dict) -> Dict:
        """Aggregate metrics across all variations.
        
        Args:
            test: Test configuration
        
        Returns:
            Aggregated metrics
        """
        aggregated = defaultdict(int)
        
        for variation in test["variations"]:
            for key, value in variation["metrics"].items():
                if isinstance(value, (int, float)):
                    aggregated[key] += value
        
        return dict(aggregated)
    
    def _generate_recommendation(self, winner: Dict, confidence: float) -> str:
        """Generate recommendation based on test results.
        
        Args:
            winner: Winning variation
            confidence: Confidence score
        
        Returns:
            Recommendation text
        """
        if confidence >= 0.8:
            return f"Strong recommendation: Use '{winner['variation_name']}' - high confidence in superiority"
        elif confidence >= 0.5:
            return f"Moderate recommendation: '{winner['variation_name']}' shows promise - consider longer testing"
        else:
            return f"Weak recommendation: '{winner['variation_name']}' slightly better - need more data"
