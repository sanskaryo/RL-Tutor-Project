"""Quick script to check database content"""
from app.core.database import SessionLocal
from app.models.models import Content

db = SessionLocal()
try:
    total = db.query(Content).count()
    print(f"✅ Total content in database: {total}")
    
    if total > 0:
        # Get difficulty distribution
        difficulties = db.query(Content.difficulty).distinct().all()
        diff_list = sorted([d[0] for d in difficulties if d[0]])
        print(f"📊 Difficulty levels: {diff_list}")
        
        # Get topics
        topics = db.query(Content.topic).distinct().all()
        topic_list = [t[0] for t in topics if t[0]]
        print(f"📚 Topics available: {topic_list}")
        
        # Show sample questions
        print(f"\n📝 Sample questions:")
        samples = db.query(Content).limit(3).all()
        for i, content in enumerate(samples, 1):
            print(f"  {i}. {content.title} (Difficulty: {content.difficulty}, Topic: {content.topic})")
    else:
        print("❌ No content found in database!")
        print("💡 Run: python populate_jee_questions.py")
        
finally:
    db.close()
