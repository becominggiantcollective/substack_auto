"""
SEO Analysis Agent using CrewAI framework.

This module provides a CrewAI-powered agent for analyzing and optimizing
content for search engine optimization (SEO).
"""
import logging
import re
from typing import Dict, List, Optional

# Try to import slugify, provide fallback if not available
try:
    from slugify import slugify as external_slugify
    SLUGIFY_AVAILABLE = True
except ImportError:
    SLUGIFY_AVAILABLE = False
    logging.warning("python-slugify not available. Using fallback slug generation.")

try:
    from crewai import Agent, Task, Crew
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    logging.warning("CrewAI not available. SEO agent functionality will be limited.")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    logging.warning("BeautifulSoup not available. HTML analysis will be limited.")

logger = logging.getLogger(__name__)


def slugify(text: str, max_length: int = 60, word_boundary: bool = True) -> str:
    """
    Fallback slug generator when python-slugify is not available.
    
    Args:
        text: Text to convert to slug
        max_length: Maximum length of slug
        word_boundary: Whether to break at word boundaries
        
    Returns:
        URL-friendly slug
    """
    if SLUGIFY_AVAILABLE:
        return external_slugify(text, max_length=max_length, word_boundary=word_boundary)
    
    # Fallback implementation
    # Convert to lowercase
    slug = text.lower()
    
    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)
    
    # Remove non-alphanumeric characters except hyphens
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Truncate to max_length
    if len(slug) > max_length:
        if word_boundary:
            # Try to break at a hyphen
            slug = slug[:max_length]
            last_hyphen = slug.rfind('-')
            if last_hyphen > 0:
                slug = slug[:last_hyphen]
        else:
            slug = slug[:max_length]
    
    return slug


