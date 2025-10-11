"""
Editor Agent for content quality and SEO refinement.

This agent reviews, refines, and enhances draft articles for clarity, engagement,
and SEO effectiveness. It checks grammar, tone, structure, and SEO keyword integration,
and refines meta titles, meta descriptions, and tags for optimal SEO performance.
"""
import logging
import re
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class EditorAgent:
    """
    Editor Agent that reviews and refines draft articles for quality and SEO.
    
    Features:
    - Grammar and spelling checks
    - Tone and style consistency analysis
    - Content structure optimization
    - SEO keyword integration and optimization
    - Meta title and description refinement
    - Tag generation and optimization
    - Comprehensive SEO improvement reports
    """
    
    def __init__(self):
        """Initialize the Editor Agent with OpenAI client."""
        from config.settings import settings
        self.settings = settings
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self.model = "gpt-4"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def check_grammar_and_spelling(self, content: str) -> Dict[str, any]:
        """
        Check grammar and spelling in the content.
        
        Args:
            content: The article content to check
            
        Returns:
            Dict containing corrections and suggestions
        """
        prompt = f"""
        Review the following content for grammar and spelling errors.
        Provide specific corrections and improvements.
        
        Content:
        {content}
        
        Return your response in the following format:
        ERRORS: List any grammar or spelling errors found
        CORRECTED_TEXT: The corrected version of the text (only if errors found)
        SUGGESTIONS: Any additional grammar or style suggestions
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse the response
            errors = []
            corrected_text = None
            suggestions = []
            
            if "ERRORS:" in result_text:
                errors_section = result_text.split("ERRORS:")[1].split("CORRECTED_TEXT:")[0].strip()
                if errors_section and errors_section.lower() != "none" and "no errors" not in errors_section.lower():
                    errors = [e.strip() for e in errors_section.split("\n") if e.strip()]
            
            if "CORRECTED_TEXT:" in result_text:
                corrected_section = result_text.split("CORRECTED_TEXT:")[1].split("SUGGESTIONS:")[0].strip()
                if corrected_section and corrected_section.lower() != "none":
                    corrected_text = corrected_section
            
            if "SUGGESTIONS:" in result_text:
                suggestions_section = result_text.split("SUGGESTIONS:")[1].strip()
                if suggestions_section:
                    suggestions = [s.strip() for s in suggestions_section.split("\n") if s.strip()]
            
            return {
                "has_errors": len(errors) > 0,
                "errors": errors,
                "corrected_text": corrected_text,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"Error checking grammar: {e}")
            return {
                "has_errors": False,
                "errors": [],
                "corrected_text": None,
                "suggestions": []
            }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def analyze_tone_and_style(self, content: str, target_tone: Optional[str] = None) -> Dict[str, any]:
        """
        Analyze the tone and style of the content.
        
        Args:
            content: The article content to analyze
            target_tone: The desired tone (defaults to settings.content_tone)
            
        Returns:
            Dict containing tone analysis and suggestions
        """
        if target_tone is None:
            target_tone = self.settings.content_tone
        
        prompt = f"""
        Analyze the tone and style of the following content.
        Target tone: {target_tone}
        Target audience: {self.settings.target_audience}
        
        Content:
        {content}
        
        Provide:
        1. Current tone assessment
        2. Whether it matches the target tone
        3. Specific suggestions for tone adjustments if needed
        4. Overall style consistency rating (1-10)
        
        Format your response as:
        CURRENT_TONE: [description]
        MATCHES_TARGET: [Yes/No]
        CONSISTENCY_RATING: [1-10]
        SUGGESTIONS: [specific suggestions, one per line]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.5
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse response
            current_tone = "Unknown"
            matches_target = False
            consistency_rating = 7
            suggestions = []
            
            if "CURRENT_TONE:" in result_text:
                current_tone = result_text.split("CURRENT_TONE:")[1].split("\n")[0].strip()
            
            if "MATCHES_TARGET:" in result_text:
                matches_text = result_text.split("MATCHES_TARGET:")[1].split("\n")[0].strip().lower()
                matches_target = "yes" in matches_text
            
            if "CONSISTENCY_RATING:" in result_text:
                rating_text = result_text.split("CONSISTENCY_RATING:")[1].split("\n")[0].strip()
                try:
                    consistency_rating = int(re.search(r'\d+', rating_text).group())
                except:
                    consistency_rating = 7
            
            if "SUGGESTIONS:" in result_text:
                suggestions_section = result_text.split("SUGGESTIONS:")[1].strip()
                if suggestions_section:
                    suggestions = [s.strip() for s in suggestions_section.split("\n") if s.strip()]
            
            return {
                "current_tone": current_tone,
                "target_tone": target_tone,
                "matches_target": matches_target,
                "consistency_rating": consistency_rating,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"Error analyzing tone: {e}")
            return {
                "current_tone": "Unknown",
                "target_tone": target_tone,
                "matches_target": True,
                "consistency_rating": 7,
                "suggestions": []
            }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def analyze_structure(self, content: str) -> Dict[str, any]:
        """
        Analyze the structure and organization of the content.
        
        Args:
            content: The article content to analyze
            
        Returns:
            Dict containing structure analysis and suggestions
        """
        prompt = f"""
        Analyze the structure and organization of the following content.
        
        Content:
        {content}
        
        Evaluate:
        1. Introduction effectiveness
        2. Body organization and flow
        3. Conclusion strength
        4. Overall readability score (1-10)
        5. Suggestions for structural improvements
        
        Format your response as:
        INTRODUCTION: [Good/Needs Improvement - brief comment]
        BODY_FLOW: [Good/Needs Improvement - brief comment]
        CONCLUSION: [Good/Needs Improvement - brief comment]
        READABILITY_SCORE: [1-10]
        IMPROVEMENTS: [specific suggestions, one per line]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.5
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse response
            introduction = "Good"
            body_flow = "Good"
            conclusion = "Good"
            readability_score = 8
            improvements = []
            
            if "INTRODUCTION:" in result_text:
                introduction = result_text.split("INTRODUCTION:")[1].split("\n")[0].strip()
            
            if "BODY_FLOW:" in result_text:
                body_flow = result_text.split("BODY_FLOW:")[1].split("\n")[0].strip()
            
            if "CONCLUSION:" in result_text:
                conclusion = result_text.split("CONCLUSION:")[1].split("\n")[0].strip()
            
            if "READABILITY_SCORE:" in result_text:
                score_text = result_text.split("READABILITY_SCORE:")[1].split("\n")[0].strip()
                try:
                    readability_score = int(re.search(r'\d+', score_text).group())
                except:
                    readability_score = 8
            
            if "IMPROVEMENTS:" in result_text:
                improvements_section = result_text.split("IMPROVEMENTS:")[1].strip()
                if improvements_section:
                    improvements = [s.strip() for s in improvements_section.split("\n") if s.strip()]
            
            return {
                "introduction": introduction,
                "body_flow": body_flow,
                "conclusion": conclusion,
                "readability_score": readability_score,
                "improvements": improvements
            }
            
        except Exception as e:
            logger.error(f"Error analyzing structure: {e}")
            return {
                "introduction": "Good",
                "body_flow": "Good",
                "conclusion": "Good",
                "readability_score": 8,
                "improvements": []
            }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def optimize_seo_keywords(self, title: str, content: str, existing_keywords: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Optimize SEO keywords for the content.
        
        Args:
            title: Article title
            content: Article content
            existing_keywords: Existing keywords/tags if any
            
        Returns:
            Dict containing keyword analysis and optimized keywords
        """
        existing_kw_text = f"\nExisting keywords: {', '.join(existing_keywords)}" if existing_keywords else ""
        
        prompt = f"""
        Analyze and optimize SEO keywords for the following article.
        
        Title: {title}
        Content: {content[:1000]}...
        {existing_kw_text}
        
        Provide:
        1. Primary keywords (2-3 most important)
        2. Secondary keywords (5-7 supporting keywords)
        3. Long-tail keywords (3-5 phrases)
        4. Keyword density assessment
        5. Suggestions for keyword integration
        
        Format your response as:
        PRIMARY: [keyword1, keyword2, keyword3]
        SECONDARY: [keyword1, keyword2, ...]
        LONG_TAIL: [phrase1, phrase2, ...]
        DENSITY: [Good/Too High/Too Low]
        SUGGESTIONS: [specific suggestions for keyword integration]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.6
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse response
            primary_keywords = []
            secondary_keywords = []
            long_tail_keywords = []
            density = "Good"
            suggestions = []
            
            if "PRIMARY:" in result_text:
                primary_text = result_text.split("PRIMARY:")[1].split("\n")[0].strip()
                primary_keywords = [k.strip() for k in primary_text.replace("[", "").replace("]", "").split(",")]
            
            if "SECONDARY:" in result_text:
                secondary_text = result_text.split("SECONDARY:")[1].split("\n")[0].strip()
                secondary_keywords = [k.strip() for k in secondary_text.replace("[", "").replace("]", "").split(",")]
            
            if "LONG_TAIL:" in result_text:
                long_tail_text = result_text.split("LONG_TAIL:")[1].split("\n")[0].strip()
                long_tail_keywords = [k.strip() for k in long_tail_text.replace("[", "").replace("]", "").split(",")]
            
            if "DENSITY:" in result_text:
                density = result_text.split("DENSITY:")[1].split("\n")[0].strip()
            
            if "SUGGESTIONS:" in result_text:
                suggestions_text = result_text.split("SUGGESTIONS:")[1].strip()
                if suggestions_text:
                    suggestions = [s.strip() for s in suggestions_text.split("\n") if s.strip()]
            
            return {
                "primary_keywords": [k for k in primary_keywords if k],
                "secondary_keywords": [k for k in secondary_keywords if k],
                "long_tail_keywords": [k for k in long_tail_keywords if k],
                "keyword_density": density,
                "integration_suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"Error optimizing SEO keywords: {e}")
            return {
                "primary_keywords": [],
                "secondary_keywords": [],
                "long_tail_keywords": [],
                "keyword_density": "Unknown",
                "integration_suggestions": []
            }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def refine_meta_title(self, current_title: str, content_summary: str) -> Dict[str, any]:
        """
        Refine the meta title for SEO optimization.
        
        Args:
            current_title: Current article title
            content_summary: Brief summary of the content
            
        Returns:
            Dict containing refined title and analysis
        """
        prompt = f"""
        Optimize the following title for SEO best practices.
        
        Current Title: {current_title}
        Content Summary: {content_summary}
        
        Requirements:
        - Keep between 50-60 characters (ideal for SEO)
        - Include primary keywords
        - Make it compelling and click-worthy
        - Maintain clarity and relevance
        
        Provide:
        1. Optimized title
        2. Character count
        3. Improvements made
        4. SEO score (1-10)
        
        Format your response as:
        OPTIMIZED_TITLE: [title]
        CHARACTER_COUNT: [number]
        IMPROVEMENTS: [what was improved]
        SEO_SCORE: [1-10]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse response
            optimized_title = current_title
            char_count = len(current_title)
            improvements = []
            seo_score = 7
            
            if "OPTIMIZED_TITLE:" in result_text:
                optimized_title = result_text.split("OPTIMIZED_TITLE:")[1].split("\n")[0].strip()
                char_count = len(optimized_title)
            
            if "CHARACTER_COUNT:" in result_text:
                count_text = result_text.split("CHARACTER_COUNT:")[1].split("\n")[0].strip()
                try:
                    char_count = int(re.search(r'\d+', count_text).group())
                except:
                    char_count = len(optimized_title)
            
            if "IMPROVEMENTS:" in result_text:
                improvements_text = result_text.split("IMPROVEMENTS:")[1]
                if "SEO_SCORE:" in improvements_text:
                    improvements_text = improvements_text.split("SEO_SCORE:")[0]
                improvements_text = improvements_text.strip()
                if improvements_text:
                    improvements = [s.strip() for s in improvements_text.split("\n") if s.strip()]
            
            if "SEO_SCORE:" in result_text:
                score_text = result_text.split("SEO_SCORE:")[1].split("\n")[0].strip()
                try:
                    seo_score = int(re.search(r'\d+', score_text).group())
                except:
                    seo_score = 7
            
            return {
                "original_title": current_title,
                "optimized_title": optimized_title,
                "character_count": char_count,
                "improvements": improvements,
                "seo_score": seo_score
            }
            
        except Exception as e:
            logger.error(f"Error refining meta title: {e}")
            return {
                "original_title": current_title,
                "optimized_title": current_title,
                "character_count": len(current_title),
                "improvements": [],
                "seo_score": 7
            }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_meta_description(self, title: str, content: str) -> Dict[str, any]:
        """
        Generate an optimized meta description for SEO.
        
        Args:
            title: Article title
            content: Article content
            
        Returns:
            Dict containing meta description and analysis
        """
        prompt = f"""
        Create an optimized meta description for SEO.
        
        Title: {title}
        Content: {content[:800]}...
        
        Requirements:
        - Keep between 150-160 characters (ideal for SEO)
        - Include primary keywords naturally
        - Make it compelling and descriptive
        - Include a call-to-action if appropriate
        
        Provide:
        1. Optimized meta description
        2. Character count
        3. Keywords included
        4. SEO score (1-10)
        
        Format your response as:
        META_DESCRIPTION: [description]
        CHARACTER_COUNT: [number]
        KEYWORDS: [keyword1, keyword2, ...]
        SEO_SCORE: [1-10]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse response
            meta_description = ""
            char_count = 0
            keywords = []
            seo_score = 7
            
            if "META_DESCRIPTION:" in result_text:
                meta_description = result_text.split("META_DESCRIPTION:")[1].split("\n")[0].strip()
                char_count = len(meta_description)
            
            if "CHARACTER_COUNT:" in result_text:
                count_text = result_text.split("CHARACTER_COUNT:")[1].split("\n")[0].strip()
                try:
                    char_count = int(re.search(r'\d+', count_text).group())
                except:
                    char_count = len(meta_description)
            
            if "KEYWORDS:" in result_text:
                keywords_text = result_text.split("KEYWORDS:")[1].split("\n")[0].strip()
                keywords = [k.strip() for k in keywords_text.replace("[", "").replace("]", "").split(",")]
            
            if "SEO_SCORE:" in result_text:
                score_text = result_text.split("SEO_SCORE:")[1].split("\n")[0].strip()
                try:
                    seo_score = int(re.search(r'\d+', score_text).group())
                except:
                    seo_score = 7
            
            return {
                "meta_description": meta_description,
                "character_count": char_count,
                "keywords_included": [k for k in keywords if k],
                "seo_score": seo_score
            }
            
        except Exception as e:
            logger.error(f"Error generating meta description: {e}")
            return {
                "meta_description": "",
                "character_count": 0,
                "keywords_included": [],
                "seo_score": 7
            }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def optimize_tags(self, title: str, content: str, existing_tags: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Optimize tags for better SEO and discoverability.
        
        Args:
            title: Article title
            content: Article content
            existing_tags: Existing tags if any
            
        Returns:
            Dict containing optimized tags and analysis
        """
        existing_tags_text = f"\nExisting tags: {', '.join(existing_tags)}" if existing_tags else ""
        
        prompt = f"""
        Generate and optimize tags for SEO and discoverability.
        
        Title: {title}
        Content: {content[:600]}...
        {existing_tags_text}
        
        Requirements:
        - Provide 5-8 relevant tags
        - Mix of broad and specific tags
        - Include trending topics if relevant
        - Balance between SEO value and relevance
        
        Format your response as:
        OPTIMIZED_TAGS: [tag1, tag2, tag3, ...]
        NEW_TAGS: [any new tags added]
        REMOVED_TAGS: [any existing tags removed]
        REASONING: [brief explanation of tag choices]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.6
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse response
            optimized_tags = existing_tags if existing_tags else []
            new_tags = []
            removed_tags = []
            reasoning = ""
            
            if "OPTIMIZED_TAGS:" in result_text:
                tags_text = result_text.split("OPTIMIZED_TAGS:")[1].split("\n")[0].strip()
                optimized_tags = [t.strip() for t in tags_text.replace("[", "").replace("]", "").split(",")]
            
            if "NEW_TAGS:" in result_text:
                new_text = result_text.split("NEW_TAGS:")[1].split("\n")[0].strip()
                new_tags = [t.strip() for t in new_text.replace("[", "").replace("]", "").split(",")]
            
            if "REMOVED_TAGS:" in result_text:
                removed_text = result_text.split("REMOVED_TAGS:")[1].split("\n")[0].strip()
                removed_tags = [t.strip() for t in removed_text.replace("[", "").replace("]", "").split(",")]
            
            if "REASONING:" in result_text:
                reasoning = result_text.split("REASONING:")[1].strip()
            
            return {
                "original_tags": existing_tags if existing_tags else [],
                "optimized_tags": [t for t in optimized_tags if t],
                "new_tags": [t for t in new_tags if t and t.lower() != "none"],
                "removed_tags": [t for t in removed_tags if t and t.lower() != "none"],
                "reasoning": reasoning
            }
            
        except Exception as e:
            logger.error(f"Error optimizing tags: {e}")
            return {
                "original_tags": existing_tags if existing_tags else [],
                "optimized_tags": existing_tags if existing_tags else [],
                "new_tags": [],
                "removed_tags": [],
                "reasoning": ""
            }
    
    def edit_article(self, article_data: Dict[str, any]) -> Dict[str, any]:
        """
        Perform comprehensive editing on an article draft.
        
        This is the main method that performs all editing checks and optimizations.
        
        Args:
            article_data: Dictionary containing:
                - title: Article title
                - subtitle: Article subtitle (optional)
                - content: Article content
                - tags: List of tags (optional)
                
        Returns:
            Dictionary containing:
                - edited_article: The refined article with all improvements
                - seo_report: Comprehensive SEO improvement report
                - quality_metrics: Quality assessment metrics
        """
        try:
            logger.info(f"Starting comprehensive editing for article: {article_data.get('title', 'Unknown')}")
            
            title = article_data.get("title", "")
            subtitle = article_data.get("subtitle", "")
            content = article_data.get("content", "")
            tags = article_data.get("tags", [])
            
            # Step 1: Grammar and spelling check
            logger.info("Checking grammar and spelling...")
            grammar_check = self.check_grammar_and_spelling(content)
            
            # Use corrected text if errors were found
            if grammar_check["has_errors"] and grammar_check["corrected_text"]:
                content = grammar_check["corrected_text"]
            
            # Step 2: Tone and style analysis
            logger.info("Analyzing tone and style...")
            tone_analysis = self.analyze_tone_and_style(content)
            
            # Step 3: Structure analysis
            logger.info("Analyzing structure...")
            structure_analysis = self.analyze_structure(content)
            
            # Step 4: SEO keyword optimization
            logger.info("Optimizing SEO keywords...")
            keyword_optimization = self.optimize_seo_keywords(title, content, tags)
            
            # Step 5: Meta title refinement
            logger.info("Refining meta title...")
            content_summary = subtitle if subtitle else content[:200]
            title_refinement = self.refine_meta_title(title, content_summary)
            
            # Step 6: Meta description generation
            logger.info("Generating meta description...")
            meta_description = self.generate_meta_description(title, content)
            
            # Step 7: Tag optimization
            logger.info("Optimizing tags...")
            tag_optimization = self.optimize_tags(title, content, tags)
            
            # Compile edited article
            edited_article = {
                "title": title_refinement["optimized_title"],
                "subtitle": subtitle,
                "content": content,
                "meta_description": meta_description["meta_description"],
                "tags": tag_optimization["optimized_tags"],
                "word_count": len(content.split()),
                "ai_generated": article_data.get("ai_generated", True)
            }
            
            # Calculate overall quality score
            quality_scores = [
                10 if not grammar_check["has_errors"] else 7,
                tone_analysis["consistency_rating"],
                structure_analysis["readability_score"],
                title_refinement["seo_score"],
                meta_description["seo_score"]
            ]
            overall_quality_score = sum(quality_scores) / len(quality_scores)
            
            # Compile SEO report
            seo_report = {
                "overall_seo_score": round(overall_quality_score, 1),
                "title_optimization": {
                    "original": title,
                    "optimized": title_refinement["optimized_title"],
                    "character_count": title_refinement["character_count"],
                    "improvements": title_refinement["improvements"],
                    "score": title_refinement["seo_score"]
                },
                "meta_description": {
                    "description": meta_description["meta_description"],
                    "character_count": meta_description["character_count"],
                    "keywords_included": meta_description["keywords_included"],
                    "score": meta_description["seo_score"]
                },
                "keywords": {
                    "primary": keyword_optimization["primary_keywords"],
                    "secondary": keyword_optimization["secondary_keywords"],
                    "long_tail": keyword_optimization["long_tail_keywords"],
                    "density": keyword_optimization["keyword_density"],
                    "suggestions": keyword_optimization["integration_suggestions"]
                },
                "tags": {
                    "original": tag_optimization["original_tags"],
                    "optimized": tag_optimization["optimized_tags"],
                    "new_tags": tag_optimization["new_tags"],
                    "removed_tags": tag_optimization["removed_tags"]
                }
            }
            
            # Compile quality metrics
            quality_metrics = {
                "overall_score": round(overall_quality_score, 1),
                "grammar_check": {
                    "has_errors": grammar_check["has_errors"],
                    "errors_found": len(grammar_check["errors"]),
                    "suggestions": grammar_check["suggestions"]
                },
                "tone_analysis": {
                    "current_tone": tone_analysis["current_tone"],
                    "target_tone": tone_analysis["target_tone"],
                    "matches_target": tone_analysis["matches_target"],
                    "consistency_rating": tone_analysis["consistency_rating"],
                    "suggestions": tone_analysis["suggestions"]
                },
                "structure_analysis": {
                    "introduction": structure_analysis["introduction"],
                    "body_flow": structure_analysis["body_flow"],
                    "conclusion": structure_analysis["conclusion"],
                    "readability_score": structure_analysis["readability_score"],
                    "improvements": structure_analysis["improvements"]
                }
            }
            
            logger.info(f"Editing complete. Overall quality score: {overall_quality_score:.1f}/10")
            
            return {
                "edited_article": edited_article,
                "seo_report": seo_report,
                "quality_metrics": quality_metrics,
                "improvements_made": {
                    "grammar_corrections": grammar_check["has_errors"],
                    "title_optimized": title != title_refinement["optimized_title"],
                    "tags_optimized": len(tag_optimization["new_tags"]) > 0,
                    "meta_description_generated": True
                }
            }
            
        except Exception as e:
            logger.error(f"Error editing article: {e}")
            raise
    
    def get_editing_summary(self, editing_result: Dict[str, any]) -> str:
        """
        Generate a human-readable summary of the editing process.
        
        Args:
            editing_result: The result from edit_article()
            
        Returns:
            Formatted summary string
        """
        try:
            seo_report = editing_result["seo_report"]
            quality_metrics = editing_result["quality_metrics"]
            improvements = editing_result["improvements_made"]
            
            summary = f"""
