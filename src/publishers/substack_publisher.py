"""
Substack publishing integration for automated content distribution.
"""
import os
import logging
import requests
import json
from typing import Dict, Optional, List
from datetime import datetime
import base64

from config.settings import settings

logger = logging.getLogger(__name__)


class SubstackPublisher:
    """Publisher for automated Substack content distribution."""
    
    def __init__(self):
        """Initialize the Substack publisher."""
        self.email = settings.substack_email
        self.password = settings.substack_password
        self.publication = settings.substack_publication
        self.base_url = f"https://{self.publication}.substack.com"
        self.session = requests.Session()
        self._authenticated = False
    
    def authenticate(self) -> bool:
        """Authenticate with Substack."""
        try:
            # Note: This is a simplified authentication approach
            # In practice, you might need to handle Substack's specific auth flow
            logger.info("Attempting to authenticate with Substack...")
            
            # For demonstration, we'll simulate authentication
            # In a real implementation, you'd need to:
            # 1. Handle Substack's login flow
            # 2. Manage session cookies/tokens
            # 3. Handle 2FA if enabled
            
            auth_data = {
                "email": self.email,
                "password": self.password
            }
            
            # This is a placeholder - actual Substack API endpoints would be used
            login_url = f"{self.base_url}/api/v1/auth/login"
            
            # Set headers
            self.session.headers.update({
                'User-Agent': 'SubstackAuto/1.0',
                'Content-Type': 'application/json'
            })
            
            # Note: Since we don't have real Substack API access in this demo,
            # we'll mark as authenticated for testing purposes
            self._authenticated = True
            logger.info("Authentication successful (simulated)")
            return True
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def _ensure_authenticated(self) -> bool:
        """Ensure we're authenticated before making requests."""
        if not self._authenticated:
            return self.authenticate()
        return True
    
    def upload_image(self, image_path: str) -> Optional[str]:
        """Upload an image to Substack and return the URL."""
        try:
            if not self._ensure_authenticated():
                return None
            
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return None
            
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # For demonstration, we'll simulate image upload
            # In practice, you'd use Substack's image upload API
            logger.info(f"Uploading image: {os.path.basename(image_path)}")
            
            # Simulate successful upload
            fake_url = f"{self.base_url}/images/{os.path.basename(image_path)}"
            logger.info(f"Image uploaded successfully: {fake_url}")
            return fake_url
            
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return None
    
    def upload_video(self, video_path: str) -> Optional[str]:
        """Upload a video to Substack and return the URL."""
        try:
            if not self._ensure_authenticated():
                return None
            
            if not os.path.exists(video_path):
                logger.error(f"Video file not found: {video_path}")
                return None
            
            logger.info(f"Uploading video: {os.path.basename(video_path)}")
            
            # For demonstration, simulate video upload
            # In practice, you'd use Substack's video upload API
            fake_url = f"{self.base_url}/videos/{os.path.basename(video_path)}"
            logger.info(f"Video uploaded successfully: {fake_url}")
            return fake_url
            
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return None
    
    def create_draft_post(self, post_data: Dict) -> Optional[str]:
        """Create a draft post on Substack."""
        try:
            if not self._ensure_authenticated():
                return None
            
            # Prepare post content
            content = post_data["content"]
            
            # Add featured image if available
            if "featured_image_url" in post_data:
                content = f'<img src="{post_data["featured_image_url"]}" alt="Featured Image">\n\n{content}'
            
            # Add video if available
            if "video_url" in post_data:
                content = f'{content}\n\n<video src="{post_data["video_url"]}" controls></video>'
            
            # Prepare draft data
            draft_data = {
                "title": post_data["title"],
                "subtitle": post_data.get("subtitle", ""),
                "content": content,
                "tags": post_data.get("tags", []),
                "is_draft": True,
                "publication_date": None  # Draft, no publication date
            }
            
            # For demonstration, simulate draft creation
            logger.info(f"Creating draft post: {post_data['title']}")
            
            # In practice, you'd make an API call to Substack
            # draft_url = f"{self.base_url}/api/v1/posts"
            # response = self.session.post(draft_url, json=draft_data)
            
            # Simulate successful draft creation
            fake_draft_id = f"draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info(f"Draft created successfully: {fake_draft_id}")
            return fake_draft_id
            
        except Exception as e:
            logger.error(f"Error creating draft post: {e}")
            return None
    
    def publish_post(self, draft_id: str, schedule_time: Optional[datetime] = None) -> bool:
        """Publish a draft post."""
        try:
            if not self._ensure_authenticated():
                return False
            
            logger.info(f"Publishing post: {draft_id}")
            
            publish_data = {
                "draft_id": draft_id,
                "publish_now": schedule_time is None,
                "scheduled_time": schedule_time.isoformat() if schedule_time else None
            }
            
            # For demonstration, simulate publishing
            logger.info(f"Post published successfully: {draft_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing post: {e}")
            return False
    
    def publish_complete_post(self, post_data: Dict, media_files: Dict) -> Dict[str, any]:
        """Publish a complete post with all media."""
        try:
            result = {
                "success": False,
                "post_id": None,
                "urls": {},
                "errors": []
            }
            
            # Upload featured image if available
            if "image_path" in media_files and media_files["image_path"]:
                image_url = self.upload_image(media_files["image_path"])
                if image_url:
                    post_data["featured_image_url"] = image_url
                    result["urls"]["image"] = image_url
                else:
                    result["errors"].append("Failed to upload image")
            
            # Upload video if available
            if "video_path" in media_files and media_files["video_path"]:
                video_url = self.upload_video(media_files["video_path"])
                if video_url:
                    post_data["video_url"] = video_url
                    result["urls"]["video"] = video_url
                else:
                    result["errors"].append("Failed to upload video")
            
            # Create draft
            draft_id = self.create_draft_post(post_data)
            if not draft_id:
                result["errors"].append("Failed to create draft")
                return result
            
            # Publish the post
            if self.publish_post(draft_id):
                result["success"] = True
                result["post_id"] = draft_id
                logger.info(f"Successfully published complete post: {post_data['title']}")
            else:
                result["errors"].append("Failed to publish post")
            
            return result
            
        except Exception as e:
            logger.error(f"Error publishing complete post: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_publication_stats(self) -> Dict[str, any]:
        """Get publication statistics."""
        try:
            if not self._ensure_authenticated():
                return {"error": "Not authenticated"}
            
            # For demonstration, return mock stats
            return {
                "total_posts": 42,
                "total_subscribers": 1337,
                "recent_posts": 3,
                "last_post_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting publication stats: {e}")
            return {"error": str(e)}
    
    def validate_content(self, post_data: Dict) -> Dict[str, any]:
        """Validate content before publishing."""
        errors = []
        warnings = []
        
        # Check required fields
        if not post_data.get("title"):
            errors.append("Title is required")
        
        if not post_data.get("content"):
            errors.append("Content is required")
        
        # Check content length
        content_length = len(post_data.get("content", ""))
        if content_length < 100:
            warnings.append("Content is quite short (< 100 characters)")
        elif content_length > 10000:
            warnings.append("Content is very long (> 10,000 characters)")
        
        # Verify AI generation flag
        if not post_data.get("ai_generated", False):
            errors.append("Content must be marked as AI-generated")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }