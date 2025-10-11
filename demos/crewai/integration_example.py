"""
CrewAI Integration Example for Substack Auto
=============================================

This file demonstrates how CrewAI can be integrated into the existing
Substack Auto architecture with minimal changes to the current codebase.

This is a proposed integration that would replace or augment the existing
TextGenerator class with a multi-agent CrewAI workflow.
"""

from typing import Dict, Any, List
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileReadTool
import os


class CrewAIContentGenerator:
    """
    Drop-in replacement for TextGenerator using CrewAI multi-agent system.
    
    This class maintains the same interface as the existing TextGenerator
    to minimize integration changes, but uses CrewAI agents internally.
    """
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the CrewAI content generator.
        
        Args:
            openai_api_key: OpenAI API key (optional if set in environment)
        """
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Initialize tools if API keys available
        self.search_tool = None
        try:
            if os.getenv("SERPER_API_KEY"):
                self.search_tool = SerperDevTool()
        except Exception:
            pass
        
        # Create agents once during initialization for efficiency
        self._seo_researcher = self._create_seo_researcher()
        self._content_writer = self._create_content_writer()
        self._seo_optimizer = self._create_seo_optimizer()
    
    def _create_seo_researcher(self) -> Agent:
        """Create SEO research specialist agent."""
        return Agent(
            role='SEO Research Specialist',
            goal='Research keywords, trends, and search intent for content topics',
            backstory="""Expert SEO researcher who analyzes search trends, 
            identifies high-value keywords, and understands user search intent.""",
            tools=[self.search_tool] if self.search_tool else [],
            verbose=False,
            allow_delegation=False
        )
    
    def _create_content_writer(self) -> Agent:
        """Create content writer agent."""
        return Agent(
            role='Senior Content Writer',
            goal='Create engaging, well-structured blog posts',
            backstory="""Experienced content writer specializing in creating 
            informative, engaging articles that provide real value to readers.""",
            verbose=False,
            allow_delegation=False
        )
    
    def _create_seo_optimizer(self) -> Agent:
        """Create SEO optimization agent."""
        return Agent(
            role='SEO Optimizer',
            goal='Optimize content for search engines without sacrificing quality',
            backstory="""SEO expert who optimizes content structure, keywords, 
            and metadata for maximum search visibility.""",
            verbose=False,
            allow_delegation=False
        )
    
    def generate_topic(self) -> str:
        """
        Generate a creative topic for a blog post.
        
        Maintains compatibility with existing TextGenerator interface.
        
        Returns:
            str: Generated topic title
        """
        # Simple task for topic generation
        task = Task(
            description="""Generate a compelling blog post topic that is:
            - Relevant to current trends
            - Interesting to a general audience
            - Suitable for a 1000+ word article
            
            Return only the topic title, nothing else.""",
            agent=self._seo_researcher,
            expected_output="A single topic title"
        )
        
        crew = Crew(
            agents=[self._seo_researcher],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return str(result).strip()
    
    def generate_blog_post(self, topic: str) -> Dict[str, str]:
        """
        Generate a complete blog post for the given topic.
        
        Maintains compatibility with existing TextGenerator interface.
        
        Args:
            topic: The blog post topic
        
        Returns:
            Dict with 'title', 'subtitle', and 'content' keys
        """
        # Task 1: SEO Research
        research_task = Task(
            description=f"""Research SEO strategy for topic: "{topic}"
            Provide:
            - 5 key keywords
            - Recommended structure (headers)
            - Key points to cover""",
            agent=self._seo_researcher,
            expected_output="SEO research brief with keywords and structure"
        )
        
        # Task 2: Content Writing
        writing_task = Task(
            description=f"""Write a comprehensive blog post about: "{topic}"
            
            Use the SEO research to inform your writing.
            
            Requirements:
            - 1000-1200 words
            - Engaging introduction
            - Clear sections with headers
            - Practical insights
            - Strong conclusion
            
            Return: Complete blog post content (body only)""",
            agent=self._content_writer,
            expected_output="Complete blog post of 1000-1200 words",
            context=[research_task]
        )
        
        # Task 3: Create title and subtitle
        metadata_task = Task(
            description=f"""Create compelling title and subtitle for the blog post.
            
            Title: SEO-optimized, 60 characters or less
            Subtitle: Engaging description, 1-2 sentences
            
            Format your response as:
            TITLE: [title]
            SUBTITLE: [subtitle]""",
            agent=self._seo_optimizer,
            expected_output="Title and subtitle in specified format",
            context=[research_task, writing_task]
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[self._seo_researcher, self._content_writer, self._seo_optimizer],
            tasks=[research_task, writing_task, metadata_task],
            process=Process.sequential,
            verbose=False
        )
        
        # Get results
        result = crew.kickoff()
        
        # Parse the metadata result
        result_str = str(result)
        title = topic  # fallback
        subtitle = ""
        
        if "TITLE:" in result_str:
            lines = result_str.split('\n')
            for line in lines:
                if line.startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                elif line.startswith("SUBTITLE:"):
                    subtitle = line.replace("SUBTITLE:", "").strip()
        
        # Get content from writing task
        content = str(writing_task.output) if hasattr(writing_task, 'output') else ""
        
        return {
            "title": title,
            "subtitle": subtitle,
            "content": content
        }
    
    def generate_tags(self, title: str, content: str) -> List[str]:
        """
        Generate relevant tags for the blog post.
        
        Maintains compatibility with existing TextGenerator interface.
        
        Args:
            title: Blog post title
            content: Blog post content
        
        Returns:
            List of tag strings
        """
        task = Task(
            description=f"""Generate 5-8 relevant tags for this blog post:
            
            Title: {title}
            Content: {content[:500]}...
            
            Return tags as a comma-separated list.""",
            agent=self._seo_optimizer,
            expected_output="Comma-separated list of tags"
        )
        
        crew = Crew(
            agents=[self._seo_optimizer],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        tags_str = str(result).strip()
        
        # Parse comma-separated tags
        tags = [tag.strip() for tag in tags_str.split(',')]
        return tags[:8]  # Limit to 8 tags
    
    def create_complete_post(self) -> Dict[str, Any]:
        """
        Generate a complete blog post with all components.
        
        Maintains full compatibility with existing TextGenerator interface.
        
        Returns:
            Dict containing all blog post components
        """
        # Generate topic
        topic = self.generate_topic()
        
        # Generate full post
        post = self.generate_blog_post(topic)
        
        # Generate tags
        tags = self.generate_tags(post['title'], post['content'])
        
        # Calculate word count
        word_count = len(post['content'].split())
        
        return {
            "topic": topic,
            "title": post['title'],
            "subtitle": post['subtitle'],
            "content": post['content'],
            "tags": tags,
            "word_count": word_count,
            "ai_generated": True
        }


# Integration example: How to use in existing ContentOrchestrator
def integration_example():
    """
    Example showing how to integrate CrewAI into existing Substack Auto.
    
    In src/main.py, replace:
        from content_generators.text_generator import TextGenerator
    
    With:
        from agents.crewai_generator import CrewAIContentGenerator as TextGenerator
    
    No other code changes needed due to compatible interface!
    """
    
    # Old way (existing code):
    # from content_generators.text_generator import TextGenerator
    # text_generator = TextGenerator()
    
    # New way (with CrewAI):
    from agents.crewai_generator import CrewAIContentGenerator as TextGenerator
    text_generator = CrewAIContentGenerator()
    
    # Rest of the code works exactly the same!
    post_data = text_generator.create_complete_post()
    
    print("Generated post:", post_data['title'])
    return post_data


if __name__ == "__main__":
    """Test the CrewAI integration."""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable to test")
    else:
        print("🧪 Testing CrewAI Integration...")
        
        generator = CrewAIContentGenerator()
        
        # Test topic generation
        print("\n1️⃣ Generating topic...")
        topic = generator.generate_topic()
        print(f"   Topic: {topic}")
        
        # Test blog post generation
        print("\n2️⃣ Generating blog post...")
        post = generator.generate_blog_post(topic)
        print(f"   Title: {post['title']}")
        print(f"   Subtitle: {post['subtitle']}")
        print(f"   Content length: {len(post['content'])} characters")
        
        # Test tag generation
        print("\n3️⃣ Generating tags...")
        tags = generator.generate_tags(post['title'], post['content'])
        print(f"   Tags: {', '.join(tags)}")
        
        print("\n✅ Integration test complete!")
