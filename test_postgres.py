import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="rl_tutor",
            user="postgres",
            password="mysecretpassword",  # Change this to your actual password
            host="localhost",
            port="5432"
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Test basic query
        print("🔍 Testing connection...")
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ PostgreSQL Version: {version[0]}\n")
        
        # List all tables
        print("📋 Listing tables in the database:")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        for table in tables:
            print(f"- {table[0]}")
            
            # Get column information for each table
            cur.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table[0]}'
            """)
            columns = cur.fetchall()
            for col in columns:
                print(f"  └─ {col[0]} ({col[1]})")
            print()
        
        # Close connection
        cur.close()
        conn.close()
        print("\n✅ Database connection test successful!")
        
    except OperationalError as e:
        print("\n❌ Error connecting to PostgreSQL database:")
        print(f"Error: {str(e)}")
        print("\nPlease check:")
        print("1. PostgreSQL is running in Docker (docker ps)")
        print("2. Port 5432 is mapped correctly (docker port my-postgres)")
        print("3. Password is correct in the script")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    print("\n🔌 Testing PostgreSQL Connection...")
    print("=====================================")
    test_connection()