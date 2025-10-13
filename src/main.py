"""
Main orchestration module for automated Substack content generation and publishing.
"""
import os
import sys
import logging
import json
from datetime import datetime
from typing import Dict, Optional
import schedule
import time

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content_generators.text_generator import TextGenerator
from content_generators.image_generator import ImageGenerator
from content_generators.video_generator import VideoGenerator
from publishers.substack_publisher import SubstackPublisher
from agents.fact_checker_agent import FactCheckerAgent
from agents.analytics_agent import AnalyticsAgent
from agents.performance_predictor import PerformancePredictorAgent
from agents.topic_trending import TopicTrendingAgent
from agents.ab_testing import ABTestingFramework
from config.settings import settings

# Set up logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('substack_auto.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ContentOrchestrator:
    """Main orchestrator for automated content generation and publishing."""
    
    def __init__(self):
        """Initialize the content orchestrator."""
        self.text_generator = TextGenerator()
        self.image_generator = ImageGenerator()
        self.video_generator = VideoGenerator()
        self.publisher = SubstackPublisher()
        self.fact_checker = FactCheckerAgent()
        self.analytics = AnalyticsAgent(settings.output_dir)
        self.predictor = PerformancePredictorAgent()
        self.trending = TopicTrendingAgent()
        self.ab_testing = ABTestingFramework(settings.output_dir)
        
        # Ensure output directory exists
        os.makedirs(settings.output_dir, exist_ok=True)
        
        # Track posts created today
        self.posts_today = 0
        self.last_post_date = None
    
    def generate_complete_content(self) -> Dict[str, any]:
        """Generate a complete blog post with text, image, and video."""
        try:
            logger.info("Starting complete content generation...")
            
            # Generate text content
            logger.info("Generating text content...")
            post_data = self.text_generator.create_complete_post()
            
            # Generate featured image
            logger.info("Generating featured image...")
            image_result = self.image_generator.generate_featured_image(post_data)
            
            # Generate video
            logger.info("Generating video content...")
            featured_image_path = image_result.get("image_path")
            video_result = self.video_generator.generate_blog_video(post_data, featured_image_path)
            
            # Combine all results
            complete_content = {
                "post_data": post_data,
                "media_files": {
                    "image_path": image_result.get("image_path"),
                    "thumbnail_path": image_result.get("thumbnail_path"),
                    "video_path": video_result.get("video_path")
                },
                "generation_stats": {
                    "text_word_count": post_data.get("word_count", 0),
                    "image_generated": "image_path" in image_result,
                    "video_generated": "video_path" in video_result,
                    "video_duration": video_result.get("duration", 0),
                    "slides_created": video_result.get("slides_created", 0)
                },
                "timestamp": datetime.now().isoformat(),
                "ai_generated": True
            }
            
            # Save content metadata
            self._save_content_metadata(complete_content)
            
            # Fact-check content
            logger.info("Running fact-check on generated content...")
            fact_check_report = self.fact_checker.process(post_data)
            complete_content["fact_check"] = fact_check_report
            
            # Log fact-check summary
            summary = fact_check_report.get("summary", {})
            logger.info(f"Fact-check: {summary.get('valid_claims', 0)}/{summary.get('total_claims_extracted', 0)} claims valid")
            if summary.get("flagged_claims", 0) > 0:
                logger.warning(f"Fact-check: {summary.get('flagged_claims', 0)} claims need review")
            
            logger.info("Complete content generation finished successfully")
            return complete_content
            
        except Exception as e:
            logger.error(f"Error generating complete content: {e}")
            raise
    
    def publish_content(self, content: Dict[str, any]) -> Dict[str, any]:
        """Publish generated content to Substack."""
        try:
            logger.info("Starting content publishing...")
            
            # Validate content before publishing
            validation_result = self.publisher.validate_content(content["post_data"])
            if not validation_result["valid"]:
                logger.error(f"Content validation failed: {validation_result['errors']}")
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            if validation_result["warnings"]:
                logger.warning(f"Content warnings: {validation_result['warnings']}")
            
            # Publish to Substack
            publish_result = self.publisher.publish_complete_post(
                content["post_data"],
                content["media_files"]
            )
            
            if publish_result["success"]:
                logger.info(f"Successfully published: {content['post_data']['title']}")
                
                # Update daily post counter
                today = datetime.now().date()
                if self.last_post_date != today:
                    self.posts_today = 0
                    self.last_post_date = today
                self.posts_today += 1
                
                # Save publication record
                self._save_publication_record(content, publish_result)
            
            return publish_result
            
        except Exception as e:
            logger.error(f"Error publishing content: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_and_publish_post(self) -> Dict[str, any]:
        """Complete workflow: generate and publish a blog post."""
        try:
            # Check daily post limit
            today = datetime.now().date()
            if self.last_post_date == today and self.posts_today >= settings.max_posts_per_day:
                logger.info(f"Daily post limit reached ({settings.max_posts_per_day})")
                return {
                    "success": False,
                    "message": "Daily post limit reached"
                }
            
            logger.info("Starting complete post creation and publishing workflow...")
            
            # Generate content
            content = self.generate_complete_content()
            
            # Publish content
            publish_result = self.publish_content(content)
            
            result = {
                "content_generated": True,
                "publish_result": publish_result,
                "post_title": content["post_data"]["title"],
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("Complete workflow finished")
            return result
            
        except Exception as e:
            logger.error(f"Error in complete workflow: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _save_content_metadata(self, content: Dict[str, any]) -> None:
        """Save content metadata to file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            metadata_file = os.path.join(settings.output_dir, f"content_metadata_{timestamp}.json")
            
            with open(metadata_file, 'w') as f:
                json.dump(content, f, indent=2, default=str)
            
            logger.info(f"Content metadata saved: {metadata_file}")
            
        except Exception as e:
            logger.error(f"Error saving content metadata: {e}")
    
    def _save_publication_record(self, content: Dict[str, any], publish_result: Dict[str, any]) -> None:
        """Save publication record to file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            record_file = os.path.join(settings.output_dir, f"publication_record_{timestamp}.json")
            
            record = {
                "title": content["post_data"]["title"],
                "publish_result": publish_result,
                "content_stats": content["generation_stats"],
                "timestamp": timestamp
            }
            
            with open(record_file, 'w') as f:
                json.dump(record, f, indent=2, default=str)
            
            logger.info(f"Publication record saved: {record_file}")
            
        except Exception as e:
            logger.error(f"Error saving publication record: {e}")
    
    def setup_scheduled_publishing(self) -> None:
        """Set up scheduled publishing based on configuration."""
        try:
            # Parse schedule (simplified - assumes format like "0 9,15,21 * * *")
            # For this demo, we'll set up simple time-based scheduling
            
            # Schedule posts at 9 AM, 3 PM, and 9 PM
            schedule.every().day.at("09:00").do(self.create_and_publish_post)
            schedule.every().day.at("15:00").do(self.create_and_publish_post)
            schedule.every().day.at("21:00").do(self.create_and_publish_post)
            
            logger.info("Scheduled publishing set up successfully")
            logger.info("Posts will be published at 9:00 AM, 3:00 PM, and 9:00 PM daily")
            
        except Exception as e:
            logger.error(f"Error setting up scheduled publishing: {e}")
    
    def run_scheduler(self) -> None:
        """Run the publishing scheduler."""
        logger.info("Starting automated publishing scheduler...")
        logger.info("Press Ctrl+C to stop the scheduler")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")
    
    def get_status(self) -> Dict[str, any]:
        """Get current system status."""
        try:
            pub_stats = self.publisher.get_publication_stats()
            
            # Get analytics insights
            insights = self.analytics.generate_insights()
            
            return {
                "posts_today": self.posts_today,
                "max_posts_per_day": settings.max_posts_per_day,
                "last_post_date": str(self.last_post_date) if self.last_post_date else None,
                "publication_stats": pub_stats,
                "output_directory": settings.output_dir,
                "configured_topics": settings.topics_list,
                "scheduler_active": len(schedule.jobs) > 0,
                "performance_summary": insights.get("summary", {}),
                "active_ab_tests": len(self.ab_testing.list_active_tests()),
                "system_status": "operational"
            }
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {
                "system_status": "error",
                "error": str(e)
            }
    
    def get_analytics_dashboard(self) -> Dict[str, any]:
        """Get comprehensive analytics dashboard.
        
        Returns:
            Dashboard data with metrics and insights
        """
        try:
            dashboard = self.analytics.get_dashboard_data()
            logger.info("Retrieved analytics dashboard")
            return dashboard
        except Exception as e:
            logger.error(f"Error getting analytics dashboard: {e}")
            return {"error": str(e)}
    
    def predict_content_performance(self, post_data: Dict) -> Dict[str, any]:
        """Predict performance of content before publishing.
        
        Args:
            post_data: Post data to analyze
        
        Returns:
            Performance prediction
        """
        try:
            prediction = self.predictor.predict_performance(post_data)
            logger.info(f"Predicted performance: {prediction.get('overall_score', 0):.2f}")
            return prediction
        except Exception as e:
            logger.error(f"Error predicting performance: {e}")
            return {"error": str(e)}
    
    def suggest_trending_topics(self, count: int = 5) -> List[Dict]:
        """Get trending topic suggestions.
        
        Args:
            count: Number of topics to suggest
        
        Returns:
            List of topic suggestions
        """
        try:
            suggestions = self.trending.suggest_content_topics(count)
            logger.info(f"Retrieved {len(suggestions)} trending topic suggestions")
            return suggestions
        except Exception as e:
            logger.error(f"Error getting topic suggestions: {e}")
            return []
    
    def create_ab_test(self, test_name: str, variations: List[Dict], test_type: str = "title") -> Dict[str, any]:
        """Create a new A/B test.
        
        Args:
            test_name: Name for the test
            variations: List of variations to test
            test_type: Type of test (title, subtitle, content_style, full_post)
        
        Returns:
            Test configuration
        """
        try:
            test = self.ab_testing.create_test(test_name, variations, test_type)
            logger.info(f"Created A/B test: {test_name}")
            return test
        except Exception as e:
            logger.error(f"Error creating A/B test: {e}")
            return {"error": str(e)}
    
    def generate_with_prediction(self) -> Dict[str, any]:
        """Generate content with performance prediction.
        
        Returns:
            Content with prediction data
        """
        try:
            logger.info("Generating content with performance prediction...")
            
            # Generate content
            content = self.generate_complete_content()
            
            # Predict performance
            prediction = self.predictor.predict_performance(content["post_data"])
            content["performance_prediction"] = prediction
            
            # Log prediction
            overall_score = prediction.get("overall_score", 0)
            logger.info(f"Performance prediction: {overall_score:.2f}")
            
            if overall_score < 0.5:
                logger.warning("Low predicted performance - consider regenerating")
            
            return content
            
        except Exception as e:
            logger.error(f"Error in generate_with_prediction: {e}")
            raise


def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Substack Content Generator')
    parser.add_argument('--mode', choices=['once', 'schedule'], default='once',
                        help='Run mode: generate one post or run scheduler')
    parser.add_argument('--status', action='store_true',
                        help='Show system status')
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = ContentOrchestrator()
    
    if args.status:
        # Show status
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2))
        return
    
    if args.mode == 'once':
        # Generate and publish one post
        logger.info("Running in single-post mode")
        result = orchestrator.create_and_publish_post()
        print(json.dumps(result, indent=2, default=str))
        
    elif args.mode == 'schedule':
        # Run scheduler
        logger.info("Running in scheduled mode")
        orchestrator.setup_scheduled_publishing()
        orchestrator.run_scheduler()


if __name__ == "__main__":
    main()