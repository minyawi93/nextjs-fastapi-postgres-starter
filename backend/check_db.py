from sqlalchemy import text
from sqlalchemy.orm import Session
from db_engine import sync_engine
from models import User

def check_database():
    with Session(sync_engine) as session:
        # Check what tables exist
        result = session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result]
        print(f"Tables in database: {tables}")
        
        # Check user table structure
        result = session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'user'
        """))
        print("\nUser table structure:")
        for row in result:
            print(f"  {row[0]}: {row[1]} ({'NULL' if row[2] == 'YES' else 'NOT NULL'})")
        
        # Check user data
        users = session.execute(text("SELECT * FROM \"user\"")).fetchall()
        print(f"\nUser data ({len(users)} rows):")
        for user in users:
            print(f"  ID: {user[0]}, Name: {user[1]}")

if __name__ == "__main__":
    check_database()
