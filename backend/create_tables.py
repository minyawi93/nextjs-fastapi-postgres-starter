from db_engine import sync_engine
from models import Base

def create_tables():
    Base.metadata.create_all(bind=sync_engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    create_tables()
