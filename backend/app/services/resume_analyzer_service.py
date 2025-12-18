"""
Resume Analyzer Service - AI-powered resume analysis and enhancement suggestions.
"""
from typing import Dict, List, Tuple
from app.services.ai_service import AIService, SYSTEM_PROMPT
from app.core.security import sanitize_input


class ResumeAnalyzerService:
    """Service for analyzing resumes and generating enhancement suggestions."""
    
    # Scoring weights
    SCORE_WEIGHTS = {
        "content_quality": 0.35,
        "ats_optimization": 0.30,
        "structure": 0.20,
        "fresher_specific": 0.15
    }
    
    @staticmethod
    def analyze_content_quality(parsed_data: Dict, metrics: Dict) -> Tuple[float, List[Dict]]:
        """
        Analyze content quality and generate suggestions.
        
        Returns:
            Tuple of (score, suggestions_list)
        """
        score = 100.0
        suggestions = []
        
        # Check for action verbs
        if metrics["action_verbs"] < 5:
            score -= 15
            suggestions.append({
                "category": "content_quality",
                "section": "experience",
                "severity": "high",
                "issue": "Limited use of action verbs",
                "suggestion": "Start bullet points with strong action verbs like 'Developed', 'Implemented', 'Led', etc.",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check for quantifiable achievements
        if metrics["quantifiable_achievements"] < 3:
            score -= 20
            suggestions.append({
                "category": "content_quality",
                "section": "experience",
                "severity": "critical",
                "issue": "Lack of quantifiable achievements",
                "suggestion": "Add numbers and metrics to demonstrate impact (e.g., 'Improved performance by 30%')",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check summary section
        summary_text = parsed_data.get("summary", "")
        if not summary_text or len(summary_text) < 50:
            score -= 15
            suggestions.append({
                "category": "content_quality",
                "section": "summary",
                "severity": "high",
                "issue": "Missing or weak professional summary",
                "suggestion": "Add a compelling 2-3 sentence summary highlighting your key skills and career goals",
                "original_text": summary_text,
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check for passive voice (basic check)
        text_lower = (parsed_data.get("experience", "") + parsed_data.get("projects", "")).lower()
        passive_indicators = ["was", "were", "been", "being"]
        passive_count = sum(text_lower.count(word) for word in passive_indicators)
        
        if passive_count > 5:
            score -= 10
            suggestions.append({
                "category": "content_quality",
                "section": "experience",
                "severity": "medium",
                "issue": "Excessive use of passive voice",
                "suggestion": "Rewrite sentences in active voice to demonstrate ownership and impact",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        return max(0, score), suggestions
    
    @staticmethod
    def analyze_ats_optimization(parsed_data: Dict, metrics: Dict) -> Tuple[float, List[Dict]]:
        """
        Analyze ATS (Applicant Tracking System) compatibility.
        
        Returns:
            Tuple of (score, suggestions_list)
        """
        score = 100.0
        suggestions = []
        
        # Check contact information
        if not metrics["has_email"]:
            score -= 20
            suggestions.append({
                "category": "ats_optimization",
                "section": "contact",
                "severity": "critical",
                "issue": "Missing email address",
                "suggestion": "Add a professional email address at the top of your resume",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        if not metrics["has_phone"]:
            score -= 15
            suggestions.append({
                "category": "ats_optimization",
                "section": "contact",
                "severity": "high",
                "issue": "Missing phone number",
                "suggestion": "Include a valid phone number for recruiters to contact you",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check for standard section headers
        required_sections = ["education", "skills"]
        for section in required_sections:
            if not parsed_data.get(section, "").strip():
                score -= 15
                suggestions.append({
                    "category": "ats_optimization",
                    "section": section,
                    "severity": "critical",
                    "issue": f"Missing {section.capitalize()} section",
                    "suggestion": f"Add a dedicated {section.capitalize()} section with relevant information",
                    "original_text": "",
                    "enhanced_text": "",
                    "accepted": False
                })
        
        # Check technical skills format
        skills_text = parsed_data.get("skills", "")
        if skills_text and "," not in skills_text and "|" not in skills_text:
            score -= 10
            suggestions.append({
                "category": "ats_optimization",
                "section": "skills",
                "severity": "medium",
                "issue": "Skills not properly formatted",
                "suggestion": "List skills separated by commas or bullet points for better ATS parsing",
                "original_text": skills_text[:100],
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check for common ATS-friendly keywords for freshers
        fresher_keywords = ["internship", "project", "coursework", "certification", "training"]
        full_text = " ".join(parsed_data.values()).lower()
        keyword_count = sum(1 for kw in fresher_keywords if kw in full_text)
        
        if keyword_count < 2:
            score -= 10
            suggestions.append({
                "category": "ats_optimization",
                "section": "general",
                "severity": "medium",
                "issue": "Limited fresher-relevant keywords",
                "suggestion": "Include keywords like 'internship', 'project', 'certification' to improve ATS matching",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        return max(0, score), suggestions
    
    @staticmethod
    def analyze_structure(parsed_data: Dict, metrics: Dict) -> Tuple[float, List[Dict]]:
        """
        Analyze resume structure and formatting.
        
        Returns:
            Tuple of (score, suggestions_list)
        """
        score = 100.0
        suggestions = []
        
        # Check resume length (ideal for freshers: 1 page = ~400-600 words)
        word_count = metrics["word_count"]
        
        if word_count < 300:
            score -= 20
            suggestions.append({
                "category": "structure",
                "section": "general",
                "severity": "high",
                "issue": "Resume is too short",
                "suggestion": "Expand your resume with more details about projects, skills, and experiences",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        elif word_count > 800:
            score -= 15
            suggestions.append({
                "category": "structure",
                "section": "general",
                "severity": "medium",
                "issue": "Resume is too lengthy",
                "suggestion": "Condense your resume to 1 page by removing less relevant information",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check for bullet points
        if metrics["bullet_points"] < 3:
            score -= 15
            suggestions.append({
                "category": "structure",
                "section": "experience",
                "severity": "high",
                "issue": "Insufficient use of bullet points",
                "suggestion": "Format experiences and achievements as bullet points for better readability",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check section balance
        experience_length = len(parsed_data.get("experience", ""))
        projects_length = len(parsed_data.get("projects", ""))
        
        if experience_length == 0 and projects_length == 0:
            score -= 25
            suggestions.append({
                "category": "structure",
                "section": "experience",
                "severity": "critical",
                "issue": "No experience or projects section",
                "suggestion": "Add internships, academic projects, or personal projects to showcase your skills",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        return max(0, score), suggestions
    
    @staticmethod
    def analyze_fresher_specific(parsed_data: Dict, metrics: Dict) -> Tuple[float, List[Dict]]:
        """
        Analyze fresher-specific aspects.
        
        Returns:
            Tuple of (score, suggestions_list)
        """
        score = 100.0
        suggestions = []
        
        # Check for education prominence
        education_text = parsed_data.get("education", "")
        if not education_text or len(education_text) < 50:
            score -= 25
            suggestions.append({
                "category": "fresher_specific",
                "section": "education",
                "severity": "critical",
                "issue": "Education section is weak or missing",
                "suggestion": "Expand education section with degree, institution, GPA (if good), and relevant coursework",
                "original_text": education_text,
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check for projects
        projects_text = parsed_data.get("projects", "")
        if not projects_text or len(projects_text) < 100:
            score -= 20
            suggestions.append({
                "category": "fresher_specific",
                "section": "projects",
                "severity": "high",
                "issue": "Limited or no project descriptions",
                "suggestion": "Add 2-3 significant projects with technologies used and outcomes achieved",
                "original_text": projects_text,
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check for certifications/achievements
        achievements_text = parsed_data.get("achievements", "")
        if not achievements_text:
            score -= 15
            suggestions.append({
                "category": "fresher_specific",
                "section": "achievements",
                "severity": "medium",
                "issue": "No certifications or achievements listed",
                "suggestion": "Add relevant certifications, awards, or academic achievements",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        # Check for LinkedIn
        if not metrics["has_linkedin"]:
            score -= 10
            suggestions.append({
                "category": "fresher_specific",
                "section": "contact",
                "severity": "low",
                "issue": "No LinkedIn profile",
                "suggestion": "Add your LinkedIn profile URL to increase professional credibility",
                "original_text": "",
                "enhanced_text": "",
                "accepted": False
            })
        
        return max(0, score), suggestions
    
    @staticmethod
    def calculate_overall_score(category_scores: Dict[str, float]) -> float:
        """
        Calculate weighted overall score.
        
        Args:
            category_scores: Dictionary of category scores
            
        Returns:
            Overall weighted score (0-100)
        """
        overall = 0.0
        for category, weight in ResumeAnalyzerService.SCORE_WEIGHTS.items():
            overall += category_scores.get(category, 0) * weight
        
        return round(overall, 2)
    
    @staticmethod
    async def generate_ai_enhancements(
        suggestions: List[Dict],
        parsed_data: Dict,
        user_tier: str
    ) -> List[Dict]:
        """
        Use AI to generate enhanced text for suggestions.
        Only generates for accepted suggestions or tier-appropriate suggestions.
        
        Args:
            suggestions: List of suggestions
            parsed_data: Parsed resume data
            user_tier: User's subscription tier
            
        Returns:
            Updated suggestions with AI-generated enhancements
        """
        # Determine how many AI suggestions based on tier
        tier_limits = {
            "FREE": 2,      # Only 2 AI-enhanced suggestions
            "PRO": 10,      # Up to 10
            "ULTIMATE": 999  # Unlimited
        }
        
        max_ai_suggestions = tier_limits.get(user_tier, 2)
        ai_count = 0
        
        enhanced_suggestions = []
        
        for suggestion in suggestions:
            # Skip if we've reached tier limit
            if ai_count >= max_ai_suggestions:
                enhanced_suggestions.append(suggestion)
                continue
            
            section = suggestion["section"]
            original_text = suggestion["original_text"]
            
            # Only generate AI enhancement if there's original text
            if original_text and len(original_text) > 10:
                try:
                    # Use AI to enhance the text
                    prompt = f"""{SYSTEM_PROMPT}

Task: Improve this resume section for a fresher.
Section: {section.capitalize()}
Issue: {suggestion['issue']}
Original text: {original_text}

Provide ONLY the improved text, nothing else."""
                    
                    enhanced_text = AIService._call_openrouter(prompt)
                    suggestion["enhanced_text"] = sanitize_input(enhanced_text, max_length=500)
                    ai_count += 1
                    
                except Exception as e:
                    # If AI fails, keep empty enhanced_text
                    suggestion["enhanced_text"] = ""
            
            enhanced_suggestions.append(suggestion)
        
        return enhanced_suggestions
    
    @staticmethod
    async def analyze_resume(
        parsed_data: Dict,
        metrics: Dict,
        user_tier: str = "FREE"
    ) -> Dict:
        """
        Perform complete resume analysis.
        
        Args:
            parsed_data: Parsed resume structure
            metrics: Extracted metrics
            user_tier: User's subscription tier
            
        Returns:
            Complete analysis results
        """
        # Analyze each category
        content_score, content_suggestions = ResumeAnalyzerService.analyze_content_quality(
            parsed_data, metrics
        )
        
        ats_score, ats_suggestions = ResumeAnalyzerService.analyze_ats_optimization(
            parsed_data, metrics
        )
        
        structure_score, structure_suggestions = ResumeAnalyzerService.analyze_structure(
            parsed_data, metrics
        )
        
        fresher_score, fresher_suggestions = ResumeAnalyzerService.analyze_fresher_specific(
            parsed_data, metrics
        )
        
        # Calculate overall score
        category_scores = {
            "content_quality": content_score,
            "ats_optimization": ats_score,
            "structure": structure_score,
            "fresher_specific": fresher_score
        }
        
        overall_score = ResumeAnalyzerService.calculate_overall_score(category_scores)
        
        # Combine all suggestions
        all_suggestions = (
            content_suggestions +
            ats_suggestions +
            structure_suggestions +
            fresher_suggestions
        )
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_suggestions.sort(key=lambda x: severity_order.get(x["severity"], 4))
        
        # Generate AI enhancements for top suggestions
        enhanced_suggestions = await ResumeAnalyzerService.generate_ai_enhancements(
            all_suggestions,
            parsed_data,
            user_tier
        )
        
        return {
            "overall_score": overall_score,
            "category_scores": category_scores,
            "suggestions": enhanced_suggestions,
            "total_suggestions": len(enhanced_suggestions),
            "critical_issues": len([s for s in enhanced_suggestions if s["severity"] == "critical"]),
            "metrics": metrics
        }
