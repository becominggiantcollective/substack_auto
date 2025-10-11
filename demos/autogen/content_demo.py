"""
AutoGen Demo: Content Generation Workflow
==========================================

This demo showcases how AutoGen can be used to create a multi-agent system
for generating content for Substack Auto.

Agents:
- User Proxy: Orchestrates the workflow
- Content Writer: Creates blog posts
- SEO Specialist: Provides SEO guidance
- Editor: Reviews and polishes content

Workflow:
Conversational approach with agents discussing and collaborating
"""

import os
from typing import Dict, Any, List
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager


class ContentAutoGenWorkflow:
    """AutoGen-powered content generation workflow."""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the AutoGen content workflow.
        
        Args:
            openai_api_key: OpenAI API key (optional, will use env var if not provided)
        """
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Configuration for LLM
        self.llm_config = {
            "model": "gpt-4",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "temperature": 0.7,
        }
    
    def create_agents(self) -> tuple:
        """Create the agents for content creation.
        
        Returns:
            Tuple of (user_proxy, writer, seo_specialist, editor)
        """
        
        # User Proxy - orchestrates the workflow
        user_proxy = UserProxyAgent(
            name="ContentManager",
            system_message="""You are the content manager orchestrating the blog post creation.
            Your role is to guide the team through the process:
            1. Request topic research and SEO guidance
            2. Request content writing
            3. Request SEO optimization
            4. Request editorial review
            Coordinate with the team to produce high-quality, SEO-optimized content.""",
            human_input_mode="NEVER",  # Fully automated
            max_consecutive_auto_reply=10,
            code_execution_config=False,
        )
        
        # Content Writer Agent
        writer = AssistantAgent(
            name="ContentWriter",
            system_message="""You are a senior content writer specializing in creating 
            engaging, informative blog posts. Your strengths include:
            - Writing compelling introductions that hook readers
            - Creating well-structured content with clear sections
            - Providing practical insights and examples
            - Maintaining a professional yet conversational tone
            - Writing 1000+ word comprehensive articles
            
            When asked to write, create complete, detailed blog post content.""",
            llm_config=self.llm_config,
        )
        
        # SEO Specialist Agent
        seo_specialist = AssistantAgent(
            name="SEOSpecialist",
            system_message="""You are an SEO expert who helps optimize content for search engines.
            Your expertise includes:
            - Keyword research and analysis
            - Content structure optimization
            - Meta description and title creation
            - Header optimization (H1, H2, H3)
            - Keyword placement strategies
            - Tag and category suggestions
            
            Provide specific, actionable SEO recommendations and create optimized meta elements.""",
            llm_config=self.llm_config,
        )
        
        # Editor Agent
        editor = AssistantAgent(
            name="Editor",
            system_message="""You are an experienced editor who reviews and polishes content.
            Your responsibilities include:
            - Checking grammar, spelling, and punctuation
            - Ensuring clarity and logical flow
            - Verifying tone consistency
            - Assessing overall quality and value
            - Providing constructive feedback
            - Giving final approval when content is publication-ready
            
            Be thorough but efficient in your review.""",
            llm_config=self.llm_config,
        )
        
        return user_proxy, writer, seo_specialist, editor
    
    def generate_content_sequential(self, topic: str) -> Dict[str, Any]:
        """Generate content using sequential agent interactions.
        
        Args:
            topic: The blog post topic
        
        Returns:
            Dictionary with generated content and metadata
        """
        print(f"\n{'='*80}")
        print(f"🚀 Starting AutoGen Content Generation (Sequential)")
        print(f"📝 Topic: {topic}")
        print(f"{'='*80}\n")
        
        user_proxy, writer, seo_specialist, editor = self.create_agents()
        
        # Step 1: SEO Research and Planning
        print("\n📊 Step 1: SEO Research and Planning\n")
        print("-" * 80)
        
        seo_message = f"""Please provide SEO research and guidance for a blog post about: "{topic}"

Include:
1. 5-10 target keywords
2. Recommended content structure (headers)
3. Common questions to address
4. SEO best practices for this topic"""

        user_proxy.initiate_chat(
            seo_specialist,
            message=seo_message,
            max_turns=2
        )
        
        # Get SEO guidance from chat history
        seo_guidance = user_proxy.chat_messages[seo_specialist][-1]['content']
        
        # Step 2: Content Writing
        print("\n✍️  Step 2: Content Writing\n")
        print("-" * 80)
        
        writing_message = f"""Using the SEO guidance provided, write a comprehensive blog post about: "{topic}"

SEO Guidance:
{seo_guidance}

Requirements:
- 1000+ words
- Engaging introduction
- Clear section headers (H2, H3)
- Practical insights and examples
- Professional yet conversational tone
- Strong conclusion with takeaways

Please write the complete blog post content."""

        user_proxy.initiate_chat(
            writer,
            message=writing_message,
            max_turns=2
        )
        
        # Get content from chat history
        blog_content = user_proxy.chat_messages[writer][-1]['content']
        
        # Step 3: SEO Optimization
        print("\n🔍 Step 3: SEO Optimization\n")
        print("-" * 80)
        
        optimization_message = f"""Review and optimize this blog post for SEO:

{blog_content}

