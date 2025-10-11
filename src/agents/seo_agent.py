"""
SEO Specialist Agent for comprehensive content optimization and scoring.

This agent performs advanced SEO analysis including:
- Keyword density and distribution
- Semantic relevance analysis
- Readability metrics
- Content structure validation
- Meta-data optimization
- SEO scoring and recommendations
"""
import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter
import math

logger = logging.getLogger(__name__)


class SEOAgent:
    """
    SEO Specialist Agent that performs comprehensive optimization and scoring
    for content workflows.
    
    Analyzes content for SEO effectiveness and provides actionable recommendations.
    """
    
    def __init__(self):
        """Initialize the SEO Agent."""
        # Common stop words for keyword analysis
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have', 'had',
            'what', 'when', 'where', 'who', 'which', 'why', 'how', 'or', 'can',
            'could', 'would', 'should', 'may', 'might', 'must', 'shall', 'will',
            'do', 'does', 'did', 'i', 'you', 'we', 'our', 'your', 'their',
            'been', 'being', 'were', 'am', 'his', 'her', 'him', 'she', 'them',
            'there', 'not', 'all', 'if', 'any', 'more', 'than', 'some', 'such'
        }
        
        # Target ranges for optimal SEO
        self.optimal_title_length = (50, 60)  # characters
        self.optimal_subtitle_length = (120, 155)  # characters
        self.optimal_word_count = (800, 2000)  # words
        self.optimal_paragraph_length = (50, 150)  # words
        self.optimal_sentence_length = (15, 25)  # words
        self.optimal_keyword_density = (1.0, 3.0)  # percentage
        self.min_headings = 3
        self.min_tags = 3
        self.max_tags = 10
        
    def analyze_content(
        self,
        title: str,
        subtitle: str,
        content: str,
        tags: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive SEO analysis on content.
        
        Args:
            title: Article title
            subtitle: Article subtitle/description
            content: Main article content
            tags: List of article tags
            metadata: Optional additional metadata
            
        Returns:
            Dictionary containing detailed SEO analysis and recommendations
        """
        logger.info("Starting SEO analysis...")
        
        try:
            # Perform individual analyses
            structure_analysis = self._analyze_structure(title, subtitle, content)
            keyword_analysis = self._analyze_keywords(title, content, tags)
            readability_analysis = self._analyze_readability(content)
            metadata_analysis = self._analyze_metadata(title, subtitle, tags)
            semantic_analysis = self._analyze_semantic_relevance(title, content, tags)
            
            # Calculate overall SEO score
            seo_score = self._calculate_seo_score(
                structure_analysis,
                keyword_analysis,
                readability_analysis,
                metadata_analysis,
                semantic_analysis
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                structure_analysis,
                keyword_analysis,
                readability_analysis,
                metadata_analysis,
                semantic_analysis
            )
            
            # Compile complete report
            report = {
                "seo_score": seo_score,
                "grade": self._get_grade(seo_score),
                "structure_analysis": structure_analysis,
                "keyword_analysis": keyword_analysis,
                "readability_analysis": readability_analysis,
                "metadata_analysis": metadata_analysis,
                "semantic_analysis": semantic_analysis,
                "recommendations": recommendations,
                "summary": self._generate_summary(seo_score, recommendations)
            }
            
            logger.info(f"SEO analysis complete. Score: {seo_score}/100")
            return report
            
        except Exception as e:
            logger.error(f"Error during SEO analysis: {e}")
            raise
    
    def _analyze_structure(self, title: str, subtitle: str, content: str) -> Dict[str, Any]:
        """
        Analyze content structure for SEO optimization.
        
        Evaluates:
        - Title length and optimization
        - Content length and word count
        - Paragraph structure
        - Heading usage
        - Sentence structure
        """
        # Count words and sentences
        words = self._extract_words(content)
        word_count = len(words)
        sentences = self._extract_sentences(content)
        sentence_count = len(sentences)
        
        # Extract paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        
        # Find headings (simple heuristic: lines that are short and may be capitalized)
        potential_headings = self._extract_headings(content)
        heading_count = len(potential_headings)
        
        # Calculate averages
        avg_paragraph_length = word_count / max(paragraph_count, 1)
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Score structure components
        title_length_score = self._score_range(
            len(title), self.optimal_title_length[0], self.optimal_title_length[1]
        )
        
        word_count_score = self._score_range(
            word_count, self.optimal_word_count[0], self.optimal_word_count[1]
        )
        
        paragraph_length_score = self._score_range(
            avg_paragraph_length,
            self.optimal_paragraph_length[0],
            self.optimal_paragraph_length[1]
        )
        
        sentence_length_score = self._score_range(
            avg_sentence_length,
            self.optimal_sentence_length[0],
            self.optimal_sentence_length[1]
        )
        
        heading_score = min(100, (heading_count / self.min_headings) * 100)
        
        overall_structure_score = (
            title_length_score * 0.15 +
            word_count_score * 0.30 +
            paragraph_length_score * 0.20 +
            sentence_length_score * 0.20 +
            heading_score * 0.15
        )
        
        return {
            "score": round(overall_structure_score, 2),
            "title_length": len(title),
            "title_length_optimal": self.optimal_title_length,
            "title_length_score": round(title_length_score, 2),
            "word_count": word_count,
            "word_count_optimal": self.optimal_word_count,
            "word_count_score": round(word_count_score, 2),
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "heading_count": heading_count,
            "avg_paragraph_length": round(avg_paragraph_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "paragraph_length_score": round(paragraph_length_score, 2),
            "sentence_length_score": round(sentence_length_score, 2),
            "heading_score": round(heading_score, 2)
        }
    
    def _analyze_keywords(
        self, title: str, content: str, tags: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze keyword usage and density.
        
        Evaluates:
        - Primary keyword identification
        - Keyword density and distribution
        - Title-content keyword alignment
        - Tag relevance to content
        """
        # Extract all words from content and title
        content_words = self._extract_words(content.lower())
        title_words = self._extract_words(title.lower())
        
        # Count word frequency (excluding stop words)
        word_freq = Counter(
            word for word in content_words 
            if word not in self.stop_words and len(word) > 3
        )
        
        # Extract multi-word phrases (2-grams and 3-grams)
        bigrams = self._extract_ngrams(content_words, 2)
        trigrams = self._extract_ngrams(content_words, 3)
        
        bigram_freq = Counter(bigrams)
        trigram_freq = Counter(trigrams)
        
        # Get top keywords
        top_keywords = word_freq.most_common(10)
        top_bigrams = bigram_freq.most_common(5)
        top_trigrams = trigram_freq.most_common(5)
        
        # Calculate keyword density for top keyword
        if top_keywords:
            primary_keyword = top_keywords[0][0]
            primary_keyword_count = top_keywords[0][1]
            keyword_density = (primary_keyword_count / len(content_words)) * 100
        else:
            primary_keyword = ""
            primary_keyword_count = 0
            keyword_density = 0.0
        
        # Check keyword presence in title
        title_keyword_match = any(
            word in title_words for word, _ in top_keywords[:5]
        )
        
        # Analyze tag relevance
        tag_relevance = self._calculate_tag_relevance(tags, content_words, word_freq)
        
        # Score keyword optimization
        density_score = self._score_range(
            keyword_density,
            self.optimal_keyword_density[0],
            self.optimal_keyword_density[1]
        )
        
        title_match_score = 100 if title_keyword_match else 50
        tag_relevance_score = tag_relevance * 100
        
        overall_keyword_score = (
            density_score * 0.40 +
            title_match_score * 0.30 +
            tag_relevance_score * 0.30
        )
        
        return {
            "score": round(overall_keyword_score, 2),
            "primary_keyword": primary_keyword,
            "primary_keyword_count": primary_keyword_count,
            "keyword_density": round(keyword_density, 2),
            "keyword_density_optimal": self.optimal_keyword_density,
            "density_score": round(density_score, 2),
            "top_keywords": [(word, count) for word, count in top_keywords],
            "top_phrases": {
                "bigrams": [(" ".join(phrase), count) for phrase, count in top_bigrams],
                "trigrams": [(" ".join(phrase), count) for phrase, count in top_trigrams]
            },
            "title_keyword_match": title_keyword_match,
            "title_match_score": round(title_match_score, 2),
            "tag_relevance": round(tag_relevance, 4),
            "tag_relevance_score": round(tag_relevance_score, 2)
        }
    
    def _analyze_readability(self, content: str) -> Dict[str, Any]:
        """
        Analyze content readability using various metrics.
        
        Calculates:
        - Flesch Reading Ease score
        - Flesch-Kincaid Grade Level
        - Average sentence length
        - Complex word ratio
        """
        words = self._extract_words(content)
        sentences = self._extract_sentences(content)
        
        if not words or not sentences:
            return {
                "score": 0,
                "flesch_reading_ease": 0,
                "flesch_kincaid_grade": 0,
                "readability_level": "Unknown",
                "avg_sentence_length": 0,
                "complex_word_ratio": 0
            }
        
        # Count syllables
        total_syllables = sum(self._count_syllables(word) for word in words)
        
        # Calculate metrics
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count
        avg_syllables_per_word = total_syllables / word_count
        
        # Flesch Reading Ease: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        flesch_reading_ease = (
            206.835 
            - 1.015 * avg_sentence_length 
            - 84.6 * avg_syllables_per_word
        )
        flesch_reading_ease = max(0, min(100, flesch_reading_ease))
        
        # Flesch-Kincaid Grade Level: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        flesch_kincaid_grade = (
            0.39 * avg_sentence_length 
            + 11.8 * avg_syllables_per_word 
            - 15.59
        )
        flesch_kincaid_grade = max(0, flesch_kincaid_grade)
        
        # Complex word ratio (words with 3+ syllables)
        complex_words = [w for w in words if self._count_syllables(w) >= 3]
        complex_word_ratio = len(complex_words) / word_count
        
        # Determine readability level
        readability_level = self._get_readability_level(flesch_reading_ease)
        
        # Score readability (higher Flesch Reading Ease is better for general audience)
        # Target: 60-70 (standard/fairly easy)
        readability_score = self._score_range(flesch_reading_ease, 60, 70)
        
        return {
            "score": round(readability_score, 2),
            "flesch_reading_ease": round(flesch_reading_ease, 2),
            "flesch_kincaid_grade": round(flesch_kincaid_grade, 2),
            "readability_level": readability_level,
            "avg_sentence_length": round(avg_sentence_length, 2),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2),
            "complex_word_ratio": round(complex_word_ratio, 4),
            "total_words": word_count,
            "total_sentences": sentence_count
        }
    
    def _analyze_metadata(
        self, title: str, subtitle: str, tags: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze metadata for SEO optimization.
        
        Evaluates:
        - Title optimization
        - Subtitle/description optimization
        - Tag quantity and quality
        """
        title_length = len(title)
        subtitle_length = len(subtitle)
        tag_count = len(tags)
        
        # Score components
        title_score = self._score_range(
            title_length,
            self.optimal_title_length[0],
            self.optimal_title_length[1]
        )
        
        subtitle_score = self._score_range(
            subtitle_length,
            self.optimal_subtitle_length[0],
            self.optimal_subtitle_length[1]
        )
        
        tag_count_score = self._score_range(
            tag_count, self.min_tags, self.max_tags
        )
        
        # Check for keyword-rich title (contains important words)
        title_words = self._extract_words(title.lower())
        meaningful_words = [
            w for w in title_words 
            if w not in self.stop_words and len(w) > 3
        ]
        keyword_rich_title = len(meaningful_words) >= 3
        keyword_richness_score = 100 if keyword_rich_title else 50
        
        overall_metadata_score = (
            title_score * 0.30 +
            subtitle_score * 0.25 +
            tag_count_score * 0.25 +
            keyword_richness_score * 0.20
        )
        
        return {
            "score": round(overall_metadata_score, 2),
            "title_length": title_length,
            "title_optimal_range": self.optimal_title_length,
            "title_score": round(title_score, 2),
            "subtitle_length": subtitle_length,
            "subtitle_optimal_range": self.optimal_subtitle_length,
            "subtitle_score": round(subtitle_score, 2),
            "tag_count": tag_count,
            "tag_count_optimal_range": (self.min_tags, self.max_tags),
            "tag_count_score": round(tag_count_score, 2),
            "keyword_rich_title": keyword_rich_title,
            "keyword_richness_score": round(keyword_richness_score, 2),
            "tags": tags
        }
    
    def _analyze_semantic_relevance(
        self, title: str, content: str, tags: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze semantic relevance and topic coherence.
        
        Evaluates:
        - Title-content alignment
        - Tag-content alignment
        - Topic consistency throughout content
        """
        title_words = set(self._extract_words(title.lower()))
        content_words = self._extract_words(content.lower())
        content_word_set = set(content_words)
        tag_words = set()
        for tag in tags:
            tag_words.update(self._extract_words(tag.lower()))
        
        # Remove stop words for meaningful comparison
        title_keywords = {
            w for w in title_words 
            if w not in self.stop_words and len(w) > 3
        }
        content_keywords = {
            w for w in content_word_set 
            if w not in self.stop_words and len(w) > 3
        }
        tag_keywords = {
            w for w in tag_words 
            if w not in self.stop_words and len(w) > 3
        }
        
        # Calculate alignment scores
        if title_keywords:
            title_content_overlap = len(title_keywords & content_keywords) / len(title_keywords)
        else:
            title_content_overlap = 0.0
        
        if tag_keywords:
            tag_content_overlap = len(tag_keywords & content_keywords) / len(tag_keywords)
        else:
            tag_content_overlap = 0.0
        
        # Analyze topic distribution (check if keywords are distributed throughout)
        topic_distribution = self._analyze_topic_distribution(content_words, title_keywords)
        
        # Score semantic relevance
        title_alignment_score = title_content_overlap * 100
        tag_alignment_score = tag_content_overlap * 100
        distribution_score = topic_distribution * 100
        
        overall_semantic_score = (
            title_alignment_score * 0.40 +
            tag_alignment_score * 0.30 +
            distribution_score * 0.30
        )
        
        return {
            "score": round(overall_semantic_score, 2),
            "title_content_alignment": round(title_content_overlap, 4),
            "title_alignment_score": round(title_alignment_score, 2),
            "tag_content_alignment": round(tag_content_overlap, 4),
            "tag_alignment_score": round(tag_alignment_score, 2),
            "topic_distribution": round(topic_distribution, 4),
            "distribution_score": round(distribution_score, 2),
            "title_keywords_in_content": list(title_keywords & content_keywords),
            "tag_keywords_in_content": list(tag_keywords & content_keywords)
        }
    
    def _calculate_seo_score(
        self,
        structure_analysis: Dict[str, Any],
        keyword_analysis: Dict[str, Any],
        readability_analysis: Dict[str, Any],
        metadata_analysis: Dict[str, Any],
        semantic_analysis: Dict[str, Any]
    ) -> float:
        """
        Calculate overall SEO score based on all analyses.
        
        Weights:
        - Structure: 20%
        - Keywords: 25%
        - Readability: 20%
        - Metadata: 15%
        - Semantic Relevance: 20%
        """
        overall_score = (
            structure_analysis["score"] * 0.20 +
            keyword_analysis["score"] * 0.25 +
            readability_analysis["score"] * 0.20 +
            metadata_analysis["score"] * 0.15 +
            semantic_analysis["score"] * 0.20
        )
        
        return round(overall_score, 2)
    
    def _generate_recommendations(
        self,
        structure_analysis: Dict[str, Any],
        keyword_analysis: Dict[str, Any],
        readability_analysis: Dict[str, Any],
        metadata_analysis: Dict[str, Any],
        semantic_analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Generate actionable SEO improvement recommendations.
        
        Returns list of recommendations with priority, category, and description.
        """
        recommendations = []
        
        # Structure recommendations
        if structure_analysis["title_length_score"] < 80:
            title_len = structure_analysis["title_length"]
            optimal = structure_analysis["title_length_optimal"]
            recommendations.append({
                "priority": "high",
                "category": "structure",
                "issue": f"Title length ({title_len} chars) is not optimal",
                "recommendation": f"Adjust title length to {optimal[0]}-{optimal[1]} characters for better SEO"
            })
        
        if structure_analysis["word_count_score"] < 70:
            word_count = structure_analysis["word_count"]
            optimal = structure_analysis["word_count_optimal"]
            if word_count < optimal[0]:
                recommendations.append({
                    "priority": "high",
                    "category": "structure",
                    "issue": f"Content is too short ({word_count} words)",
                    "recommendation": f"Expand content to at least {optimal[0]} words for better SEO performance"
                })
            else:
                recommendations.append({
                    "priority": "medium",
                    "category": "structure",
                    "issue": f"Content is too long ({word_count} words)",
                    "recommendation": f"Consider condensing to {optimal[1]} words or breaking into multiple posts"
                })
        
        if structure_analysis["heading_count"] < self.min_headings:
            recommendations.append({
                "priority": "medium",
                "category": "structure",
                "issue": f"Insufficient headings ({structure_analysis['heading_count']})",
                "recommendation": f"Add at least {self.min_headings} section headings to improve structure and scannability"
            })
        
        # Keyword recommendations
        if keyword_analysis["density_score"] < 70:
            density = keyword_analysis["keyword_density"]
            optimal = keyword_analysis["keyword_density_optimal"]
            recommendations.append({
                "priority": "high",
                "category": "keywords",
                "issue": f"Keyword density ({density}%) is not optimal",
                "recommendation": f"Adjust primary keyword usage to {optimal[0]}-{optimal[1]}% density"
            })
        
        if not keyword_analysis["title_keyword_match"]:
            primary_kw = keyword_analysis["primary_keyword"]
            recommendations.append({
                "priority": "high",
                "category": "keywords",
                "issue": "Primary keywords not in title",
                "recommendation": f"Include primary keyword '{primary_kw}' in the title for better SEO"
            })
        
        if keyword_analysis["tag_relevance_score"] < 70:
            recommendations.append({
                "priority": "medium",
                "category": "keywords",
                "issue": "Tags have low relevance to content",
                "recommendation": "Update tags to better reflect main topics and keywords in the content"
            })
        
        # Readability recommendations
        if readability_analysis["flesch_reading_ease"] < 50:
            recommendations.append({
                "priority": "medium",
                "category": "readability",
                "issue": "Content is difficult to read",
                "recommendation": "Simplify sentence structure and use shorter sentences for better readability"
            })
        elif readability_analysis["flesch_reading_ease"] > 80:
            recommendations.append({
                "priority": "low",
                "category": "readability",
                "issue": "Content may be too simple",
                "recommendation": "Consider adding more depth and complexity for target audience"
            })
        
        if readability_analysis["avg_sentence_length"] > 25:
            recommendations.append({
                "priority": "medium",
                "category": "readability",
                "issue": f"Sentences are too long (avg {readability_analysis['avg_sentence_length']} words)",
                "recommendation": "Break long sentences into shorter ones for better readability"
            })
        
        # Metadata recommendations
        if metadata_analysis["subtitle_score"] < 70:
            sub_len = metadata_analysis["subtitle_length"]
            optimal = metadata_analysis["subtitle_optimal_range"]
            recommendations.append({
                "priority": "medium",
                "category": "metadata",
                "issue": f"Subtitle length ({sub_len} chars) is not optimal",
                "recommendation": f"Adjust subtitle to {optimal[0]}-{optimal[1]} characters"
            })
        
        if metadata_analysis["tag_count"] < self.min_tags:
            recommendations.append({
                "priority": "medium",
                "category": "metadata",
                "issue": f"Too few tags ({metadata_analysis['tag_count']})",
                "recommendation": f"Add more relevant tags (minimum {self.min_tags})"
            })
        elif metadata_analysis["tag_count"] > self.max_tags:
            recommendations.append({
                "priority": "low",
                "category": "metadata",
                "issue": f"Too many tags ({metadata_analysis['tag_count']})",
                "recommendation": f"Reduce to {self.max_tags} most relevant tags"
            })
        
        if not metadata_analysis["keyword_rich_title"]:
            recommendations.append({
                "priority": "high",
                "category": "metadata",
                "issue": "Title lacks meaningful keywords",
                "recommendation": "Include more descriptive, keyword-rich words in the title"
            })
        
        # Semantic recommendations
        if semantic_analysis["title_alignment_score"] < 70:
            recommendations.append({
                "priority": "high",
                "category": "semantic",
                "issue": "Title and content are not well aligned",
                "recommendation": "Ensure content thoroughly covers topics mentioned in the title"
            })
        
        if semantic_analysis["tag_alignment_score"] < 60:
            recommendations.append({
                "priority": "medium",
                "category": "semantic",
                "issue": "Tags don't match content topics",
                "recommendation": "Choose tags that better reflect the actual content topics"
            })
        
        if semantic_analysis["distribution_score"] < 60:
            recommendations.append({
                "priority": "medium",
                "category": "semantic",
                "issue": "Main topics not distributed throughout content",
                "recommendation": "Ensure main keywords and topics appear consistently throughout the article"
            })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda x: priority_order[x["priority"]])
        
        return recommendations
    
    def _generate_summary(self, seo_score: float, recommendations: List[Dict[str, str]]) -> str:
        """Generate a human-readable summary of the SEO analysis."""
        grade = self._get_grade(seo_score)
        
        high_priority = len([r for r in recommendations if r["priority"] == "high"])
        medium_priority = len([r for r in recommendations if r["priority"] == "medium"])
        low_priority = len([r for r in recommendations if r["priority"] == "low"])
        
        summary = f"SEO Score: {seo_score}/100 (Grade: {grade})\n\n"
        
        if seo_score >= 90:
            summary += "Excellent! This content is highly optimized for SEO."
        elif seo_score >= 80:
            summary += "Good! This content has strong SEO with minor improvements possible."
        elif seo_score >= 70:
            summary += "Fair. This content has decent SEO but could benefit from optimization."
        elif seo_score >= 60:
            summary += "Needs improvement. Several SEO issues should be addressed."
        else:
            summary += "Poor. Significant SEO optimization is required."
        
        summary += f"\n\nFound {len(recommendations)} recommendations: "
        summary += f"{high_priority} high priority, {medium_priority} medium priority, {low_priority} low priority."
        
        return summary
    
    # Helper methods
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text, removing punctuation."""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return words
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_headings(self, text: str) -> List[str]:
        """
        Extract potential headings from text.
        Simple heuristic: lines that are short and may start with capital letters.
        """
        lines = text.split('\n')
        headings = []
        for line in lines:
            line = line.strip()
            # Potential heading: short line (< 100 chars), not empty, starts with capital
            if line and len(line) < 100 and line[0].isupper() and not line.endswith('.'):
                words = line.split()
                # Check if it's actually a heading (not a regular sentence)
                if len(words) <= 12:
                    headings.append(line)
        return headings
    
    def _extract_ngrams(self, words: List[str], n: int) -> List[Tuple[str, ...]]:
        """Extract n-grams from word list."""
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i:i+n])
            # Exclude ngrams with stop words
            if not any(word in self.stop_words for word in ngram):
                ngrams.append(ngram)
        return ngrams
    
    def _count_syllables(self, word: str) -> int:
        """
        Count syllables in a word using a simple heuristic.
        """
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent e
        if word.endswith('e'):
            syllable_count -= 1
        
        # Ensure at least one syllable
        if syllable_count == 0:
            syllable_count = 1
        
        return syllable_count
    
    def _score_range(self, value: float, min_optimal: float, max_optimal: float) -> float:
        """
        Score a value based on optimal range.
        Returns 100 if in range, decreases as value moves away from range.
        """
        if min_optimal <= value <= max_optimal:
            return 100.0
        elif value < min_optimal:
            # Score decreases as we go below minimum
            diff = min_optimal - value
            penalty = (diff / min_optimal) * 100
            return max(0, 100 - penalty)
        else:
            # Score decreases as we go above maximum
            diff = value - max_optimal
            penalty = (diff / max_optimal) * 100
            return max(0, 100 - penalty)
    
    def _calculate_tag_relevance(
        self, tags: List[str], content_words: List[str], word_freq: Counter
    ) -> float:
        """Calculate how relevant tags are to the content."""
        if not tags:
            return 0.0
        
        tag_words = []
        for tag in tags:
            tag_words.extend(self._extract_words(tag.lower()))
        
        # Check how many tag words appear in content
        relevant_count = 0
        for tag_word in tag_words:
            if tag_word in content_words and tag_word not in self.stop_words:
                relevant_count += 1
        
        if not tag_words:
            return 0.0
        
        relevance = relevant_count / len(tag_words)
        return min(1.0, relevance)
    
    def _analyze_topic_distribution(
        self, content_words: List[str], title_keywords: set
    ) -> float:
        """
        Analyze how well main topics are distributed throughout content.
        Checks if title keywords appear throughout the content, not just in one section.
        """
        if not title_keywords or not content_words:
            return 0.0
        
        # Divide content into quarters
        quarter_size = len(content_words) // 4
        if quarter_size == 0:
            return 0.0
        
        quarters = [
            set(content_words[i:i+quarter_size])
            for i in range(0, len(content_words), quarter_size)
        ]
        
        # Check how many quarters contain title keywords
        quarters_with_keywords = 0
        for quarter in quarters:
            if any(keyword in quarter for keyword in title_keywords):
                quarters_with_keywords += 1
        
        distribution = quarters_with_keywords / len(quarters)
        return distribution
    
    def _get_readability_level(self, flesch_score: float) -> str:
        """Convert Flesch Reading Ease score to readability level."""
        if flesch_score >= 90:
            return "Very Easy (5th grade)"
        elif flesch_score >= 80:
            return "Easy (6th grade)"
        elif flesch_score >= 70:
            return "Fairly Easy (7th grade)"
        elif flesch_score >= 60:
            return "Standard (8th-9th grade)"
        elif flesch_score >= 50:
            return "Fairly Difficult (10th-12th grade)"
        elif flesch_score >= 30:
            return "Difficult (College)"
        else:
            return "Very Difficult (College graduate)"
    
    def _get_grade(self, score: float) -> str:
        """Convert numerical score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
