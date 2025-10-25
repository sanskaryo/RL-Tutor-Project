"""
Seed database with sample educational content
"""
import sys
sys.path.append('.')

from app.core.database import SessionLocal, init_db
from app.models.models import Content

# Sample questions for each topic
SAMPLE_CONTENT = [
    # Algebra Questions (Difficulty 1-2)
    {
        "title": "Basic Linear Equation",
        "description": "Solve for x",
        "topic": "algebra",
        "difficulty": 1,
        "content_type": "question",
        "question_text": "Solve: 2x + 5 = 13",
        "correct_answer": "4",
        "options": ["2", "3", "4", "5"],
        "explanation": "Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4",
        "tags": ["linear_equations", "beginner"]
    },
    {
        "title": "Simple Equation",
        "description": "Basic algebra practice",
        "topic": "algebra",
        "difficulty": 1,
        "content_type": "question",
        "question_text": "Solve: x - 7 = 12",
        "correct_answer": "19",
        "options": ["15", "17", "19", "21"],
        "explanation": "Add 7 to both sides: x = 19",
        "tags": ["linear_equations", "beginner"]
    },
    {
        "title": "Two-Step Equation",
        "description": "Solve algebraic equation",
        "topic": "algebra",
        "difficulty": 2,
        "content_type": "question",
        "question_text": "Solve: 3x - 4 = 11",
        "correct_answer": "5",
        "options": ["3", "4", "5", "6"],
        "explanation": "Add 4 to both sides: 3x = 15, then divide by 3: x = 5",
        "tags": ["linear_equations", "intermediate"]
    },
    {
        "title": "Equation with Fractions",
        "description": "Algebra with fractions",
        "topic": "algebra",
        "difficulty": 3,
        "content_type": "question",
        "question_text": "Solve: x/2 + 3 = 7",
        "correct_answer": "8",
        "options": ["6", "7", "8", "9"],
        "explanation": "Subtract 3: x/2 = 4, then multiply by 2: x = 8",
        "tags": ["fractions", "intermediate"]
    },
    {
        "title": "Quadratic Introduction",
        "description": "Basic quadratic",
        "topic": "algebra",
        "difficulty": 4,
        "content_type": "question",
        "question_text": "Solve: x² = 16",
        "correct_answer": "4",
        "options": ["2", "4", "8", "16"],
        "explanation": "Take square root of both sides: x = ±4 (positive answer is 4)",
        "tags": ["quadratic", "advanced"]
    },
    
    # Calculus Questions (Difficulty 2-4)
    {
        "title": "Basic Derivative",
        "description": "Find the derivative",
        "topic": "calculus",
        "difficulty": 2,
        "content_type": "question",
        "question_text": "Find d/dx of x²",
        "correct_answer": "2x",
        "options": ["x", "2x", "x²", "2"],
        "explanation": "Using power rule: d/dx(x²) = 2x",
        "tags": ["derivatives", "power_rule"]
    },
    {
        "title": "Constant Derivative",
        "description": "Derivative of constant",
        "topic": "calculus",
        "difficulty": 1,
        "content_type": "question",
        "question_text": "Find d/dx of 5",
        "correct_answer": "0",
        "options": ["0", "1", "5", "x"],
        "explanation": "The derivative of any constant is 0",
        "tags": ["derivatives", "beginner"]
    },
    {
        "title": "Polynomial Derivative",
        "description": "Differentiate polynomial",
        "topic": "calculus",
        "difficulty": 3,
        "content_type": "question",
        "question_text": "Find d/dx of 3x³",
        "correct_answer": "9x²",
        "options": ["3x²", "6x²", "9x²", "3x³"],
        "explanation": "Using power rule: d/dx(3x³) = 3·3x² = 9x²",
        "tags": ["derivatives", "power_rule", "intermediate"]
    },
    {
        "title": "Chain Rule",
        "description": "Apply chain rule",
        "topic": "calculus",
        "difficulty": 4,
        "content_type": "question",
        "question_text": "Find d/dx of (x² + 1)²",
        "correct_answer": "4x(x² + 1)",
        "options": ["2x", "4x", "4x(x² + 1)", "2(x² + 1)"],
        "explanation": "Chain rule: 2(x² + 1) · 2x = 4x(x² + 1)",
        "tags": ["chain_rule", "advanced"]
    },
    
    # Geometry Questions (Difficulty 1-3)
    {
        "title": "Area of Rectangle",
        "description": "Calculate area",
        "topic": "geometry",
        "difficulty": 1,
        "content_type": "question",
        "question_text": "Find the area of a rectangle with length 5 and width 3",
        "correct_answer": "15",
        "options": ["8", "12", "15", "18"],
        "explanation": "Area = length × width = 5 × 3 = 15",
        "tags": ["area", "rectangles", "beginner"]
    },
    {
        "title": "Perimeter of Square",
        "description": "Calculate perimeter",
        "topic": "geometry",
        "difficulty": 1,
        "content_type": "question",
        "question_text": "Find the perimeter of a square with side length 7",
        "correct_answer": "28",
        "options": ["14", "21", "28", "49"],
        "explanation": "Perimeter = 4 × side = 4 × 7 = 28",
        "tags": ["perimeter", "squares", "beginner"]
    },
    {
        "title": "Pythagorean Theorem",
        "description": "Apply Pythagorean theorem",
        "topic": "geometry",
        "difficulty": 3,
        "content_type": "question",
        "question_text": "In a right triangle with legs 3 and 4, find the hypotenuse",
        "correct_answer": "5",
        "options": ["5", "6", "7", "12"],
        "explanation": "a² + b² = c², so 3² + 4² = 9 + 16 = 25, c = 5",
        "tags": ["pythagorean", "triangles", "intermediate"]
    },
    {
        "title": "Circle Area",
        "description": "Calculate circle area",
        "topic": "geometry",
        "difficulty": 2,
        "content_type": "question",
        "question_text": "Find the area of a circle with radius 4 (use π ≈ 3.14)",
        "correct_answer": "50.24",
        "options": ["25.12", "50.24", "12.56", "100.48"],
        "explanation": "Area = πr² = 3.14 × 4² = 3.14 × 16 = 50.24",
        "tags": ["circles", "area", "intermediate"]
    },
    
    # Statistics Questions (Difficulty 1-3)
    {
        "title": "Mean Calculation",
        "description": "Find the mean",
        "topic": "statistics",
        "difficulty": 1,
        "content_type": "question",
        "question_text": "Find the mean of: 2, 4, 6, 8",
        "correct_answer": "5",
        "options": ["4", "5", "6", "7"],
        "explanation": "Mean = (2+4+6+8)/4 = 20/4 = 5",
        "tags": ["mean", "average", "beginner"]
    },
    {
        "title": "Median Value",
        "description": "Find the median",
        "topic": "statistics",
        "difficulty": 2,
        "content_type": "question",
        "question_text": "Find the median of: 1, 3, 5, 7, 9",
        "correct_answer": "5",
        "options": ["3", "5", "7", "9"],
        "explanation": "Median is the middle value when sorted: 5",
        "tags": ["median", "intermediate"]
    },
    {
        "title": "Mode Identification",
        "description": "Find the mode",
        "topic": "statistics",
        "difficulty": 2,
        "content_type": "question",
        "question_text": "Find the mode of: 2, 3, 3, 4, 5",
        "correct_answer": "3",
        "options": ["2", "3", "4", "5"],
        "explanation": "Mode is the most frequent value: 3 appears twice",
        "tags": ["mode", "intermediate"]
    },
    {
        "title": "Probability",
        "description": "Calculate probability",
        "topic": "statistics",
        "difficulty": 3,
        "content_type": "question",
        "question_text": "What is the probability of rolling a 6 on a fair die?",
        "correct_answer": "1/6",
        "options": ["1/6", "1/5", "1/4", "1/2"],
        "explanation": "Probability = favorable outcomes / total outcomes = 1/6",
        "tags": ["probability", "intermediate"]
    },
]


def seed_content():
    """Seed database with sample content"""
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if content already exists
        existing_count = db.query(Content).count()
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} content items")
            response = input("Do you want to add more content? (y/n): ")
            if response.lower() != 'y':
                print("❌ Seeding cancelled")
                return
        
        # Add sample content
        added_count = 0
        for content_data in SAMPLE_CONTENT:
            content = Content(**content_data)
            db.add(content)
            added_count += 1
        
        db.commit()
        print(f"✅ Successfully added {added_count} content items to database")
        print(f"📊 Total content items: {db.query(Content).count()}")
        
        # Show content distribution
        print("\n📚 Content Distribution:")
        for topic in ["algebra", "calculus", "geometry", "statistics"]:
            count = db.query(Content).filter(Content.topic == topic).count()
            print(f"  - {topic.capitalize()}: {count} items")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_content()
