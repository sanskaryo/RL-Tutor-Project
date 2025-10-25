"""
Seed database with skills and badges for Phase 13.
Run this after database initialization to populate skill tree and badges.
"""

from sqlalchemy.orm import Session
from app.core.database import get_db, init_db
from app.models import mastery


def seed_skills(db: Session):
    """Create skill tree with 50+ skills across mathematics topics"""
    
    print("Seeding skills...")
    
    # Check if skills already exist
    existing = db.query(mastery.MasterySkill).first()
    if existing:
        print("Skills already seeded. Skipping...")
        return
    
    skills_data = [
        # ========== FUNDAMENTALS (No prerequisites) ==========
        {"name": "Basic Arithmetic", "category": "Fundamentals", "difficulty": "beginner", "hours": 2},
        {"name": "Fractions", "category": "Fundamentals", "difficulty": "beginner", "hours": 3},
        {"name": "Decimals", "category": "Fundamentals", "difficulty": "beginner", "hours": 2},
        {"name": "Percentages", "category": "Fundamentals", "difficulty": "beginner", "hours": 2},
        {"name": "Order of Operations", "category": "Fundamentals", "difficulty": "beginner", "hours": 1},
        
        # ========== ALGEBRA ==========
        {"name": "Variables and Expressions", "category": "Algebra", "difficulty": "beginner", "hours": 3, "prereqs": ["Basic Arithmetic"]},
        {"name": "Linear Equations", "category": "Algebra", "difficulty": "intermediate", "hours": 4, "prereqs": ["Variables and Expressions"]},
        {"name": "Systems of Equations", "category": "Algebra", "difficulty": "intermediate", "hours": 5, "prereqs": ["Linear Equations"]},
        {"name": "Quadratic Equations", "category": "Algebra", "difficulty": "intermediate", "hours": 6, "prereqs": ["Linear Equations"]},
        {"name": "Polynomials", "category": "Algebra", "difficulty": "intermediate", "hours": 5, "prereqs": ["Quadratic Equations"]},
        {"name": "Factoring", "category": "Algebra", "difficulty": "intermediate", "hours": 4, "prereqs": ["Polynomials"]},
        {"name": "Rational Expressions", "category": "Algebra", "difficulty": "advanced", "hours": 6, "prereqs": ["Factoring"]},
        {"name": "Exponents and Radicals", "category": "Algebra", "difficulty": "intermediate", "hours": 4, "prereqs": ["Polynomials"]},
        {"name": "Logarithms", "category": "Algebra", "difficulty": "advanced", "hours": 5, "prereqs": ["Exponents and Radicals"]},
        {"name": "Sequences and Series", "category": "Algebra", "difficulty": "advanced", "hours": 5, "prereqs": ["Polynomials"]},
        
        # ========== GEOMETRY ==========
        {"name": "Points, Lines, and Angles", "category": "Geometry", "difficulty": "beginner", "hours": 3, "prereqs": ["Basic Arithmetic"]},
        {"name": "Triangles", "category": "Geometry", "difficulty": "beginner", "hours": 4, "prereqs": ["Points, Lines, and Angles"]},
        {"name": "Pythagorean Theorem", "category": "Geometry", "difficulty": "intermediate", "hours": 3, "prereqs": ["Triangles"]},
        {"name": "Quadrilaterals", "category": "Geometry", "difficulty": "intermediate", "hours": 3, "prereqs": ["Triangles"]},
        {"name": "Circles", "category": "Geometry", "difficulty": "intermediate", "hours": 4, "prereqs": ["Points, Lines, and Angles"]},
        {"name": "Area and Perimeter", "category": "Geometry", "difficulty": "intermediate", "hours": 3, "prereqs": ["Quadrilaterals", "Circles"]},
        {"name": "Volume and Surface Area", "category": "Geometry", "difficulty": "intermediate", "hours": 4, "prereqs": ["Area and Perimeter"]},
        {"name": "Coordinate Geometry", "category": "Geometry", "difficulty": "intermediate", "hours": 5, "prereqs": ["Linear Equations", "Points, Lines, and Angles"]},
        {"name": "Transformations", "category": "Geometry", "difficulty": "advanced", "hours": 4, "prereqs": ["Coordinate Geometry"]},
        {"name": "Trigonometry Basics", "category": "Geometry", "difficulty": "advanced", "hours": 6, "prereqs": ["Pythagorean Theorem"]},
        
        # ========== TRIGONOMETRY ==========
        {"name": "Sine, Cosine, Tangent", "category": "Trigonometry", "difficulty": "advanced", "hours": 5, "prereqs": ["Trigonometry Basics"]},
        {"name": "Unit Circle", "category": "Trigonometry", "difficulty": "advanced", "hours": 4, "prereqs": ["Sine, Cosine, Tangent"]},
        {"name": "Trigonometric Identities", "category": "Trigonometry", "difficulty": "advanced", "hours": 6, "prereqs": ["Unit Circle"]},
        {"name": "Inverse Trig Functions", "category": "Trigonometry", "difficulty": "advanced", "hours": 4, "prereqs": ["Trigonometric Identities"]},
        {"name": "Law of Sines and Cosines", "category": "Trigonometry", "difficulty": "expert", "hours": 5, "prereqs": ["Trigonometric Identities"]},
        
        # ========== PRE-CALCULUS ==========
        {"name": "Functions", "category": "Pre-Calculus", "difficulty": "intermediate", "hours": 5, "prereqs": ["Linear Equations"]},
        {"name": "Function Transformations", "category": "Pre-Calculus", "difficulty": "advanced", "hours": 4, "prereqs": ["Functions"]},
        {"name": "Composite Functions", "category": "Pre-Calculus", "difficulty": "advanced", "hours": 4, "prereqs": ["Functions"]},
        {"name": "Inverse Functions", "category": "Pre-Calculus", "difficulty": "advanced", "hours": 4, "prereqs": ["Composite Functions"]},
        {"name": "Exponential Functions", "category": "Pre-Calculus", "difficulty": "advanced", "hours": 5, "prereqs": ["Exponents and Radicals", "Functions"]},
        {"name": "Logarithmic Functions", "category": "Pre-Calculus", "difficulty": "advanced", "hours": 5, "prereqs": ["Logarithms", "Functions"]},
        {"name": "Polynomial Functions", "category": "Pre-Calculus", "difficulty": "advanced", "hours": 6, "prereqs": ["Polynomials", "Functions"]},
        {"name": "Rational Functions", "category": "Pre-Calculus", "difficulty": "advanced", "hours": 5, "prereqs": ["Rational Expressions", "Functions"]},
        {"name": "Limits", "category": "Pre-Calculus", "difficulty": "expert", "hours": 6, "prereqs": ["Functions"]},
        
        # ========== CALCULUS ==========
        {"name": "Derivatives", "category": "Calculus", "difficulty": "expert", "hours": 8, "prereqs": ["Limits"]},
        {"name": "Chain Rule", "category": "Calculus", "difficulty": "expert", "hours": 5, "prereqs": ["Derivatives"]},
        {"name": "Product and Quotient Rules", "category": "Calculus", "difficulty": "expert", "hours": 5, "prereqs": ["Derivatives"]},
        {"name": "Implicit Differentiation", "category": "Calculus", "difficulty": "expert", "hours": 4, "prereqs": ["Chain Rule"]},
        {"name": "Applications of Derivatives", "category": "Calculus", "difficulty": "expert", "hours": 6, "prereqs": ["Derivatives"]},
        {"name": "Integrals", "category": "Calculus", "difficulty": "expert", "hours": 8, "prereqs": ["Derivatives"]},
        {"name": "Integration Techniques", "category": "Calculus", "difficulty": "expert", "hours": 10, "prereqs": ["Integrals"]},
        {"name": "Integration by Parts", "category": "Calculus", "difficulty": "expert", "hours": 5, "prereqs": ["Integration Techniques"]},
        {"name": "Definite Integrals", "category": "Calculus", "difficulty": "expert", "hours": 6, "prereqs": ["Integrals"]},
        {"name": "Applications of Integrals", "category": "Calculus", "difficulty": "expert", "hours": 7, "prereqs": ["Definite Integrals"]},
        
        # ========== STATISTICS ==========
        {"name": "Data and Graphs", "category": "Statistics", "difficulty": "beginner", "hours": 3, "prereqs": ["Basic Arithmetic"]},
        {"name": "Mean, Median, Mode", "category": "Statistics", "difficulty": "beginner", "hours": 2, "prereqs": ["Data and Graphs"]},
        {"name": "Probability Basics", "category": "Statistics", "difficulty": "intermediate", "hours": 4, "prereqs": ["Fractions", "Percentages"]},
        {"name": "Combinations and Permutations", "category": "Statistics", "difficulty": "intermediate", "hours": 4, "prereqs": ["Probability Basics"]},
        {"name": "Distributions", "category": "Statistics", "difficulty": "advanced", "hours": 6, "prereqs": ["Mean, Median, Mode", "Probability Basics"]},
        {"name": "Standard Deviation", "category": "Statistics", "difficulty": "advanced", "hours": 4, "prereqs": ["Distributions"]},
        {"name": "Hypothesis Testing", "category": "Statistics", "difficulty": "expert", "hours": 8, "prereqs": ["Distributions"]},
    ]
    
    # Create skills and store by name for prerequisite linking
    skills_by_name = {}
    
    for skill_data in skills_data:
        skill = mastery.MasterySkill(
            name=skill_data["name"],
            description=f"Learn and master {skill_data['name']}",
            category=skill_data["category"],
            difficulty=skill_data["difficulty"],
            estimated_hours=skill_data["hours"]
        )
        db.add(skill)
        skills_by_name[skill_data["name"]] = skill
    
    # Commit to get IDs
    db.commit()
    
    # Now add prerequisites
    for skill_data in skills_data:
        if "prereqs" in skill_data:
            skill = skills_by_name[skill_data["name"]]
            for prereq_name in skill_data["prereqs"]:
                if prereq_name in skills_by_name:
                    skill.prerequisites.append(skills_by_name[prereq_name])
    
    db.commit()
    
    print(f"✅ Created {len(skills_data)} skills")


