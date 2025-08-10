from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from seed import seed_user_if_needed
from sqlalchemy.ext.asyncio import AsyncSession
from db_engine import engine
from models import User, Thread, Message
from datetime import datetime
import random
import asyncio
from typing import List, Optional

seed_user_if_needed()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserRead(BaseModel):
    id: int
    name: str


class MessageRead(BaseModel):
    id: int
    content: str
    is_from_user: bool
    created_at: datetime


class MessageCreate(BaseModel):
    content: str


class ThreadRead(BaseModel):
    id: int
    messages: List[MessageRead]


@app.get("/users/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)


@app.get("/threads/me")
async def get_my_thread():
    async with AsyncSession(engine) as session:
        # Get the current user
        user_result = await session.execute(select(User))
        user = user_result.scalars().first()
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get or create thread for the user
        thread_result = await session.execute(
            select(Thread).where(Thread.user_id == user.id)
        )
        thread = thread_result.scalars().first()
        
        if thread is None:
            thread = Thread(user_id=user.id)
            session.add(thread)
            await session.commit()
        
        # Get messages for the thread
        messages_result = await session.execute(
            select(Message).where(Message.thread_id == thread.id).order_by(Message.created_at)
        )
        messages = messages_result.scalars().all()
        
        return ThreadRead(
            id=thread.id,
            messages=[MessageRead(
                id=msg.id,
                content=msg.content,
                is_from_user=msg.is_from_user,
                created_at=msg.created_at
            ) for msg in messages]
        )


@app.post("/messages")
async def create_message(message: MessageCreate):
    async with AsyncSession(engine) as session:
        # Get the current user
        user_result = await session.execute(select(User))
        user = user_result.scalars().first()
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get or create thread for the user
        thread_result = await session.execute(
            select(Thread).where(Thread.user_id == user.id)
        )
        thread = thread_result.scalars().first()
        
        if thread is None:
            thread = Thread(user_id=user.id)
            session.add(thread)
            await session.flush()
        
        # Create user message
        user_message = Message(
            thread_id=thread.id,
            content=message.content,
            is_from_user=True
        )
        session.add(user_message)
        await session.flush()
        
        # Store the user message ID before creating bot message
        user_message_id = user_message.id
        user_message_content = user_message.content
        user_message_created_at = user_message.created_at
        
        # Generate bot response
        bot_responses = [
            "That's interesting! Tell me more about that.",
            "I understand what you're saying. How can I help you further?",
            "Thanks for sharing that with me. Is there anything specific you'd like to know?",
            "I'm here to help! What would you like to discuss?",
            "That's a great point. Let me think about that for a moment...",
            "I appreciate you reaching out. How can I assist you today?",
            "That sounds fascinating! I'd love to hear more details.",
            "I'm processing what you've said. What's your next question?",
            "Thank you for the information. How can I be of service?",
            "I'm listening and ready to help. What's on your mind?"
        ]
        
        bot_message = Message(
            thread_id=thread.id,
            content=random.choice(bot_responses),
            is_from_user=False
        )
        session.add(bot_message)
        await session.flush()
        
        # Store the bot message ID before committing
        bot_message_id = bot_message.id
        bot_message_content = bot_message.content
        bot_message_created_at = bot_message.created_at
        
        await session.commit()
        
        return {
            "user_message": MessageRead(
                id=user_message_id,
                content=user_message_content,
                is_from_user=True,
                created_at=user_message_created_at
            ),
            "bot_message": MessageRead(
                id=bot_message_id,
                content=bot_message_content,
                is_from_user=False,
                created_at=bot_message_created_at
            )
        }


# @app.get("/messages/stream")
# async def stream_messages():
#     """Stream new messages for real-time updates"""
#     async def generate():
#         while True:
#             # In a real implementation, you'd use a proper message queue
#             # For now, we'll just yield a simple heartbeat
#             yield f"data: {datetime.now().isoformat()}\n\n"
#             await asyncio.sleep(1)
    
#     return generate()