=== EDITOR AGENT REPORT ===

Overall Quality Score: {quality_metrics['overall_score']}/10
Overall SEO Score: {seo_report['overall_seo_score']}/10

IMPROVEMENTS MADE:
- Grammar corrections: {'Yes' if improvements['grammar_corrections'] else 'No'}
- Title optimized: {'Yes' if improvements['title_optimized'] else 'No'}
- Tags optimized: {'Yes' if improvements['tags_optimized'] else 'No'}
- Meta description generated: {'Yes' if improvements['meta_description_generated'] else 'No'}

SEO OPTIMIZATIONS:
Title: {seo_report['title_optimization']['original']}
  → {seo_report['title_optimization']['optimized']}
  (Score: {seo_report['title_optimization']['score']}/10, {seo_report['title_optimization']['character_count']} chars)

Meta Description: {seo_report['meta_description']['description']}
  (Score: {seo_report['meta_description']['score']}/10, {seo_report['meta_description']['character_count']} chars)

Primary Keywords: {', '.join(seo_report['keywords']['primary'])}
Long-tail Keywords: {', '.join(seo_report['keywords']['long_tail'][:3])}

Tags: {', '.join(seo_report['tags']['optimized'])}

QUALITY METRICS:
- Tone Consistency: {quality_metrics['tone_analysis']['consistency_rating']}/10
- Readability: {quality_metrics['structure_analysis']['readability_score']}/10
- Grammar: {'Clean' if not quality_metrics['grammar_check']['has_errors'] else f"{quality_metrics['grammar_check']['errors_found']} issues found"}

=== END REPORT ===
            """
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error generating editing summary: {e}")
            return "Error generating summary"
