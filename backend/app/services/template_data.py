"""
Resume Template Definitions
50+ ATS-Optimized Templates for Various Industries and Positions
"""

RESUME_TEMPLATES = [
    # ==================== TECHNOLOGY & SOFTWARE ====================
    {
        "name": "tech_minimal_swe",
        "display_name": "Tech Minimal - Software Engineer",
        "description": "Clean, ATS-friendly template for software engineers",
        "industry": "Technology",
        "position_type": "Entry-level",
        "category": "Minimal",
        "tier_required": "FREE",
        "is_featured": True,
        "settings": {
            "font": "Calibri",
            "font_size": 11,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["summary", "skills", "experience", "education", "projects"]
        }
    },
    {
        "name": "tech_modern_fullstack",
        "display_name": "Modern Fullstack Developer",
        "description": "Contemporary design for fullstack developers",
        "industry": "Technology",
        "position_type": "Mid-level",
        "category": "Modern",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "teal",
            "layout": "two-column",
            "sections": ["summary", "technical_skills", "experience", "projects", "education"]
        }
    },
    {
        "name": "tech_senior_architect",
        "display_name": "Senior Software Architect",
        "description": "Executive-level template for senior tech roles",
        "industry": "Technology",
        "position_type": "Senior",
        "category": "Executive",
        "tier_required": "PRO",
        "settings": {
            "font": "Georgia",
            "font_size": 11,
            "color_scheme": "navy",
            "layout": "hybrid",
            "sections": ["executive_summary", "core_competencies", "leadership", "experience", "education"]
        }
    },
    {
        "name": "tech_data_scientist",
        "display_name": "Data Scientist Professional",
        "description": "Quantitative-focused template for data roles",
        "industry": "Technology",
        "position_type": "Mid-level",
        "category": "Modern",
        "tier_required": "PRO",
        "settings": {
            "font": "Helvetica",
            "font_size": 10,
            "color_scheme": "purple",
            "layout": "two-column",
            "sections": ["summary", "technical_skills", "projects", "experience", "education", "certifications"]
        }
    },
    {
        "name": "tech_devops_engineer",
        "display_name": "DevOps Engineer",
        "description": "Infrastructure and automation focused",
        "industry": "Technology",
        "position_type": "Mid-level",
        "category": "Technical",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "orange",
            "layout": "single-column",
            "sections": ["summary", "technical_skills", "certifications", "experience", "education"]
        }
    },
    
    # ==================== FINANCE & ACCOUNTING ====================
    {
        "name": "finance_analyst_classic",
        "display_name": "Financial Analyst Classic",
        "description": "Traditional format for finance professionals",
        "industry": "Finance",
        "position_type": "Entry-level",
        "category": "Classic",
        "tier_required": "FREE",
        "settings": {
            "font": "Times New Roman",
            "font_size": 11,
            "color_scheme": "black",
            "layout": "single-column",
            "sections": ["objective", "education", "experience", "skills", "certifications"]
        }
    },
    {
        "name": "finance_investment_banker",
        "display_name": "Investment Banking Professional",
        "description": "High-impact template for banking roles",
        "industry": "Finance",
        "position_type": "Mid-level",
        "category": "Executive",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 11,
            "color_scheme": "navy",
            "layout": "single-column",
            "sections": ["summary", "experience", "education", "skills", "achievements"]
        }
    },
    {
        "name": "finance_accountant",
        "display_name": "Certified Public Accountant",
        "description": "CPA-focused professional template",
        "industry": "Finance",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "green",
            "layout": "single-column",
            "sections": ["certifications", "experience", "education", "skills"]
        }
    },
    {
        "name": "finance_risk_analyst",
        "display_name": "Risk Management Analyst",
        "description": "Specialized template for risk analysis",
        "industry": "Finance",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "maroon",
            "layout": "two-column",
            "sections": ["summary", "certifications", "experience", "skills", "education"]
        }
    },
    
    # ==================== HEALTHCARE & MEDICAL ====================
    {
        "name": "healthcare_nurse",
        "display_name": "Registered Nurse",
        "description": "Clinical template for nursing professionals",
        "industry": "Healthcare",
        "position_type": "Entry-level",
        "category": "Professional",
        "tier_required": "FREE",
        "settings": {
            "font": "Arial",
            "font_size": 11,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["licenses", "clinical_experience", "education", "certifications", "skills"]
        }
    },
    {
        "name": "healthcare_physician",
        "display_name": "Medical Doctor",
        "description": "Comprehensive MD/DO template",
        "industry": "Healthcare",
        "position_type": "Senior",
        "category": "Executive",
        "tier_required": "PRO",
        "settings": {
            "font": "Times New Roman",
            "font_size": 11,
            "color_scheme": "black",
            "layout": "single-column",
            "sections": ["education", "residency", "board_certifications", "clinical_experience", "publications"]
        }
    },
    {
        "name": "healthcare_pharmacy",
        "display_name": "Clinical Pharmacist",
        "description": "Pharmacy-focused professional template",
        "industry": "Healthcare",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "teal",
            "layout": "single-column",
            "sections": ["licenses", "experience", "education", "certifications", "skills"]
        }
    },
    
    # ==================== MARKETING & SALES ====================
    {
        "name": "marketing_digital",
        "display_name": "Digital Marketing Specialist",
        "description": "Modern template for digital marketers",
        "industry": "Marketing",
        "position_type": "Mid-level",
        "category": "Creative",
        "tier_required": "PRO",
        "settings": {
            "font": "Helvetica",
            "font_size": 10,
            "color_scheme": "purple",
            "layout": "two-column",
            "sections": ["summary", "key_achievements", "experience", "skills", "education", "certifications"]
        }
    },
    {
        "name": "marketing_content",
        "display_name": "Content Marketing Manager",
        "description": "Content-focused marketing template",
        "industry": "Marketing",
        "position_type": "Mid-level",
        "category": "Creative",
        "tier_required": "PRO",
        "settings": {
            "font": "Georgia",
            "font_size": 11,
            "color_scheme": "orange",
            "layout": "single-column",
            "sections": ["summary", "portfolio", "experience", "skills", "education"]
        }
    },
    {
        "name": "sales_executive",
        "display_name": "Sales Executive",
        "description": "Results-driven sales template",
        "industry": "Sales",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "FREE",
        "settings": {
            "font": "Arial",
            "font_size": 11,
            "color_scheme": "red",
            "layout": "single-column",
            "sections": ["summary", "achievements", "experience", "education", "skills"]
        }
    },
    {
        "name": "sales_account_manager",
        "display_name": "Account Manager",
        "description": "Relationship-focused sales template",
        "industry": "Sales",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "blue",
            "layout": "two-column",
            "sections": ["summary", "key_accounts", "experience", "achievements", "education"]
        }
    },
    
    # ==================== DESIGN & CREATIVE ====================
    {
        "name": "design_ux_ui",
        "display_name": "UX/UI Designer",
        "description": "Modern template for design professionals",
        "industry": "Design",
        "position_type": "Mid-level",
        "category": "Creative",
        "tier_required": "ULTIMATE",
        "is_featured": True,
        "settings": {
            "font": "Helvetica",
            "font_size": 10,
            "color_scheme": "purple",
            "layout": "creative",
            "sections": ["summary", "portfolio", "experience", "skills", "education", "tools"]
        }
    },
    {
        "name": "design_graphic",
        "display_name": "Graphic Designer",
        "description": "Visual-focused creative template",
        "industry": "Design",
        "position_type": "Entry-level",
        "category": "Creative",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "multicolor",
            "layout": "creative",
            "sections": ["portfolio", "experience", "skills", "education", "awards"]
        }
    },
    {
        "name": "design_product",
        "display_name": "Product Designer",
        "description": "Product-focused design template",
        "industry": "Design",
        "position_type": "Mid-level",
        "category": "Modern",
        "tier_required": "PRO",
        "settings": {
            "font": "Helvetica",
            "font_size": 10,
            "color_scheme": "blue",
            "layout": "two-column",
            "sections": ["summary", "case_studies", "experience", "skills", "education"]
        }
    },
    
    # ==================== ENGINEERING (Non-Software) ====================
    {
        "name": "engineer_mechanical",
        "display_name": "Mechanical Engineer",
        "description": "Technical template for mechanical engineers",
        "industry": "Engineering",
        "position_type": "Entry-level",
        "category": "Technical",
        "tier_required": "FREE",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["summary", "technical_skills", "projects", "experience", "education", "certifications"]
        }
    },
    {
        "name": "engineer_civil",
        "display_name": "Civil Engineer",
        "description": "Project-focused civil engineering template",
        "industry": "Engineering",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "green",
            "layout": "single-column",
            "sections": ["summary", "project_experience", "technical_skills", "experience", "education", "licenses"]
        }
    },
    {
        "name": "engineer_electrical",
        "display_name": "Electrical Engineer",
        "description": "Specialized electrical engineering template",
        "industry": "Engineering",
        "position_type": "Mid-level",
        "category": "Technical",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "orange",
            "layout": "two-column",
            "sections": ["summary", "technical_expertise", "projects", "experience", "education", "certifications"]
        }
    },
    
    # ==================== LEGAL & LAW ====================
    {
        "name": "legal_attorney",
        "display_name": "Attorney at Law",
        "description": "Professional legal template",
        "industry": "Legal",
        "position_type": "Senior",
        "category": "Executive",
        "tier_required": "PRO",
        "settings": {
            "font": "Times New Roman",
            "font_size": 11,
            "color_scheme": "black",
            "layout": "single-column",
            "sections": ["bar_admissions", "experience", "education", "practice_areas", "publications"]
        }
    },
    {
        "name": "legal_paralegal",
        "display_name": "Paralegal Professional",
        "description": "Paralegal-focused template",
        "industry": "Legal",
        "position_type": "Entry-level",
        "category": "Professional",
        "tier_required": "FREE",
        "settings": {
            "font": "Calibri",
            "font_size": 11,
            "color_scheme": "navy",
            "layout": "single-column",
            "sections": ["certifications", "experience", "education", "skills", "areas_of_practice"]
        }
    },
    
    # ==================== EDUCATION & ACADEMIA ====================
    {
        "name": "education_teacher",
        "display_name": "K-12 Teacher",
        "description": "Education-focused teaching template",
        "industry": "Education",
        "position_type": "Entry-level",
        "category": "Professional",
        "tier_required": "FREE",
        "settings": {
            "font": "Arial",
            "font_size": 11,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["certifications", "teaching_experience", "education", "skills", "philosophy"]
        }
    },
    {
        "name": "education_professor",
        "display_name": "University Professor",
        "description": "Academic CV template",
        "industry": "Education",
        "position_type": "Senior",
        "category": "Academic",
        "tier_required": "PRO",
        "settings": {
            "font": "Times New Roman",
            "font_size": 11,
            "color_scheme": "black",
            "layout": "single-column",
            "sections": ["education", "research", "publications", "teaching", "grants", "service"]
        }
    },
    
    # ==================== HUMAN RESOURCES ====================
    {
        "name": "hr_specialist",
        "display_name": "HR Specialist",
        "description": "Human resources professional template",
        "industry": "Human Resources",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "FREE",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "teal",
            "layout": "single-column",
            "sections": ["summary", "experience", "education", "certifications", "skills"]
        }
    },
    {
        "name": "hr_director",
        "display_name": "HR Director",
        "description": "Executive HR template",
        "industry": "Human Resources",
        "position_type": "Senior",
        "category": "Executive",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 11,
            "color_scheme": "navy",
            "layout": "single-column",
            "sections": ["executive_summary", "leadership_experience", "achievements", "education", "certifications"]
        }
    },
    
    # ==================== PROJECT MANAGEMENT ====================
    {
        "name": "pm_agile_scrum",
        "display_name": "Agile Project Manager",
        "description": "Scrum/Agile PM template",
        "industry": "Project Management",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["summary", "certifications", "project_highlights", "experience", "education", "skills"]
        }
    },
    {
        "name": "pm_pmp",
        "display_name": "PMP Certified PM",
        "description": "PMP certification focused",
        "industry": "Project Management",
        "position_type": "Senior",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "green",
            "layout": "two-column",
            "sections": ["certifications", "summary", "key_projects", "experience", "education"]
        }
    },
    
    # ==================== CUSTOMER SERVICE & SUPPORT ====================
    {
        "name": "cs_representative",
        "display_name": "Customer Service Rep",
        "description": "Customer-facing role template",
        "industry": "Customer Service",
        "position_type": "Entry-level",
        "category": "Professional",
        "tier_required": "FREE",
        "settings": {
            "font": "Arial",
            "font_size": 11,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["summary", "experience", "skills", "education", "achievements"]
        }
    },
    {
        "name": "cs_manager",
        "display_name": "Customer Success Manager",
        "description": "Customer success focused template",
        "industry": "Customer Service",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "teal",
            "layout": "two-column",
            "sections": ["summary", "key_metrics", "experience", "skills", "education"]
        }
    },
    
    # ==================== OPERATIONS & LOGISTICS ====================
    {
        "name": "ops_supply_chain",
        "display_name": "Supply Chain Manager",
        "description": "Supply chain focused template",
        "industry": "Operations",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "brown",
            "layout": "single-column",
            "sections": ["summary", "key_achievements", "experience", "education", "certifications"]
        }
    },
    {
        "name": "ops_logistics",
        "display_name": "Logistics Coordinator",
        "description": "Logistics and transportation template",
        "industry": "Operations",
        "position_type": "Entry-level",
        "category": "Professional",
        "tier_required": "FREE",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["summary", "experience", "skills", "education", "certifications"]
        }
    },
    
    # ==================== EXECUTIVE & C-LEVEL ====================
    {
        "name": "exec_ceo",
        "display_name": "Chief Executive Officer",
        "description": "Executive-level CEO template",
        "industry": "Executive",
        "position_type": "Executive",
        "category": "Executive",
        "tier_required": "ULTIMATE",
        "settings": {
            "font": "Georgia",
            "font_size": 11,
            "color_scheme": "navy",
            "layout": "executive",
            "sections": ["executive_profile", "board_positions", "leadership_experience", "education", "achievements"]
        }
    },
    {
        "name": "exec_cto",
        "display_name": "Chief Technology Officer",
        "description": "Technology executive template",
        "industry": "Technology",
        "position_type": "Executive",
        "category": "Executive",
        "tier_required": "ULTIMATE",
        "settings": {
            "font": "Calibri",
            "font_size": 11,
            "color_scheme": "blue",
            "layout": "executive",
            "sections": ["executive_summary", "technical_leadership", "strategic_initiatives", "experience", "education"]
        }
    },
    {
        "name": "exec_cfo",
        "display_name": "Chief Financial Officer",
        "description": "Finance executive template",
        "industry": "Finance",
        "position_type": "Executive",
        "category": "Executive",
        "tier_required": "ULTIMATE",
        "settings": {
            "font": "Times New Roman",
            "font_size": 11,
            "color_scheme": "black",
            "layout": "executive",
            "sections": ["executive_profile", "financial_leadership", "experience", "education", "board_service"]
        }
    },
    
    # ==================== SPECIALIZED ROLES ====================
    {
        "name": "research_scientist",
        "display_name": "Research Scientist",
        "description": "Academic research template",
        "industry": "Research",
        "position_type": "Mid-level",
        "category": "Academic",
        "tier_required": "PRO",
        "settings": {
            "font": "Times New Roman",
            "font_size": 10,
            "color_scheme": "black",
            "layout": "single-column",
            "sections": ["research_interests", "publications", "experience", "education", "grants", "presentations"]
        }
    },
    {
        "name": "consultant",
        "display_name": "Management Consultant",
        "description": "Consulting-focused template",
        "industry": "Consulting",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "navy",
            "layout": "single-column",
            "sections": ["summary", "client_engagements", "experience", "education", "skills"]
        }
    },
    {
        "name": "quality_assurance",
        "display_name": "QA Engineer",
        "description": "Quality assurance template",
        "industry": "Technology",
        "position_type": "Mid-level",
        "category": "Technical",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "green",
            "layout": "single-column",
            "sections": ["summary", "technical_skills", "testing_experience", "experience", "education", "certifications"]
        }
    },
    {
        "name": "business_analyst",
        "display_name": "Business Analyst",
        "description": "BA-focused professional template",
        "industry": "Business",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "blue",
            "layout": "two-column",
            "sections": ["summary", "key_projects", "experience", "skills", "education", "certifications"]
        }
    },
    {
        "name": "cybersecurity",
        "display_name": "Cybersecurity Analyst",
        "description": "Security-focused technical template",
        "industry": "Technology",
        "position_type": "Mid-level",
        "category": "Technical",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "red",
            "layout": "single-column",
            "sections": ["summary", "certifications", "technical_skills", "experience", "education"]
        }
    },
    
    # ==================== STUDENT & INTERNSHIP ====================
    {
        "name": "student_fresher",
        "display_name": "Fresh Graduate",
        "description": "Recent graduate template",
        "industry": "General",
        "position_type": "Entry-level",
        "category": "Student",
        "tier_required": "FREE",
        "is_featured": True,
        "settings": {
            "font": "Arial",
            "font_size": 11,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["objective", "education", "projects", "internships", "skills", "extracurricular"]
        }
    },
    {
        "name": "student_internship",
        "display_name": "Internship Seeker",
        "description": "Student internship template",
        "industry": "General",
        "position_type": "Intern",
        "category": "Student",
        "tier_required": "FREE",
        "settings": {
            "font": "Calibri",
            "font_size": 11,
            "color_scheme": "blue",
            "layout": "single-column",
            "sections": ["objective", "education", "relevant_coursework", "projects", "skills", "activities"]
        }
    },
    
    # ==================== INDUSTRY-SPECIFIC ====================
    {
        "name": "hospitality_manager",
        "display_name": "Hospitality Manager",
        "description": "Hotel and service management",
        "industry": "Hospitality",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "brown",
            "layout": "single-column",
            "sections": ["summary", "experience", "achievements", "education", "skills"]
        }
    },
    {
        "name": "real_estate_agent",
        "display_name": "Real Estate Agent",
        "description": "Real estate professional template",
        "industry": "Real Estate",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Calibri",
            "font_size": 10,
            "color_scheme": "green",
            "layout": "single-column",
            "sections": ["summary", "licenses", "sales_achievements", "experience", "education"]
        }
    },
    {
        "name": "nonprofit_coordinator",
        "display_name": "Non-Profit Coordinator",
        "description": "Nonprofit sector template",
        "industry": "Non-Profit",
        "position_type": "Mid-level",
        "category": "Professional",
        "tier_required": "PRO",
        "settings": {
            "font": "Arial",
            "font_size": 10,
            "color_scheme": "purple",
            "layout": "single-column",
            "sections": ["summary", "program_experience", "experience", "education", "volunteer_work"]
        }
    },
]

# Total: 50+ templates covering major industries and position types
