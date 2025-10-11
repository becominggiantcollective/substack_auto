"""
Fact-Checker Agent for validating claims and assessing SEO compliance.

This agent extracts claims and statistics from content, validates them against
trusted sources, and provides SEO recommendations.
"""
import re
import logging
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from openai import OpenAI

from config.settings import settings
from agents import BaseAgent

logger = logging.getLogger(__name__)


class FactCheckerAgent(BaseAgent):
    """
    Agent that validates factual accuracy of claims and assesses SEO compliance.
    
    Features:
    - Extracts claims and statistics from content
    - Validates claims using AI and external sources
    - Assesses SEO impact of claims
    - Generates detailed reports with confidence scores
    """
    
    def __init__(self):
        """Initialize the fact-checker agent."""
        super().__init__("FactCheckerAgent")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.confidence_threshold = 0.7  # Minimum confidence for validation
    
    def process(self, content: Dict) -> Dict:
        """
        Process content and validate claims.
        
        Args:
            content: Dictionary containing 'title' and 'content' keys
            
        Returns:
            Dictionary with validation results, flagged claims, and SEO report
        """
        if not self.validate_input(content):
            return {
                "error": "Invalid input format",
                "valid": False
            }
        
        self.logger.info(f"Processing content: {content.get('title', 'Untitled')}")
        
        # Extract claims and statistics
        claims = self._extract_claims(content)
        
        # Validate each claim
        validation_results = []
        for claim in claims:
            result = self._validate_claim(claim, content)
            validation_results.append(result)
        
        # Assess SEO impact
        seo_report = self._assess_seo_impact(claims, validation_results)
        
        # Generate summary report
        report = self._generate_report(claims, validation_results, seo_report)
        
        self.logger.info(f"Fact-checking complete: {len(claims)} claims processed")
        
        return report
    
    def validate_input(self, content: Dict) -> bool:
        """
        Validate input content structure.
        
        Args:
            content: Content dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not super().validate_input(content):
            return False
        
        required_keys = ["title", "content"]
        return all(key in content for key in required_keys)
    
    def _extract_claims(self, content: Dict) -> List[Dict]:
        """
        Extract factual claims and statistics from content using AI.
        
        Args:
            content: Content dictionary
            
        Returns:
            List of claim dictionaries with text and type
        """
        title = content.get("title", "")
        text = content.get("content", "")
        
        # Use AI to identify claims and statistics
        prompt = f"""
        Analyze the following article and extract all factual claims and statistics.
        
        Title: {title}
        
        Content: {text}
        
        For each claim or statistic, provide:
        1. The exact claim text
        2. The type (statistic, fact, prediction, or opinion)
        3. A brief context
        
        Return the results as a JSON array with this structure:
        [
          {{
            "text": "exact claim text",
            "type": "statistic|fact|prediction|opinion",
            "context": "brief surrounding context"
          }}
        ]
        
        Focus on claims that can be verified and statistics with specific numbers.
        Ignore vague statements and purely subjective opinions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert fact-checker who extracts verifiable claims from text. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            
            # Parse JSON response
            import json
            claims = json.loads(result)
            
            # Add metadata
            for i, claim in enumerate(claims):
                claim["id"] = i + 1
                claim["extracted_at"] = datetime.now().isoformat()
            
            self.logger.info(f"Extracted {len(claims)} claims from content")
            return claims
            
        except Exception as e:
            self.logger.error(f"Error extracting claims: {e}")
            # Fallback: extract statistics using regex
            return self._extract_claims_fallback(text)
    
    def _extract_claims_fallback(self, text: str) -> List[Dict]:
        """
        Fallback method to extract claims using regex patterns.
        
        Args:
            text: Content text
            
        Returns:
            List of claim dictionaries
        """
        claims = []
        claim_id = 1
        
        # Pattern for statistics (numbers with units or percentages)
        stat_pattern = r'(\d+(?:\.\d+)?)\s*(%|percent|million|billion|thousand|users|people|times)'
        matches = re.finditer(stat_pattern, text, re.IGNORECASE)
        
        for match in matches:
            # Get context (surrounding text)
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text[start:end].strip()
            
            claims.append({
                "id": claim_id,
                "text": match.group(0),
                "type": "statistic",
                "context": context,
                "extracted_at": datetime.now().isoformat()
            })
            claim_id += 1
        
        self.logger.info(f"Fallback extraction found {len(claims)} statistical claims")
        return claims
    
    def _validate_claim(self, claim: Dict, content: Dict) -> Dict:
        """
        Validate a single claim using AI analysis.
        
        Args:
            claim: Claim dictionary
            content: Original content for context
            
        Returns:
            Validation result dictionary
        """
        claim_text = claim.get("text", "")
        claim_type = claim.get("type", "fact")
        context = claim.get("context", "")
        
        # Use AI to assess claim validity
        prompt = f"""
        Evaluate the following claim for factual accuracy:
        
        Claim: {claim_text}
        Type: {claim_type}
        Context: {context}
        
        Provide your assessment in JSON format:
        {{
          "is_valid": true/false,
          "confidence_score": 0.0-1.0,
          "reasoning": "brief explanation",
          "potential_sources": ["list of suggested verification sources"],
          "flags": ["any concerns or warnings"],
          "seo_value": "high|medium|low",
          "seo_reasoning": "why this claim has SEO value"
        }}
        
        Consider:
        - Factual accuracy based on general knowledge
        - Whether the claim is verifiable
        - Potential for misinformation
        - SEO value (specific data, featured snippet potential)
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional fact-checker with expertise in verifying claims and assessing SEO value. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            result = response.choices[0].message.content
            
            # Parse JSON response
            import json
            validation = json.loads(result)
            
            # Add claim reference
            validation["claim_id"] = claim.get("id")
            validation["claim_text"] = claim_text
            validation["validated_at"] = datetime.now().isoformat()
            
            # Determine if claim needs review
            validation["needs_review"] = (
                not validation.get("is_valid", False) or
                validation.get("confidence_score", 0) < self.confidence_threshold or
                len(validation.get("flags", [])) > 0
            )
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error validating claim: {e}")
            # Return conservative validation result
            return {
                "claim_id": claim.get("id"),
                "claim_text": claim_text,
                "is_valid": False,
                "confidence_score": 0.0,
                "reasoning": f"Validation error: {str(e)}",
                "potential_sources": [],
                "flags": ["validation_error"],
                "needs_review": True,
                "seo_value": "unknown",
                "seo_reasoning": "Could not assess due to validation error",
                "validated_at": datetime.now().isoformat()
            }
    
    def _assess_seo_impact(self, claims: List[Dict], validations: List[Dict]) -> Dict:
        """
        Assess the SEO impact of claims and statistics.
        
        Args:
            claims: List of extracted claims
            validations: List of validation results
            
        Returns:
            SEO assessment report
        """
        # Count SEO value ratings
        seo_values = {"high": 0, "medium": 0, "low": 0, "unknown": 0}
        high_value_claims = []
        
        for validation in validations:
            seo_value = validation.get("seo_value", "unknown")
            seo_values[seo_value] = seo_values.get(seo_value, 0) + 1
            
            if seo_value == "high":
                high_value_claims.append({
                    "claim": validation.get("claim_text"),
                    "reasoning": validation.get("seo_reasoning")
                })
        
        # Calculate overall SEO score
        total_claims = len(validations)
        if total_claims == 0:
            seo_score = 0.0
        else:
            seo_score = (
                (seo_values["high"] * 1.0 + 
                 seo_values["medium"] * 0.6 + 
                 seo_values["low"] * 0.3) / total_claims
            )
        
        # Generate recommendations
        recommendations = []
        
        if seo_values["high"] == 0:
            recommendations.append("Add specific statistics or data points to improve featured snippet potential")
        
        if seo_values["low"] > seo_values["high"]:
            recommendations.append("Replace vague statements with concrete, verifiable facts")
        
        if len(validations) < 3:
            recommendations.append("Include more factual claims to establish authority")
        
        if seo_score >= 0.7:
            recommendations.append("Strong SEO foundation - claims are specific and valuable")
        
        return {
            "seo_score": round(seo_score, 2),
            "total_claims": total_claims,
            "seo_distribution": seo_values,
            "high_value_claims": high_value_claims,
            "recommendations": recommendations,
            "featured_snippet_potential": seo_score >= 0.7
        }
    
    def _generate_report(self, claims: List[Dict], validations: List[Dict], seo_report: Dict) -> Dict:
        """
        Generate comprehensive fact-checking and SEO report.
        
        Args:
            claims: List of extracted claims
            validations: List of validation results
            seo_report: SEO assessment report
            
        Returns:
            Complete report dictionary
        """
        # Categorize validations
        flagged_claims = [v for v in validations if v.get("needs_review", False)]
        valid_claims = [v for v in validations if v.get("is_valid", False) and not v.get("needs_review", False)]
        
        # Calculate overall confidence
        if validations:
            avg_confidence = sum(v.get("confidence_score", 0) for v in validations) / len(validations)
        else:
            avg_confidence = 0.0
        
        # Generate actionable recommendations
        recommendations = []
        
        for flagged in flagged_claims:
            rec = {
                "claim": flagged.get("claim_text"),
                "issue": flagged.get("reasoning"),
                "action": "Verify with sources: " + ", ".join(flagged.get("potential_sources", ["general research"])),
                "confidence": flagged.get("confidence_score", 0)
            }
            recommendations.append(rec)
        
        # Summary statistics
        summary = {
            "total_claims_extracted": len(claims),
            "claims_validated": len(validations),
            "valid_claims": len(valid_claims),
            "flagged_claims": len(flagged_claims),
            "average_confidence": round(avg_confidence, 2),
            "overall_status": "pass" if len(flagged_claims) == 0 else "review_needed"
        }
        
        return {
            "summary": summary,
            "claims": claims,
            "validations": validations,
            "flagged_claims": flagged_claims,
            "recommendations": recommendations,
            "seo_report": seo_report,
            "generated_at": datetime.now().isoformat(),
            "agent": self.name
        }
    
    def check_article_quality(self, content: Dict) -> Dict:
        """
        Quick quality check for an article.
        
        Args:
            content: Article content dictionary
            
        Returns:
            Quick quality assessment
        """
        report = self.process(content)
        
        summary = report.get("summary", {})
        seo_report = report.get("seo_report", {})
        
        quality_score = (
            (summary.get("average_confidence", 0) * 0.5) +
            (seo_report.get("seo_score", 0) * 0.3) +
            ((1 - (summary.get("flagged_claims", 0) / max(summary.get("total_claims_extracted", 1), 1))) * 0.2)
        )
        
        return {
            "quality_score": round(quality_score, 2),
            "passes_quality_check": quality_score >= 0.7,
            "confidence": summary.get("average_confidence", 0),
            "seo_score": seo_report.get("seo_score", 0),
            "issues_count": summary.get("flagged_claims", 0),
            "recommendation": "Publish" if quality_score >= 0.8 else "Review before publishing" if quality_score >= 0.6 else "Needs revision"
        }


__all__ = ["FactCheckerAgent"]