def seed_badges(db: Session):
    """Create badges for various achievements"""
    
    print("Seeding badges...")
    
    # Check if badges already exist
    existing = db.query(mastery.Badge).first()
    if existing:
        print("Badges already seeded. Skipping...")
        return
    
    badges_data = [
        # ========== MASTERY BADGES ==========
        {
            "name": "First Steps",
            "description": "Complete your first skill",
            "category": "mastery",
            "tier": "bronze",
            "icon": "🎯",
            "color": "#CD7F32",
            "criteria": {"mastered_skills": 1},
            "points": 10
        },
        {
            "name": "Skill Collector",
            "description": "Master 5 skills",
            "category": "mastery",
            "tier": "silver",
            "icon": "📚",
            "color": "#C0C0C0",
            "criteria": {"mastered_skills": 5},
            "points": 50
        },
        {
            "name": "Knowledge Seeker",
            "description": "Master 10 skills",
            "category": "mastery",
            "tier": "gold",
            "icon": "🏆",
            "color": "#FFD700",
            "criteria": {"mastered_skills": 10},
            "points": 100
        },
        {
            "name": "Master Scholar",
            "description": "Master 25 skills",
            "category": "mastery",
            "tier": "platinum",
            "icon": "👑",
            "color": "#E5E4E2",
            "criteria": {"mastered_skills": 25},
            "points": 250
        },
        
        # ========== STREAK BADGES ==========
        {
            "name": "On Fire",
            "description": "Maintain a 3-day streak",
            "category": "streak",
            "tier": "bronze",
            "icon": "🔥",
            "color": "#FF6B35",
            "criteria": {"current_streak": 3},
            "points": 15
        },
        {
            "name": "Dedicated Learner",
            "description": "Maintain a 7-day streak",
            "category": "streak",
            "tier": "silver",
            "icon": "⚡",
            "color": "#FFD700",
            "criteria": {"current_streak": 7},
            "points": 35
        },
        {
            "name": "Unstoppable",
            "description": "Maintain a 30-day streak",
            "category": "streak",
            "tier": "gold",
            "icon": "💪",
            "color": "#FFD700",
            "criteria": {"current_streak": 30},
            "points": 150
        },
        {
            "name": "Legend",
            "description": "Maintain a 100-day streak",
            "category": "streak",
            "tier": "platinum",
            "icon": "🌟",
            "color": "#E5E4E2",
            "criteria": {"current_streak": 100},
            "points": 500
        },
        
        # ========== ACCURACY BADGES ==========
        {
            "name": "Sharpshooter",
            "description": "Achieve 90% accuracy",
            "category": "achievement",
            "tier": "silver",
            "icon": "🎯",
            "color": "#C0C0C0",
            "criteria": {"accuracy": 90, "total_attempts": 20},
            "points": 40
        },
        {
            "name": "Perfectionist",
            "description": "Achieve 95% accuracy",
            "category": "achievement",
            "tier": "gold",
            "icon": "💯",
            "color": "#FFD700",
            "criteria": {"accuracy": 95, "total_attempts": 50},
            "points": 100
        },
        {
            "name": "Flawless",
            "description": "Achieve 98% accuracy",
            "category": "achievement",
            "tier": "platinum",
            "icon": "💎",
            "color": "#E5E4E2",
            "criteria": {"accuracy": 98, "total_attempts": 100},
            "points": 200
        },
        
        # ========== PRACTICE BADGES ==========
        {
            "name": "Getting Started",
            "description": "Complete 10 practice problems",
            "category": "achievement",
            "tier": "bronze",
            "icon": "✏️",
            "color": "#CD7F32",
            "criteria": {"total_attempts": 10},
            "points": 5
        },
        {
            "name": "Practice Makes Perfect",
            "description": "Complete 100 practice problems",
            "category": "achievement",
            "tier": "silver",
            "icon": "📝",
            "color": "#C0C0C0",
            "criteria": {"total_attempts": 100},
            "points": 50
        },
        {
            "name": "Problem Solver",
            "description": "Complete 500 practice problems",
            "category": "achievement",
            "tier": "gold",
            "icon": "🧩",
            "color": "#FFD700",
            "criteria": {"total_attempts": 500},
            "points": 150
        },
        {
            "name": "Master Practitioner",
            "description": "Complete 1000 practice problems",
            "category": "achievement",
            "tier": "platinum",
            "icon": "🏅",
            "color": "#E5E4E2",
            "criteria": {"total_attempts": 1000},
            "points": 300
        },
        
        # ========== CATEGORY BADGES ==========
        {
            "name": "Algebra Expert",
            "description": "Master all Algebra skills",
            "category": "mastery",
            "tier": "gold",
            "icon": "📐",
            "color": "#FFD700",
            "criteria": {"mastered_skills": 10, "category": "Algebra"},
            "points": 120
        },
        {
            "name": "Geometry Master",
            "description": "Master all Geometry skills",
            "category": "mastery",
            "tier": "gold",
            "icon": "📏",
            "color": "#FFD700",
            "criteria": {"mastered_skills": 10, "category": "Geometry"},
            "points": 120
        },
        {
            "name": "Calculus Wizard",
            "description": "Master all Calculus skills",
            "category": "mastery",
            "tier": "platinum",
            "icon": "🧙",
            "color": "#E5E4E2",
            "criteria": {"mastered_skills": 10, "category": "Calculus"},
            "points": 200
        },
        {
            "name": "Statistics Pro",
            "description": "Master all Statistics skills",
            "category": "mastery",
            "tier": "gold",
            "icon": "📊",
            "color": "#FFD700",
            "criteria": {"mastered_skills": 7, "category": "Statistics"},
            "points": 100
        },
        
        # ========== SPECIAL BADGES ==========
        {
            "name": "Early Bird",
            "description": "Complete a lesson before 8 AM",
            "category": "social",
            "tier": "bronze",
            "icon": "🌅",
            "color": "#CD7F32",
            "criteria": {"account_age_days": 1},
            "points": 10
        },
        {
            "name": "Night Owl",
            "description": "Complete a lesson after 10 PM",
            "category": "social",
            "tier": "bronze",
            "icon": "🦉",
            "color": "#CD7F32",
            "criteria": {"account_age_days": 1},
            "points": 10
        },
    ]
    
    for badge_data in badges_data:
        badge = mastery.Badge(
            name=badge_data["name"],
            description=badge_data["description"],
            category=badge_data["category"],
            tier=badge_data["tier"],
            icon=badge_data["icon"],
            color=badge_data["color"],
            criteria=badge_data["criteria"],
            points=badge_data["points"]
        )
        db.add(badge)
    
    db.commit()
    
    print(f"✅ Created {len(badges_data)} badges")


def main():
    """Main seed function"""
    print("\n" + "="*60)
    print("  SEEDING PHASE 13: MASTERY-BASED PROGRESSION")
    print("="*60 + "\n")
    
    # Initialize database
    init_db()
    
    # Get database session
    db = next(get_db())
    
    try:
        seed_skills(db)
        seed_badges(db)
        
        print("\n" + "="*60)
        print("  ✅ SEEDING COMPLETE!")
        print("="*60 + "\n")
        
        # Print summary
        skill_count = db.query(mastery.MasterySkill).count()
        badge_count = db.query(mastery.Badge).count()
        
        print(f"Total Skills: {skill_count}")
        print(f"Total Badges: {badge_count}")
        print("\nSkills by category:")
        from sqlalchemy import func
        categories = db.query(
            mastery.MasterySkill.category, func.count(mastery.MasterySkill.id)
        ).group_by(mastery.MasterySkill.category).all()
        
        for category, count in categories:
            print(f"  - {category}: {count} skills")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
