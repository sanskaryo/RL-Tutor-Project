import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
import sys

def test_mongodb_connection(uri, db_name=None, collection_name=None):
    try:
        print(f"Attempting to connect to: {uri.split('@')[-1] if '@' in uri else uri}")
        
        # Create a new client and connect to the server
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)  # 5 second timeout
        
        # The ismaster command is cheap and does not require auth
        client.admin.command('ismaster')
        print("✅ Successfully connected to MongoDB")
        
        if db_name:
            print(f"\n📂 Accessing database: {db_name}")
            db = client[db_name]
            
            # List all collections in the database
            collections = db.list_collection_names()
            print(f"📋 Available collections: {collections}")
            
            if collection_name:
                print(f"\n📄 Accessing collection: {collection_name}")
                collection = db[collection_name]
                
                # Get document count
                count = collection.count_documents({})
                print(f"📊 Document count: {count}")
                
                # Get one sample document
                if count > 0:
                    sample = collection.find_one()
                    print("\n📝 Sample document:")
                    print(sample)
        
        return True
        
    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
    except ConnectionFailure as e:
        print(f"❌ Could not connect to MongoDB: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    return False

if __name__ == "__main__":
    # Replace these with your actual values
    MONGODB_URI = "mongodb+srv://sankhuzzy:VvksMgQY2mUN77nZ@cluster0.4dob0.mongodb.net/"  # e.g., "mongodb://localhost:27017"
    DB_NAME = "your_database_name"          # e.g., "jee_tutor"
    COLLECTION_NAME = "your_collection"     # e.g., "document_chunks"
    
    print("🔍 MongoDB Connection Tester")
    print("=" * 30)
    
    # Test connection
    if test_mongodb_connection(MONGODB_URI, DB_NAME, COLLECTION_NAME):
        print("\n✅ Connection test completed successfully")
    else:
        print("\n❌ Connection test failed")
        sys.exit(1)