class SEOAnalyzer:
    """SEO analysis and optimization tool for Substack content."""
    
    def __init__(self):
        """Initialize the SEO analyzer."""
        self.logger = logger
    
    def generate_slug(self, title: str) -> str:
        """
        Generate an SEO-friendly URL slug from a title.
        
        Args:
            title: The title to convert to a slug
            
        Returns:
            SEO-friendly URL slug
        """
        return slugify(title, max_length=60, word_boundary=True)
    
    def analyze_title(self, title: str) -> Dict[str, any]:
        """
        Analyze a title for SEO best practices.
        
        Args:
            title: The title to analyze
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            "title": title,
            "length": len(title),
            "word_count": len(title.split()),
            "slug": self.generate_slug(title),
            "recommendations": []
        }
        
        # Check title length (optimal: 50-60 characters)
        if analysis["length"] < 30:
            analysis["recommendations"].append("Title is too short. Aim for 50-60 characters.")
        elif analysis["length"] > 70:
            analysis["recommendations"].append("Title is too long. Aim for 50-60 characters.")
        else:
            analysis["recommendations"].append("Title length is optimal.")
        
        # Check word count (optimal: 6-8 words)
        if analysis["word_count"] < 4:
            analysis["recommendations"].append("Consider adding more descriptive words to the title.")
        elif analysis["word_count"] > 12:
            analysis["recommendations"].append("Title may be too wordy. Consider simplifying.")
        
        return analysis
    
    def analyze_content(self, content: str, title: str = "") -> Dict[str, any]:
        """
        Analyze content for SEO best practices.
        
        Args:
            content: The content to analyze
            title: Optional title for keyword comparison
            
        Returns:
            Dictionary with SEO analysis results
        """
        analysis = {
            "content_length": len(content),
            "word_count": len(content.split()),
            "paragraph_count": content.count('\n\n') + 1,
            "recommendations": []
        }
        
        # Check content length (optimal: 1000-2500 words for blog posts)
        if analysis["word_count"] < 300:
            analysis["recommendations"].append(
                "Content is quite short. Consider expanding to 1000+ words for better SEO."
            )
        elif analysis["word_count"] < 800:
            analysis["recommendations"].append(
                "Content length is acceptable, but 1000+ words perform better in search."
            )
        elif analysis["word_count"] > 3000:
            analysis["recommendations"].append(
                "Content is quite long. Consider breaking into multiple posts."
            )
        else:
            analysis["recommendations"].append("Content length is optimal for SEO.")
        
        # Check readability
        avg_words_per_paragraph = analysis["word_count"] / max(analysis["paragraph_count"], 1)
        if avg_words_per_paragraph > 150:
            analysis["recommendations"].append(
                "Paragraphs are too long. Break them up for better readability."
            )
        
        # Extract basic keywords (simplified approach)
        words = content.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only consider words longer than 4 characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        analysis["top_keywords"] = [{"keyword": k, "count": c} for k, c in top_keywords]
        
        return analysis
    
    def extract_metadata(self, html_content: str) -> Dict[str, any]:
        """
        Extract SEO metadata from HTML content.
        
        Args:
            html_content: HTML content to parse
            
        Returns:
            Dictionary with extracted metadata
        """
        if not BS4_AVAILABLE:
            logger.warning("BeautifulSoup not available. Cannot extract metadata.")
            return {}
        
        soup = BeautifulSoup(html_content, 'html.parser')
        metadata = {
            "title": None,
            "description": None,
            "keywords": None,
            "og_title": None,
            "og_description": None,
            "og_image": None,
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata["title"] = title_tag.string
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            property_attr = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description':
                metadata["description"] = content
            elif name == 'keywords':
                metadata["keywords"] = content
            elif property_attr == 'og:title':
                metadata["og_title"] = content
            elif property_attr == 'og:description':
                metadata["og_description"] = content
            elif property_attr == 'og:image':
                metadata["og_image"] = content
        
        return metadata
    
    def generate_meta_description(self, content: str, max_length: int = 160) -> str:
        """
        Generate a meta description from content.
        
        Args:
            content: The content to generate description from
            max_length: Maximum length of the description
            
        Returns:
            Generated meta description
        """
        # Take first paragraph or first few sentences
        paragraphs = content.split('\n\n')
        first_paragraph = paragraphs[0] if paragraphs else content
        
        # Clean up and truncate
        description = first_paragraph.replace('\n', ' ').strip()
        
        if len(description) > max_length:
            # Truncate at word boundary
            description = description[:max_length].rsplit(' ', 1)[0] + '...'
        
        return description
    
    def generate_seo_report(self, title: str, content: str) -> Dict[str, any]:
        """
        Generate a comprehensive SEO report for a blog post.
        
        Args:
            title: Post title
            content: Post content
            
        Returns:
            Comprehensive SEO analysis report
        """
        report = {
            "title_analysis": self.analyze_title(title),
            "content_analysis": self.analyze_content(content, title),
            "meta_description": self.generate_meta_description(content),
            "slug": self.generate_slug(title),
            "overall_score": 0.0,
            "recommendations": []
        }
        
        # Calculate overall score (simplified)
        score = 0.0
        max_score = 100.0
        
        # Title score (20 points)
        title_len = report["title_analysis"]["length"]
        if 50 <= title_len <= 60:
            score += 20
        elif 40 <= title_len <= 70:
            score += 15
        else:
            score += 10
        
        # Content length score (30 points)
        word_count = report["content_analysis"]["word_count"]
        if 1000 <= word_count <= 2500:
            score += 30
        elif 800 <= word_count <= 3000:
            score += 25
        elif 500 <= word_count <= 800:
            score += 15
        else:
            score += 5
        
        # Meta description score (20 points)
        meta_len = len(report["meta_description"])
        if 120 <= meta_len <= 160:
            score += 20
        elif 100 <= meta_len <= 165:
            score += 15
        else:
            score += 10
        
        # Slug score (10 points)
        slug_len = len(report["slug"])
        if 20 <= slug_len <= 60:
            score += 10
        else:
            score += 5
        
        # Keywords score (20 points)
        if report["content_analysis"]["top_keywords"]:
            score += 20
        
        report["overall_score"] = round(score, 1)
        
        # Add overall recommendations
        if score >= 80:
            report["recommendations"].append("✅ Excellent SEO optimization!")
        elif score >= 60:
            report["recommendations"].append("✓ Good SEO, but there's room for improvement.")
        else:
            report["recommendations"].append("⚠ SEO needs significant improvement.")
        
        # Combine all recommendations
        report["recommendations"].extend(report["title_analysis"]["recommendations"])
        report["recommendations"].extend(report["content_analysis"]["recommendations"])
        
        return report


def create_seo_agent(role: str = "SEO Specialist", 
                     goal: str = "Optimize content for search engines",
                     backstory: str = None):
    """
    Create a CrewAI SEO agent for content optimization.
    
    Args:
        role: The role of the agent
        goal: The goal of the agent
        backstory: Optional backstory for the agent
        
    Returns:
        CrewAI Agent instance or None if CrewAI is not available
    """
    if not CREWAI_AVAILABLE:
        logger.error("CrewAI is not available. Cannot create SEO agent.")
        return None
    
    if backstory is None:
        backstory = (
            "You are an expert SEO specialist with years of experience in "
            "optimizing content for search engines. You understand best practices "
            "for title optimization, meta descriptions, keyword usage, and content "
            "structure that drives organic traffic."
        )
    
    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=False
    )
    
    return agent


def create_seo_optimization_task(agent, title: str, content: str):
    """
    Create an SEO optimization task for the agent.
    
    Args:
        agent: The CrewAI agent to assign the task to
        title: The content title to optimize
        content: The content to optimize
        
    Returns:
        CrewAI Task instance or None if CrewAI is not available
    """
    if not CREWAI_AVAILABLE:
        logger.error("CrewAI is not available. Cannot create SEO task.")
        return None
    
    description = f"""
    Analyze and provide SEO optimization recommendations for the following content:
    
    Title: {title}
    Content Preview: {content[:500]}...
    
    Provide specific, actionable recommendations for:
    1. Title optimization
    2. Content structure and length
    3. Keyword usage and placement
    4. Meta description
    5. URL slug
    """
    
    task = Task(
        description=description,
        agent=agent,
        expected_output="A detailed SEO analysis with specific recommendations"
    )
    
    return task


def run_seo_crew(title: str, content: str) -> Optional[str]:
    """
    Run a CrewAI crew for SEO analysis and optimization.
    
    Args:
        title: Content title
        content: Content to analyze
        
    Returns:
        SEO analysis results or None if CrewAI is not available
    """
    if not CREWAI_AVAILABLE:
        logger.error("CrewAI is not available. Using basic SEO analyzer instead.")
        # Fall back to basic analyzer
        analyzer = SEOAnalyzer()
        report = analyzer.generate_seo_report(title, content)
        return str(report)
    
    try:
        # Create agent
        seo_agent = create_seo_agent()
        
        # Create task
        seo_task = create_seo_optimization_task(seo_agent, title, content)
        
        # Create and run crew
        crew = Crew(
            agents=[seo_agent],
            tasks=[seo_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    except Exception as e:
        logger.error(f"Error running SEO crew: {e}")
        # Fall back to basic analyzer
        analyzer = SEOAnalyzer()
        report = analyzer.generate_seo_report(title, content)
        return str(report)


# Example usage and testing
if __name__ == "__main__":
    # Test basic SEO analyzer
    analyzer = SEOAnalyzer()
    
    # Test title analysis
    test_title = "How AI is Transforming Modern Content Creation"
    title_analysis = analyzer.analyze_title(test_title)
    print("Title Analysis:")
    print(f"  Title: {title_analysis['title']}")
    print(f"  Length: {title_analysis['length']}")
    print(f"  Slug: {title_analysis['slug']}")
    print(f"  Recommendations: {title_analysis['recommendations']}")
    print()
    
    # Test content analysis
    test_content = """
    Artificial Intelligence is revolutionizing the way we create and consume content.
    From automated writing to intelligent editing, AI tools are becoming essential
    for content creators across all industries.
    
    In this comprehensive guide, we'll explore how AI is transforming content creation,
    the tools available today, and what the future holds for this exciting field.
    """ * 20  # Repeat to get realistic word count
    
    content_analysis = analyzer.analyze_content(test_content, test_title)
    print("Content Analysis:")
    print(f"  Word Count: {content_analysis['word_count']}")
    print(f"  Top Keywords: {content_analysis['top_keywords'][:5]}")
    print(f"  Recommendations: {content_analysis['recommendations']}")
    print()
    
    # Test full SEO report
    full_report = analyzer.generate_seo_report(test_title, test_content)
    print("Full SEO Report:")
    print(f"  Overall Score: {full_report['overall_score']}/100")
    print(f"  Meta Description: {full_report['meta_description']}")
    print(f"  Slug: {full_report['slug']}")
    print(f"  Recommendations: {full_report['recommendations'][:3]}")
