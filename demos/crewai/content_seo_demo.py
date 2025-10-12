"""
CrewAI Demo: Content Generation + SEO Optimization Workflow
============================================================

This demo showcases how CrewAI can be used to create a multi-agent system
for generating SEO-optimized content for Substack Auto.

Agents:
- SEO Researcher: Conducts keyword research and competitor analysis
- Content Writer: Creates engaging blog posts
- SEO Optimizer: Optimizes content for search engines
- Editor: Reviews and polishes final content

Workflow:
SEO Research → Content Creation → SEO Optimization → Final Review
"""

import os
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool

# Optional: Set environment variables for demo
# os.environ["OPENAI_API_KEY"] = "your-api-key"
# os.environ["SERPER_API_KEY"] = "your-serper-api-key"  # For web search


class ContentSEOCrew:
    """CrewAI-powered content generation with SEO optimization."""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the content SEO crew.
        
        Args:
            openai_api_key: OpenAI API key (optional, will use env var if not provided)
        """
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Initialize tools (some require API keys)
        self.search_tool = None
        try:
            # SerperDevTool requires SERPER_API_KEY
            if os.getenv("SERPER_API_KEY"):
                self.search_tool = SerperDevTool()
        except Exception:
            pass
        
        self.scrape_tool = ScrapeWebsiteTool()
    
    def create_agents(self) -> tuple[Agent, Agent, Agent, Agent]:
        """Create the four specialized agents for content creation.
        
        Returns:
            Tuple of (seo_researcher, content_writer, seo_optimizer, editor)
        """
        
        # Agent 1: SEO Researcher
        seo_researcher = Agent(
            role='SEO Research Specialist',
            goal='Research trending topics, keywords, and competitor content to inform content strategy',
            backstory="""You are an expert SEO researcher with deep knowledge of 
            keyword research, search trends, and competitive analysis. You understand 
            what makes content rank well in search engines and can identify opportunities 
            for high-performing content. You stay updated on the latest SEO best practices 
            and search engine algorithm changes.""",
            tools=[self.search_tool] if self.search_tool else [],
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 2: Content Writer
        content_writer = Agent(
            role='Senior Content Writer',
            goal='Create engaging, informative, and well-structured blog posts that resonate with readers',
            backstory="""You are a skilled content writer with years of experience 
            in creating compelling blog posts. You know how to hook readers with 
            captivating introductions, structure content for readability, and include 
            practical insights that provide real value. Your writing is clear, engaging, 
            and authoritative while remaining accessible to a general audience.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 3: SEO Optimizer
        seo_optimizer = Agent(
            role='SEO Content Optimizer',
            goal='Optimize content for search engines while maintaining readability and quality',
            backstory="""You are an SEO optimization expert who knows how to make 
            content rank well without sacrificing quality. You excel at strategic 
            keyword placement, meta description creation, header optimization, and 
            internal linking. You understand the balance between SEO best practices 
            and creating content that genuinely serves readers.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 4: Editor
        editor = Agent(
            role='Editorial Director',
            goal='Review and polish content to ensure highest quality before publication',
            backstory="""You are a meticulous editor with an eye for detail and 
            a commitment to quality. You check for clarity, consistency, grammar, 
            and overall flow. You ensure the content meets brand standards and 
            provides real value to readers. You're not afraid to suggest improvements 
            but you also know when content is ready to publish.""",
            verbose=True,
            allow_delegation=False
        )
        
        return seo_researcher, content_writer, seo_optimizer, editor
    
    def create_tasks(self, 
                     topic: str,
                     target_word_count: int = 1000,
                     agents: tuple = None) -> list[Task]:
        """Create the sequential tasks for content creation workflow.
        
        Args:
            topic: The blog post topic
            target_word_count: Target length for the blog post
            agents: Tuple of agents (seo_researcher, content_writer, seo_optimizer, editor)
        
        Returns:
            List of tasks in execution order
        """
        seo_researcher, content_writer, seo_optimizer, editor = agents
        
        # Task 1: SEO Research
        research_task = Task(
            description=f"""Conduct comprehensive SEO research for the topic: "{topic}"
            
            Your research should include:
            1. Primary and secondary keywords related to the topic
            2. Search volume and competition analysis (if search tool available)
            3. Current trending angles or subtopics
            4. Common questions people ask about this topic
            5. Recommended content structure based on top-ranking content
            
            Provide a detailed research brief that will guide the content writer.""",
            agent=seo_researcher,
            expected_output="""A comprehensive SEO research brief containing:
            - 5-10 target keywords with their relevance
            - 3-5 trending angles or subtopics
            - 5-8 common questions to address
            - Recommended content structure (headers/sections)
            - Key points to cover for search intent"""
        )
        
        # Task 2: Content Writing
        writing_task = Task(
            description=f"""Write a comprehensive blog post about: "{topic}"
            
            Use the SEO research brief from the previous task to inform your writing.
            
            Requirements:
            - Target length: {target_word_count}+ words
            - Include an engaging introduction that hooks the reader
            - Organize content with clear headers (H2, H3)
            - Include practical insights, examples, or takeaways
            - Write in a professional yet conversational tone
            - Address the key questions identified in research
            - Include a compelling conclusion with key takeaways
            
            Format: Write the complete blog post content (body only, no title/meta yet)""",
            agent=content_writer,
            expected_output=f"""A complete, well-structured blog post of {target_word_count}+ words with:
            - Engaging introduction
            - Clear section headers
            - Practical, valuable content
            - Examples and insights
            - Strong conclusion""",
            context=[research_task]  # Depends on research task output
        )
        
        # Task 3: SEO Optimization
        optimization_task = Task(
            description=f"""Optimize the blog post for search engines while maintaining quality.
            
            Using the research brief and the written content, perform these optimizations:
            
            1. Create an SEO-optimized title (60 characters or less)
            2. Write a compelling meta description (155-160 characters)
            3. Verify keyword placement in:
               - Title
               - First paragraph
               - Headers (at least 2-3)
               - Throughout body (natural placement)
               - Conclusion
            4. Suggest 5-8 relevant tags/categories
            5. Generate alt text for potential featured image
            6. Ensure content includes:
               - Clear header hierarchy (H2, H3)
               - Optimal keyword density (1-2%)
               - Internal linking opportunities
               - Call-to-action
            
            Provide the optimized version with all SEO elements.""",
            agent=seo_optimizer,
            expected_output="""Complete SEO package including:
            - SEO-optimized title
            - Meta description
            - Optimized blog post content
            - 5-8 tags/categories
            - Featured image alt text
            - Image prompt suggestion
            - SEO checklist confirmation""",
            context=[research_task, writing_task]  # Depends on both previous tasks
        )
        
        # Task 4: Editorial Review
        editing_task = Task(
            description="""Review and finalize the SEO-optimized blog post.
            
            Perform a comprehensive editorial review:
            
            1. Quality Check:
               - Content accuracy and clarity
               - Grammar, spelling, and punctuation
               - Tone consistency
               - Logical flow and transitions
            
            2. SEO Review:
               - Verify keyword optimization is natural
               - Check that headers are clear and informative
               - Ensure meta elements are compelling
            
            3. Value Assessment:
               - Does it provide real value to readers?
               - Are practical takeaways clear?
               - Is it engaging and readable?
            
            4. Final Polish:
               - Make any necessary improvements
               - Ensure publication readiness
            
            Provide the final, publication-ready version with your editorial notes.""",
            agent=editor,
            expected_output="""Final publication package including:
            - Polished title
            - Final meta description
            - Edited and approved blog post content
            - Final tag list
            - Editorial notes on quality
            - Approval status
            - Any final recommendations""",
            context=[research_task, writing_task, optimization_task]  # Depends on all previous tasks
        )
        
        return [research_task, writing_task, optimization_task, editing_task]
    
    def generate_content(self, 
                        topic: str, 
                        target_word_count: int = 1000) -> Dict[str, Any]:
        """Execute the complete content generation workflow.
        
        Args:
            topic: The blog post topic
            target_word_count: Target word count for the post
        
        Returns:
            Dictionary with all generated content and metadata
        """
        print(f"\n{'='*80}")
        print(f"🚀 Starting Content Generation Workflow")
        print(f"📝 Topic: {topic}")
        print(f"📏 Target Length: {target_word_count}+ words")
        print(f"{'='*80}\n")
        
        # Create agents
        agents = self.create_agents()
        
        # Create tasks
        tasks = self.create_tasks(topic, target_word_count, agents)
        
        # Create crew with sequential process
        crew = Crew(
            agents=list(agents),
            tasks=tasks,
            process=Process.sequential,  # Execute tasks in order
            verbose=True
        )
        
        # Execute the workflow
        print("\n🎬 Executing crew workflow...\n")
        result = crew.kickoff()
        
        print(f"\n{'='*80}")
        print(f"✅ Content Generation Complete!")
        print(f"{'='*80}\n")
        
        return {
            "success": True,
            "topic": topic,
            "result": result,
            "agents_used": len(agents),
            "tasks_completed": len(tasks)
        }


def main():
    """Run the demo workflow."""
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║        CrewAI Content Generation + SEO Optimization Demo              ║
    ║                      for Substack Auto                                 ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check for required API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print("   Exiting demo...\n")
        return
    
    # Create the crew
    crew = ContentSEOCrew()
    
    # Example topics
    example_topics = [
        "The Future of AI-Powered Content Creation",
        "SEO Strategies for 2025: What's Changed",
        "Building Multi-Agent Systems with Python"
    ]
    
    print("\n📋 Example Topics:")
    for i, topic in enumerate(example_topics, 1):
        print(f"   {i}. {topic}")
    
    # For demo purposes, use the first topic
    topic = example_topics[0]
    print(f"\n🎯 Using topic: {topic}")
    print("\n" + "="*80 + "\n")
    
    # Generate content
    try:
        result = crew.generate_content(
            topic=topic,
            target_word_count=1000
        )
        
        print("\n" + "="*80)
        print("📊 RESULTS SUMMARY")
        print("="*80)
        print(f"✓ Topic: {result['topic']}")
        print(f"✓ Agents Used: {result['agents_used']}")
        print(f"✓ Tasks Completed: {result['tasks_completed']}")
        print(f"✓ Success: {result['success']}")
        print("\n📄 Final Output:")
        print("-" * 80)
        print(result['result'])
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during content generation: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure OPENAI_API_KEY is set")
        print("2. Check your OpenAI API key is valid and has credits")
        print("3. Verify internet connectivity")


if __name__ == "__main__":
    main()