Please provide:
1. SEO-optimized title (60 chars or less)
2. Meta description (155-160 chars)
3. Any content improvements for SEO
4. 5-8 relevant tags
5. Featured image alt text suggestion
6. Image prompt for featured image"""

        user_proxy.initiate_chat(
            seo_specialist,
            message=optimization_message,
            max_turns=2
        )
        
        # Get SEO optimization from chat history
        seo_optimization = user_proxy.chat_messages[seo_specialist][-1]['content']
        
        # Step 4: Editorial Review
        print("\n📝 Step 4: Editorial Review\n")
        print("-" * 80)
        
        review_message = f"""Please review this blog post and SEO optimization for final publication:

CONTENT:
{blog_content}

SEO OPTIMIZATION:
{seo_optimization}

Provide:
1. Quality assessment
2. Any necessary improvements
3. Final approval or revision needs"""

        user_proxy.initiate_chat(
            editor,
            message=review_message,
            max_turns=2
        )
        
        # Get editorial review from chat history
        editorial_review = user_proxy.chat_messages[editor][-1]['content']
        
        print(f"\n{'='*80}")
        print(f"✅ Content Generation Complete!")
        print(f"{'='*80}\n")
        
        return {
            "success": True,
            "topic": topic,
            "seo_guidance": seo_guidance,
            "blog_content": blog_content,
            "seo_optimization": seo_optimization,
            "editorial_review": editorial_review,
            "agents_used": 4
        }
    
    def generate_content_group_chat(self, topic: str) -> Dict[str, Any]:
        """Generate content using group chat approach.
        
        Args:
            topic: The blog post topic
        
        Returns:
            Dictionary with generated content and metadata
        """
        print(f"\n{'='*80}")
        print(f"🚀 Starting AutoGen Content Generation (Group Chat)")
        print(f"📝 Topic: {topic}")
        print(f"{'='*80}\n")
        
        user_proxy, writer, seo_specialist, editor = self.create_agents()
        
        # Create group chat
        group_chat = GroupChat(
            agents=[user_proxy, writer, seo_specialist, editor],
            messages=[],
            max_round=12  # Limit rounds to prevent endless conversation
        )
        
        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=self.llm_config
        )
        
        # Start the group chat
        initial_message = f"""Let's create an SEO-optimized blog post about: "{topic}"

Process:
1. SEOSpecialist: Provide keyword research and SEO guidance
2. ContentWriter: Write the blog post using SEO guidance
3. SEOSpecialist: Optimize the content for SEO
4. Editor: Review and approve

Please collaborate to produce publication-ready content."""

        user_proxy.initiate_chat(
            manager,
            message=initial_message,
        )
        
        print(f"\n{'='*80}")
        print(f"✅ Group Chat Content Generation Complete!")
        print(f"{'='*80}\n")
        
        # Extract conversation results
        conversation_history = group_chat.messages
        
        return {
            "success": True,
            "topic": topic,
            "conversation": conversation_history,
            "agents_used": 4,
            "rounds": len(conversation_history)
        }


def main():
    """Run the demo workflow."""
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║              AutoGen Content Generation Demo                           ║
    ║                      for Substack Auto                                 ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check for required API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print("   Exiting demo...\n")
        return
    
    # Create the workflow
    try:
        workflow = ContentAutoGenWorkflow()
    except ValueError as e:
        print(f"❌ Error: {e}")
        return
    
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
    
    print("\n" + "="*80)
    print("Choose workflow mode:")
    print("1. Sequential (agents work one at a time)")
    print("2. Group Chat (agents collaborate in conversation)")
    print("="*80)
    
    # For demo, use sequential (more predictable)
    mode = "sequential"
    print(f"\n📍 Using mode: {mode}")
    print("\n" + "="*80 + "\n")
    
    # Generate content
    try:
        if mode == "sequential":
            result = workflow.generate_content_sequential(topic=topic)
        else:
            result = workflow.generate_content_group_chat(topic=topic)
        
        print("\n" + "="*80)
        print("📊 RESULTS SUMMARY")
        print("="*80)
        print(f"✓ Topic: {result['topic']}")
        print(f"✓ Agents Used: {result['agents_used']}")
        print(f"✓ Success: {result['success']}")
        
        if mode == "sequential":
            print("\n📄 Generated Content:")
            print("-" * 80)
            print("\n🔍 SEO Guidance:")
            print(result['seo_guidance'][:500] + "..." if len(result['seo_guidance']) > 500 else result['seo_guidance'])
            print("\n✍️  Blog Content:")
            print(result['blog_content'][:500] + "..." if len(result['blog_content']) > 500 else result['blog_content'])
            print("\n📈 SEO Optimization:")
            print(result['seo_optimization'][:500] + "..." if len(result['seo_optimization']) > 500 else result['seo_optimization'])
            print("\n📝 Editorial Review:")
            print(result['editorial_review'][:500] + "..." if len(result['editorial_review']) > 500 else result['editorial_review'])
        else:
            print(f"\n💬 Conversation Rounds: {result['rounds']}")
        
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during content generation: {e}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Ensure OPENAI_API_KEY is set")
        print("2. Check your OpenAI API key is valid and has credits")
        print("3. Verify internet connectivity")


if __name__ == "__main__":
    main()
