import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Print some debug information
print("Attempting to connect to PostgreSQL...")
connection_string = "postgresql://postgres:postgres@localhost:5432/rl_tutor"
print(f"Connection string: {connection_string}")

try:
    # Create database engine
    engine = create_engine(connection_string)
    print("Engine created successfully")
    
    # Try to connect
    print("Attempting to establish connection...")
    with engine.connect() as connection:
        print("Connection established!")
        result = connection.execute(text("SELECT 1"))
        print("✅ Successfully executed test query!")
        
        # Test query to list all tables
        print("\nQuerying for available tables...")
        result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        print("\nAvailable tables:")
        tables = result.fetchall()
        if tables:
            for row in tables:
                print(f"- {row[0]}")
        else:
            print("No tables found in public schema")
            
except SQLAlchemyError as e:
    print("❌ Database connection failed!")
    print(f"Error: {str(e)}")
    print("\nDetails:")
    print(f"Error type: {type(e).__name__}")
    print(f"Full error message: {e.args[0] if e.args else 'No additional details'}")
except Exception as e:
    print("❌ Unexpected error!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")