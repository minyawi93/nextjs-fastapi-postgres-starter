from sqlalchemy import select
from sqlalchemy.orm import Session
from db_engine import sync_engine
from models import User, Thread, Message


def seed_user_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            # Check if users exist
            users = session.execute(select(User)).scalars().all()
            
            if not users:
                print("Seeding users")
                
                # Create multiple users with API keys
                users_data = [
                    {"name": "Alice", "api_key": "alice_key_123"},
                    {"name": "Bob", "api_key": "bob_key_456"},
                    {"name": "Charlie", "api_key": "charlie_key_789"}
                ]
                
                for user_data in users_data:
                    user = User(name=user_data["name"], api_key=user_data["api_key"])
                    session.add(user)
                    session.flush()  # Flush to get the user ID
                    
                    # Create a default thread for each user
                    thread = Thread(user_id=user.id)
                    session.add(thread)
                    session.flush()  # Flush to get the thread ID
                    
                    # Add some sample messages for each user
                    sample_messages = [
                        Message(thread_id=thread.id, content=f"Hello {user.name}! How can I help you today?", is_from_user=False),
                        Message(thread_id=thread.id, content="I'm here to assist you with any questions.", is_from_user=False),
                    ]
                    
                    for message in sample_messages:
                        session.add(message)
                
                session.commit()
                print(f"Created {len(users_data)} users with threads and sample messages")
                print("Available API keys:")
                for user_data in users_data:
                    print(f"  {user_data['name']}: {user_data['api_key']}")
            else:
                print(f"Found {len(users)} existing users")
                
                # Ensure each user has a thread
                for user in users:
                    thread = session.execute(select(Thread).where(Thread.user_id == user.id)).scalar_one_or_none()
                    
                    if thread is None:
                        print(f"Creating thread for user {user.name}")
                        thread = Thread(user_id=user.id)
                        session.add(thread)
                        session.commit()
                        print(f"Thread created for {user.name}")
                    else:
                        print(f"Thread already exists for {user.name}")


if __name__ == "__main__":
    seed_user_if_needed()
