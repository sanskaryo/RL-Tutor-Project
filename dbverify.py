# import os
# from sqlalchemy import create_engine, text
# from pymongo import MongoClient
# from dotenv import load_dotenv

# load_dotenv()

# def test_postgresql():
#     try:
#         db_url = os.getenv("DATABASE_URL")
#         engine = create_engine(db_url)
#         with engine.connect() as conn:
#             result = conn.execute(text("SELECT version();"))
#             print("✅ PostgreSQL Connected!")
#             print(f"Version: {result.fetchone()[0]}")
#     except Exception as e:
#         print(f"❌ PostgreSQL Error: {e}")

# def test_mongodb():
#     try:
#         mongo_uri = os.getenv("MONGODB_URI")
#         client = MongoClient(mongo_uri)
#         db = client[os.getenv("MONGODB_DB_NAME")]
#         print("✅ MongoDB Connected!")
#         print(f"Available collections: {db.list_collection_names()}")
#     except Exception as e:
#         print(f"❌ MongoDB Error: {e}")

# if __name__ == "__main__":
#     test_postgresql()
#     test_mongodb()

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def init_database():
    engine = create_engine(os.getenv("DATABASE_URL"))
    
    with engine.connect() as conn:
        # Create users table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """))
        
        # Create user_progress table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            topic VARCHAR(100),
            score FLOAT,
            attempts INTEGER DEFAULT 1,
            last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """))
        
        print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_database()