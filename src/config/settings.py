"""
Configuration settings for the automated Substack content generation system.
"""
import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    
    # Substack Configuration
    substack_email: str = Field(..., env="SUBSTACK_EMAIL")
    substack_password: str = Field(..., env="SUBSTACK_PASSWORD")
    substack_publication: str = Field(..., env="SUBSTACK_PUBLICATION")
    
    # Content Generation Settings
    max_posts_per_day: int = Field(3, env="MAX_POSTS_PER_DAY")
    content_topics: str = Field("technology,AI,innovation,science", env="CONTENT_TOPICS")
    image_style: str = Field("digital art,modern,professional", env="IMAGE_STYLE")
    video_duration: int = Field(30, env="VIDEO_DURATION")
    
    # AI Prompt Customization Settings
    content_tone: str = Field("professional and engaging", env="CONTENT_TONE")
    target_audience: str = Field("intelligent general audience", env="TARGET_AUDIENCE")
    content_style: str = Field("informative and thought-provoking", env="CONTENT_STYLE")
    custom_instructions: str = Field("", env="CUSTOM_INSTRUCTIONS")
    
    # Publishing Schedule
    publish_schedule: str = Field("0 9,15,21 * * *", env="PUBLISH_SCHEDULE")
    
    # File Paths
    output_dir: str = Field("generated_content", env="OUTPUT_DIR")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @property
    def topics_list(self) -> List[str]:
        """Get content topics as a list."""
        return [topic.strip() for topic in self.content_topics.split(",")]
    
    @property
    def image_styles_list(self) -> List[str]:
        """Get image styles as a list."""
        return [style.strip() for style in self.image_style.split(",")]


# Global settings instance
settings = Settings()