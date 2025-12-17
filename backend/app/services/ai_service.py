"""
AI Service - Hugging Face Integration
LOCKED SYSTEM PROMPT - AI ONLY PERFORMS SPECIFIC RESUME TASKS
"""
import requests
from typing import Optional
from app.core.config import settings
from app.core.security import sanitize_input
from fastapi import HTTPException


# MASTER SYSTEM PROMPT - LOCKED AND UNCHANGEABLE
SYSTEM_PROMPT = """You are an AI Resume Coach specialized in helping STUDENTS and FRESHERS.
Convert raw, informal input into professional, ATS-friendly resume content.
Do not invent experience, metrics, or achievements.
Keep output concise, factual, and suitable for a one-page resume.
Return ONLY resume-ready text."""


class AIService:
    """Hugging Face AI integration service."""
    
    @staticmethod
    def _call_openrouter(prompt: str) -> str:
        """
        Internal method to call OpenRouter API.
        OpenRouter uses OpenAI-compatible API format.
        SECURITY: This method is NOT exposed to users.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-resume-coach.com",
            "X-Title": "AI Resume Coach"
        }
        
        payload = {
            "model": settings.AI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": settings.AI_MAX_TOKENS,
            "temperature": settings.AI_TEMPERATURE,
            "top_p": settings.AI_TOP_P
        }
        
        try:
            logger.info(f"Calling OpenRouter API with model: {settings.AI_MODEL}")
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            # Log response status
            logger.info(f"OpenRouter response status: {response.status_code}")
            
            # Check for various error codes
            if response.status_code == 401:
                logger.error("OpenRouter API key is invalid or expired")
                raise HTTPException(
                    status_code=503, 
                    detail="AI service authentication failed. Please contact support."
                )
            
            if response.status_code == 402:
                logger.error("OpenRouter account has insufficient credits")
                raise HTTPException(
                    status_code=503,
                    detail="AI service temporarily unavailable. Please try again later."
                )
            
            if response.status_code == 429:
                logger.error("OpenRouter rate limit exceeded")
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please wait a moment and try again."
                )
            
            if response.status_code >= 500:
                logger.error(f"OpenRouter server error: {response.status_code}")
                error_detail = "AI service is temporarily unavailable. Please try again in a few moments."
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        logger.error(f"OpenRouter error details: {error_data['error']}")
                except:
                    pass
                raise HTTPException(status_code=503, detail=error_detail)
            
            # Raise for other error status codes
            response.raise_for_status()
            
            result = response.json()
            logger.info("Successfully received response from OpenRouter")
            
            # Extract message from OpenAI-compatible response
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"].strip()
                if content:
                    return content
                else:
                    logger.error("OpenRouter returned empty content")
                    raise HTTPException(
                        status_code=500, 
                        detail="AI service returned empty response. Please try again."
                    )
            
            logger.error(f"Unexpected OpenRouter response format: {result}")
            raise HTTPException(
                status_code=500, 
                detail="Unexpected AI response format. Please try again."
            )
        
        except requests.exceptions.Timeout:
            logger.error("OpenRouter request timed out")
            raise HTTPException(
                status_code=504, 
                detail="AI service timeout. The request took too long. Please try again."
            )
        
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to OpenRouter")
            raise HTTPException(
                status_code=503,
                detail="Unable to connect to AI service. Please check your internet connection."
            )
        
        except HTTPException:
            # Re-raise HTTPExceptions as-is
            raise
        
        except Exception as e:
            logger.error(f"Unexpected error calling OpenRouter: {str(e)}")
            raise HTTPException(
                status_code=503, 
                detail=f"AI service error: {str(e)}"
            )
    
    @staticmethod
    def rewrite_bullet_point(raw_text: str, tone: str = "professional") -> str:
        """
        Rewrite a resume bullet point.
        Allowed for: ALL tiers (with usage limits)
        """
        # Sanitize input
        clean_text = sanitize_input(raw_text, max_length=300)
        
        if not clean_text:
            raise HTTPException(status_code=400, detail="Input text is required")
        
        # Build prompt
        prompt = f"""{SYSTEM_PROMPT}

Task: Rewrite this bullet point in a {tone} tone for a fresher's resume.
Input: {clean_text}
Output:"""
        
        return AIService._call_openrouter(prompt)
    
    @staticmethod
    def generate_project_description(project_name: str, tech_stack: str, key_points: str) -> str:
        """
        Generate project description.
        Allowed for: PRO and ULTIMATE tiers
        """
        # Sanitize inputs
        project_name = sanitize_input(project_name, max_length=100)
        tech_stack = sanitize_input(tech_stack, max_length=200)
        key_points = sanitize_input(key_points, max_length=300)
        
        if not all([project_name, tech_stack, key_points]):
            raise HTTPException(status_code=400, detail="All fields are required")
        
        prompt = f"""{SYSTEM_PROMPT}

Task: Write a concise project description for a fresher's resume.
Project: {project_name}
Tech Stack: {tech_stack}
Key Points: {key_points}
Output:"""
        
        return AIService._call_openrouter(prompt)
    
    @staticmethod
    def generate_resume_summary(skills: str, experience: str, goal: str) -> str:
        """
        Generate resume summary/objective.
        Allowed for: PRO and ULTIMATE tiers
        """
        # Sanitize inputs
        skills = sanitize_input(skills, max_length=200)
        experience = sanitize_input(experience, max_length=200)
        goal = sanitize_input(goal, max_length=200)
        
        if not all([skills, goal]):
            raise HTTPException(status_code=400, detail="Skills and goal are required")
        
        prompt = f"""{SYSTEM_PROMPT}

Task: Write a professional resume summary for a fresher.
Skills: {skills}
Experience: {experience if experience else 'None'}
Career Goal: {goal}
Output:"""
        
        return AIService._call_openrouter(prompt)
    
    @staticmethod
    def apply_tone_variation(text: str, tone: str) -> str:
        """
        Apply advanced tone variation.
        Allowed for: ULTIMATE tier only
        Tones: confident, concise, impactful
        """
        # Sanitize input
        clean_text = sanitize_input(text, max_length=500)
        
        if tone not in ["confident", "concise", "impactful"]:
            tone = "professional"
        
        prompt = f"""{SYSTEM_PROMPT}

Task: Rewrite this text with a {tone} tone.
Input: {clean_text}
Output:"""
        
        return AIService._call_openrouter(prompt)
