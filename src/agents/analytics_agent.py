"""
Analytics Agent for tracking content performance and providing insights.

This agent monitors publication metrics, engagement patterns, and provides
actionable insights to improve content strategy.
"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class AnalyticsAgent:
    """Agent for tracking and analyzing content performance."""
    
    def __init__(self, data_dir: str = "generated_content"):
        """Initialize the analytics agent.
        
        Args:
            data_dir: Directory containing publication records
        """
        self.data_dir = data_dir
        self.metrics_cache = {}
        self.insights_cache = {}
        logger.info("AnalyticsAgent initialized")
    
    def collect_metrics(self) -> Dict[str, any]:
        """Collect metrics from all publication records.
        
        Returns:
            Dictionary containing aggregated metrics
        """
        try:
            metrics = {
                "total_posts": 0,
                "posts_by_date": defaultdict(int),
                "posts_by_topic": defaultdict(int),
                "word_counts": [],
                "video_durations": [],
                "fact_check_scores": [],
                "seo_scores": [],
                "generation_times": [],
                "recent_posts": []
            }
            
            # Scan all publication records
            if not os.path.exists(self.data_dir):
                logger.warning(f"Data directory not found: {self.data_dir}")
                return metrics
            
            for filename in os.listdir(self.data_dir):
                if filename.startswith("publication_record_") and filename.endswith(".json"):
                    record_path = os.path.join(self.data_dir, filename)
                    try:
                        with open(record_path, 'r') as f:
                            record = json.load(f)
                        
                        metrics["total_posts"] += 1
                        
                        # Extract timestamp
                        timestamp = record.get("timestamp", "")
                        if timestamp:
                            date = timestamp[:8]  # YYYYMMDD format
                            metrics["posts_by_date"][date] += 1
                        
                        # Extract content stats
                        stats = record.get("content_stats", {})
                        if "text_word_count" in stats:
                            metrics["word_counts"].append(stats["text_word_count"])
                        if "video_duration" in stats:
                            metrics["video_durations"].append(stats["video_duration"])
                        
                        # Store recent posts
                        metrics["recent_posts"].append({
                            "title": record.get("title", "Unknown"),
                            "timestamp": timestamp,
                            "stats": stats
                        })
                        
                    except Exception as e:
                        logger.error(f"Error reading record {filename}: {e}")
                        continue
            
            # Also scan content metadata for additional info
            for filename in os.listdir(self.data_dir):
                if filename.startswith("content_metadata_") and filename.endswith(".json"):
                    metadata_path = os.path.join(self.data_dir, filename)
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        
                        # Extract fact check scores
                        fact_check = metadata.get("fact_check", {})
                        if "summary" in fact_check:
                            summary = fact_check["summary"]
                            if "valid_claims" in summary and "total_claims_extracted" in summary:
                                total = summary["total_claims_extracted"]
                                valid = summary["valid_claims"]
                                if total > 0:
                                    score = valid / total
                                    metrics["fact_check_scores"].append(score)
                        
                        # Extract SEO scores
                        if "seo_report" in fact_check:
                            seo = fact_check["seo_report"]
                            if "seo_score" in seo:
                                metrics["seo_scores"].append(seo["seo_score"])
                        
                        # Extract topics from post data
                        post_data = metadata.get("post_data", {})
                        tags = post_data.get("tags", [])
                        for tag in tags:
                            metrics["posts_by_topic"][tag] += 1
                        
                    except Exception as e:
                        logger.error(f"Error reading metadata {filename}: {e}")
                        continue
            
            # Sort recent posts by timestamp
            metrics["recent_posts"] = sorted(
                metrics["recent_posts"], 
                key=lambda x: x["timestamp"], 
                reverse=True
            )[:10]
            
            # Convert defaultdicts to regular dicts
            metrics["posts_by_date"] = dict(metrics["posts_by_date"])
            metrics["posts_by_topic"] = dict(metrics["posts_by_topic"])
            
            self.metrics_cache = metrics
            logger.info(f"Collected metrics for {metrics['total_posts']} posts")
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {}
    
    def generate_insights(self, metrics: Optional[Dict] = None) -> Dict[str, any]:
        """Generate actionable insights from metrics.
        
        Args:
            metrics: Optional pre-collected metrics. If None, will collect fresh metrics.
        
        Returns:
            Dictionary containing insights and recommendations
        """
        try:
            if metrics is None:
                metrics = self.collect_metrics()
            
            insights = {
                "summary": {},
                "trends": [],
                "recommendations": [],
                "alerts": [],
                "performance_scores": {}
            }
            
            total_posts = metrics.get("total_posts", 0)
            
            if total_posts == 0:
                insights["summary"]["message"] = "No posts published yet"
                return insights
            
            # Calculate summary statistics
            word_counts = metrics.get("word_counts", [])
            if word_counts:
                insights["summary"]["avg_word_count"] = sum(word_counts) / len(word_counts)
                insights["summary"]["min_word_count"] = min(word_counts)
                insights["summary"]["max_word_count"] = max(word_counts)
            
            video_durations = metrics.get("video_durations", [])
            if video_durations:
                insights["summary"]["avg_video_duration"] = sum(video_durations) / len(video_durations)
            
            fact_scores = metrics.get("fact_check_scores", [])
            if fact_scores:
                avg_fact_score = sum(fact_scores) / len(fact_scores)
                insights["summary"]["avg_fact_check_score"] = avg_fact_score
                insights["performance_scores"]["content_accuracy"] = avg_fact_score
                
                if avg_fact_score < 0.7:
                    insights["alerts"].append({
                        "level": "warning",
                        "message": f"Fact check score is below recommended threshold: {avg_fact_score:.2f}",
                        "suggestion": "Review AI prompts to improve factual accuracy"
                    })
            
            seo_scores = metrics.get("seo_scores", [])
            if seo_scores:
                avg_seo_score = sum(seo_scores) / len(seo_scores)
                insights["summary"]["avg_seo_score"] = avg_seo_score
                insights["performance_scores"]["seo_optimization"] = avg_seo_score
                
                if avg_seo_score < 0.6:
                    insights["recommendations"].append({
                        "priority": "high",
                        "category": "SEO",
                        "message": "SEO scores are below optimal",
                        "actions": [
                            "Include more specific statistics and data",
                            "Add more structured content (lists, headers)",
                            "Focus on featured snippet optimization"
                        ]
                    })
            
            # Analyze posting frequency
            posts_by_date = metrics.get("posts_by_date", {})
            if posts_by_date:
                dates = sorted(posts_by_date.keys())
                if len(dates) >= 2:
                    first_date = datetime.strptime(dates[0], "%Y%m%d")
                    last_date = datetime.strptime(dates[-1], "%Y%m%d")
                    days_span = (last_date - first_date).days + 1
                    avg_posts_per_day = total_posts / days_span
                    
                    insights["summary"]["posting_frequency"] = avg_posts_per_day
                    insights["summary"]["active_days"] = days_span
                    
                    if avg_posts_per_day < 1:
                        insights["recommendations"].append({
                            "priority": "medium",
                            "category": "Frequency",
                            "message": "Consider increasing posting frequency",
                            "actions": [
                                "Schedule more posts per day",
                                "Adjust MAX_POSTS_PER_DAY setting"
                            ]
                        })
            
            # Analyze topic distribution
            posts_by_topic = metrics.get("posts_by_topic", {})
            if posts_by_topic:
                top_topics = sorted(posts_by_topic.items(), key=lambda x: x[1], reverse=True)[:5]
                insights["trends"].append({
                    "type": "topics",
                    "message": "Most popular topics",
                    "data": [{"topic": t[0], "count": t[1]} for t in top_topics]
                })
                
                # Check for topic diversity
                if len(posts_by_topic) < 3:
                    insights["recommendations"].append({
                        "priority": "medium",
                        "category": "Content Diversity",
                        "message": "Limited topic diversity detected",
                        "actions": [
                            "Expand CONTENT_TOPICS configuration",
                            "Experiment with emerging topics in your niche"
                        ]
                    })
            
            # Calculate overall performance score
            if insights["performance_scores"]:
                overall_score = sum(insights["performance_scores"].values()) / len(insights["performance_scores"])
                insights["performance_scores"]["overall"] = overall_score
                
                if overall_score >= 0.8:
                    insights["summary"]["status"] = "excellent"
                elif overall_score >= 0.6:
                    insights["summary"]["status"] = "good"
                else:
                    insights["summary"]["status"] = "needs_improvement"
            
            self.insights_cache = insights
            logger.info("Generated insights successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return {"error": str(e)}
    
    def get_dashboard_data(self) -> Dict[str, any]:
        """Get comprehensive dashboard data.
        
        Returns:
            Dictionary containing metrics, insights, and visualizations
        """
        try:
            metrics = self.collect_metrics()
            insights = self.generate_insights(metrics)
            
            dashboard = {
                "last_updated": datetime.now().isoformat(),
                "metrics": metrics,
                "insights": insights,
                "quick_stats": {
                    "total_posts": metrics.get("total_posts", 0),
                    "avg_word_count": insights["summary"].get("avg_word_count", 0),
                    "avg_fact_score": insights["summary"].get("avg_fact_check_score", 0),
                    "avg_seo_score": insights["summary"].get("avg_seo_score", 0),
                    "overall_performance": insights["performance_scores"].get("overall", 0)
                },
                "recent_activity": metrics.get("recent_posts", [])[:5]
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error generating dashboard data: {e}")
            return {"error": str(e)}
    
    def export_report(self, output_file: str = "analytics_report.json") -> str:
        """Export analytics report to file.
        
        Args:
            output_file: Path to output file
        
        Returns:
            Path to exported file
        """
        try:
            dashboard_data = self.get_dashboard_data()
            
            output_path = os.path.join(self.data_dir, output_file)
            with open(output_path, 'w') as f:
                json.dump(dashboard_data, f, indent=2, default=str)
            
            logger.info(f"Analytics report exported to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting report: {e}")
            raise
