"""
Fact-Checker Agent for validating factual accuracy and SEO compliance.

This module provides automated fact-checking capabilities for article content,
including claim extraction, validation, confidence scoring, and SEO impact assessment.
"""
import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)


class FactCheckerAgent:
    """Agent for validating claims and ensuring SEO compliance in articles."""
    
    def __init__(self):
        """Initialize the fact-checker agent with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4"
        
    def extract_claims(self, content: str) -> List[Dict[str, str]]:
        """
        Extract factual claims and statistics from article content.
        
        Args:
            content: The article content to analyze
            
        Returns:
            List of dictionaries containing claim text and type
        """
        try:
            prompt = f"""
            Analyze the following article content and extract all factual claims and statistics.
            For each claim, identify:
            1. The exact claim text
            2. The type (statistic, fact, prediction, opinion)
            3. Whether it's verifiable
            
            Article content:
            {content}
            
            Return the claims in this format:
            CLAIM: [exact text]
            TYPE: [statistic/fact/prediction/opinion]
            VERIFIABLE: [yes/no]
            ---
            
            Extract all significant claims. If there are no claims, return "NO_CLAIMS_FOUND".
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3
            )
            
            claims_text = response.choices[0].message.content.strip()
            
            if "NO_CLAIMS_FOUND" in claims_text:
                logger.info("No factual claims found in content")
                return []
            
            # Parse the structured response
            claims = []
            claim_blocks = claims_text.split("---")
            
            for block in claim_blocks:
                if not block.strip():
                    continue
                    
                claim_match = re.search(r'CLAIM:\s*(.+?)(?=\nTYPE:|\nVERIFIABLE:|$)', block, re.DOTALL)
                type_match = re.search(r'TYPE:\s*(.+?)(?=\nVERIFIABLE:|$)', block, re.DOTALL)
                verifiable_match = re.search(r'VERIFIABLE:\s*(.+?)$', block, re.DOTALL)
                
                if claim_match:
                    claims.append({
                        "claim": claim_match.group(1).strip(),
                        "type": type_match.group(1).strip() if type_match else "unknown",
                        "verifiable": verifiable_match.group(1).strip().lower() if verifiable_match else "unknown"
                    })
            
            logger.info(f"Extracted {len(claims)} claims from content")
            return claims
            
        except Exception as e:
            logger.error(f"Error extracting claims: {e}")
            return []
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def validate_claim(self, claim: str) -> Dict[str, any]:
        """
        Validate a single claim using AI analysis.
        
        In production, this would use external APIs like Google Search API or Wikipedia API.
        For this implementation, we use GPT-4 to assess claim plausibility.
        
        Args:
            claim: The claim to validate
            
        Returns:
            Dictionary with validation results including confidence score
        """
        try:
            prompt = f"""
            Analyze the following claim for factual accuracy:
            
            Claim: "{claim}"
            
            Provide:
            1. CONFIDENCE: A score from 0-100 indicating how confident you are this claim is accurate
            2. ASSESSMENT: One of: ACCURATE, LIKELY_ACCURATE, UNCERTAIN, LIKELY_INACCURATE, INACCURATE
            3. REASONING: Brief explanation of your assessment
            4. SOURCES_NEEDED: Whether external sources are needed to verify (yes/no)
            5. SEO_POTENTIAL: Whether this claim could enhance SEO (high/medium/low)
            
            Format your response exactly as:
            CONFIDENCE: [number]
            ASSESSMENT: [assessment]
            REASONING: [reasoning]
            SOURCES_NEEDED: [yes/no]
            SEO_POTENTIAL: [high/medium/low]
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.2
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse the structured response
            confidence_match = re.search(r'CONFIDENCE:\s*(\d+)', result_text)
            assessment_match = re.search(r'ASSESSMENT:\s*(.+?)(?=\n|$)', result_text)
            reasoning_match = re.search(r'REASONING:\s*(.+?)(?=\nSOURCES_NEEDED:|$)', result_text, re.DOTALL)
            sources_match = re.search(r'SOURCES_NEEDED:\s*(.+?)(?=\n|$)', result_text)
            seo_match = re.search(r'SEO_POTENTIAL:\s*(.+?)(?=\n|$)', result_text)
            
            return {
                "claim": claim,
                "confidence_score": int(confidence_match.group(1)) if confidence_match else 50,
                "assessment": assessment_match.group(1).strip() if assessment_match else "UNCERTAIN",
                "reasoning": reasoning_match.group(1).strip() if reasoning_match else "",
                "sources_needed": sources_match.group(1).strip().lower() == "yes" if sources_match else True,
                "seo_potential": seo_match.group(1).strip().lower() if seo_match else "low",
                "validated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validating claim: {e}")
            return {
                "claim": claim,
                "confidence_score": 0,
                "assessment": "ERROR",
                "reasoning": f"Validation error: {str(e)}",
                "sources_needed": True,
                "seo_potential": "unknown",
                "validated_at": datetime.now().isoformat()
            }
    
    def assess_seo_impact(self, claims: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Assess the overall SEO impact of claims in the article.
        
        Args:
            claims: List of validated claims
            
        Returns:
            Dictionary with SEO impact analysis
        """
        if not claims:
            return {
                "overall_score": 0,
                "featured_snippet_potential": "low",
                "recommendations": ["Add factual claims and statistics to improve SEO"]
            }
        
        # Calculate SEO metrics
        high_potential_claims = [c for c in claims if c.get("seo_potential") == "high"]
        medium_potential_claims = [c for c in claims if c.get("seo_potential") == "medium"]
        
        # Score calculation
        seo_score = (
            len(high_potential_claims) * 30 +
            len(medium_potential_claims) * 15 +
            len(claims) * 5
        )
        seo_score = min(seo_score, 100)  # Cap at 100
        
        # Determine featured snippet potential
        if len(high_potential_claims) >= 2:
            snippet_potential = "high"
        elif len(high_potential_claims) >= 1 or len(medium_potential_claims) >= 2:
            snippet_potential = "medium"
        else:
            snippet_potential = "low"
        
        # Generate recommendations
        recommendations = []
        if len(high_potential_claims) < 2:
            recommendations.append("Add more statistics or data points to increase featured snippet potential")
        if seo_score < 50:
            recommendations.append("Include more verifiable facts and figures")
        if snippet_potential == "low":
            recommendations.append("Format key statistics as clear, quotable statements")
        
        return {
            "overall_score": seo_score,
            "featured_snippet_potential": snippet_potential,
            "high_seo_claims": len(high_potential_claims),
            "medium_seo_claims": len(medium_potential_claims),
            "total_claims": len(claims),
            "recommendations": recommendations if recommendations else ["SEO optimization is good"]
        }
    
    def check_article(self, title: str, content: str) -> Dict[str, any]:
        """
        Perform complete fact-checking and SEO analysis on an article.
        
        Args:
            title: Article title
            content: Article content
            
        Returns:
            Comprehensive report with validation results and recommendations
        """
        logger.info(f"Starting fact-check for article: {title}")
        
        try:
            # Extract claims
            claims = self.extract_claims(content)
            
            # Validate each claim
            validated_claims = []
            for claim_info in claims:
                if claim_info.get("verifiable", "").lower() == "yes":
                    validation = self.validate_claim(claim_info["claim"])
                    validated_claims.append({
                        **claim_info,
                        **validation
                    })
                else:
                    # Non-verifiable claims get a default validation
                    validated_claims.append({
                        **claim_info,
                        "confidence_score": None,
                        "assessment": "NON_VERIFIABLE",
                        "reasoning": "This claim is not objectively verifiable",
                        "sources_needed": False,
                        "seo_potential": "low"
                    })
            
            # Assess SEO impact
            verifiable_claims = [c for c in validated_claims if c.get("confidence_score") is not None]
            seo_analysis = self.assess_seo_impact(verifiable_claims)
            
            # Calculate overall metrics
            if validated_claims:
                avg_confidence = sum(
                    c.get("confidence_score", 0) 
                    for c in validated_claims 
                    if c.get("confidence_score") is not None
                ) / len([c for c in validated_claims if c.get("confidence_score") is not None]) if any(c.get("confidence_score") is not None for c in validated_claims) else 0
            else:
                avg_confidence = 0
            
            # Flag problematic claims
            flagged_claims = [
                c for c in validated_claims 
                if c.get("confidence_score") is not None and c["confidence_score"] < 60
            ]
            
            # Generate recommendations
            recommendations = []
            if flagged_claims:
                recommendations.append(f"Review {len(flagged_claims)} low-confidence claims for accuracy")
            if avg_confidence < 70:
                recommendations.append("Consider adding more well-established facts")
            recommendations.extend(seo_analysis["recommendations"])
            
            report = {
                "article_title": title,
                "analysis_timestamp": datetime.now().isoformat(),
                "claims_extracted": len(claims),
                "claims_validated": len(validated_claims),
                "flagged_claims_count": len(flagged_claims),
                "average_confidence": round(avg_confidence, 2),
                "claims": validated_claims,
                "flagged_claims": flagged_claims,
                "seo_analysis": seo_analysis,
                "recommendations": recommendations,
                "overall_status": "PASS" if len(flagged_claims) == 0 and avg_confidence >= 70 else "REVIEW_NEEDED"
            }
            
            logger.info(f"Fact-check complete. Status: {report['overall_status']}")
            return report
            
        except Exception as e:
            logger.error(f"Error during fact-checking: {e}")
            return {
                "article_title": title,
                "analysis_timestamp": datetime.now().isoformat(),
                "error": str(e),
                "overall_status": "ERROR",
                "recommendations": ["Unable to complete fact-checking. Please review manually."]
            }
    
    def generate_report(self, check_result: Dict[str, any], output_format: str = "text") -> str:
        """
        Generate a formatted report from fact-checking results.
        
        Args:
            check_result: Results from check_article()
            output_format: Format for the report ("text" or "markdown")
            
        Returns:
            Formatted report string
        """
        if output_format == "markdown":
            return self._generate_markdown_report(check_result)
        else:
            return self._generate_text_report(check_result)
    
    def _generate_text_report(self, result: Dict[str, any]) -> str:
        """Generate a plain text report."""
        lines = [
            "=" * 70,
            "FACT-CHECKER REPORT",
            "=" * 70,
            f"Article: {result.get('article_title', 'N/A')}",
            f"Analysis Date: {result.get('analysis_timestamp', 'N/A')}",
            f"Overall Status: {result.get('overall_status', 'N/A')}",
            "",
            "SUMMARY:",
            f"  Claims Extracted: {result.get('claims_extracted', 0)}",
            f"  Claims Validated: {result.get('claims_validated', 0)}",
            f"  Flagged Claims: {result.get('flagged_claims_count', 0)}",
            f"  Average Confidence: {result.get('average_confidence', 0)}%",
            ""
        ]
        
        if result.get('seo_analysis'):
            seo = result['seo_analysis']
            lines.extend([
                "SEO ANALYSIS:",
                f"  Overall SEO Score: {seo.get('overall_score', 0)}/100",
                f"  Featured Snippet Potential: {seo.get('featured_snippet_potential', 'N/A').upper()}",
                f"  High-Impact Claims: {seo.get('high_seo_claims', 0)}",
                ""
            ])
        
        if result.get('flagged_claims'):
            lines.extend(["FLAGGED CLAIMS (Low Confidence):"])
            for claim in result['flagged_claims']:
                lines.extend([
                    f"  - {claim['claim'][:80]}...",
                    f"    Confidence: {claim.get('confidence_score', 0)}%",
                    f"    Assessment: {claim.get('assessment', 'N/A')}",
                    ""
                ])
        
        if result.get('recommendations'):
            lines.extend(["RECOMMENDATIONS:"])
            for rec in result['recommendations']:
                lines.append(f"  • {rec}")
            lines.append("")
        
        lines.append("=" * 70)
        return "\n".join(lines)
    
    def _generate_markdown_report(self, result: Dict[str, any]) -> str:
        """Generate a markdown formatted report."""
        lines = [
            "# Fact-Checker Report",
            "",
            f"**Article:** {result.get('article_title', 'N/A')}  ",
            f"**Analysis Date:** {result.get('analysis_timestamp', 'N/A')}  ",
            f"**Overall Status:** {result.get('overall_status', 'N/A')}",
            "",
            "## Summary",
            "",
            f"- **Claims Extracted:** {result.get('claims_extracted', 0)}",
            f"- **Claims Validated:** {result.get('claims_validated', 0)}",
            f"- **Flagged Claims:** {result.get('flagged_claims_count', 0)}",
            f"- **Average Confidence:** {result.get('average_confidence', 0)}%",
            ""
        ]
        
        if result.get('seo_analysis'):
            seo = result['seo_analysis']
            lines.extend([
                "## SEO Analysis",
                "",
                f"- **Overall SEO Score:** {seo.get('overall_score', 0)}/100",
                f"- **Featured Snippet Potential:** {seo.get('featured_snippet_potential', 'N/A').upper()}",
                f"- **High-Impact Claims:** {seo.get('high_seo_claims', 0)}",
                f"- **Medium-Impact Claims:** {seo.get('medium_seo_claims', 0)}",
                ""
            ])
        
        if result.get('flagged_claims'):
            lines.extend(["## Flagged Claims (Low Confidence)", ""])
            for claim in result['flagged_claims']:
                lines.extend([
                    f"### {claim['claim'][:100]}",
                    f"- **Confidence:** {claim.get('confidence_score', 0)}%",
                    f"- **Assessment:** {claim.get('assessment', 'N/A')}",
                    f"- **Reasoning:** {claim.get('reasoning', 'N/A')}",
                    ""
                ])
        
        if result.get('recommendations'):
            lines.extend(["## Recommendations", ""])
            for rec in result['recommendations']:
                lines.append(f"- {rec}")
            lines.append("")
        
        return "\n".join(lines)
