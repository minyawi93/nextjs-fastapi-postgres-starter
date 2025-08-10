# Real-Time Chatbot Application

A full-stack real-time chatbot application built with Next.js, FastAPI, and PostgreSQL, featuring multi-user support with API key authentication.

## 🚀 Features

- **Multi-User Support**: Three default users (Alice, Bob, Charlie) with unique API keys
- **API Key Authentication**: Secure authentication using API keys in request headers
- **User Selection Interface**: Choose which user to log in as
- **Real-time Chat Interface**: Modern, responsive chat UI
- **Message Persistence**: All messages stored in PostgreSQL database
- **Bot Responses**: Automated responses with random message selection
- **Modern UI**: Clean, intuitive interface
- **Type Safety**: Full TypeScript support with proper type definitions
- **Error Handling**: Graceful error handling with user-friendly messages
- **RESTful API**: Well-structured FastAPI backend with proper error handling

## 🏗️ Architecture

### Frontend (Next.js 14)
- **State Management**: React hooks for local state
- **Component Structure**: Modular components (UserSelector, ChatInterface)
- **API Layer**: Centralized API utility with error handling
- **Type Safety**: Shared TypeScript types for consistency

### Backend (FastAPI)
- **Framework**: FastAPI with async/await support
- **Database**: SQLAlchemy ORM with PostgreSQL
- **Authentication**: API key-based authentication system
- **CORS**: Configured for frontend communication
- **API Documentation**: Auto-generated with FastAPI

### Database (PostgreSQL)
- **User Table**: Stores user information with API keys
- **Thread Table**: Manages conversation threads per user
- **Message Table**: Stores all chat messages with metadata

## 📊 Database Schema

```sql
-- Users table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    api_key VARCHAR(50) UNIQUE NOT NULL
);

-- Threads table
CREATE TABLE "thread" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE "message" (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES "thread"(id),
    content TEXT NOT NULL,
    is_from_user BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🛠️ Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Node.js 18+

### 1. Start Database
```bash
docker-compose up -d database
```

### 2. Backend Setup
```bash
cd backend
poetry install
python create_tables.py
python seed.py
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔌 API Endpoints

### Public Endpoints
- `GET /users` - Get all available users (for user selection)

### Authenticated Endpoints (require X-API-Key header)
- `GET /users/me` - Get current user information
- `GET /threads/me` - Get user's chat thread with all messages
- `POST /messages` - Send a message and receive bot response

### Request/Response Examples

**Get Users (Public):**
```bash
GET /users
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Alice",
    "api_key": "alice_key_123"
  },
  {
    "id": 2,
    "name": "Bob",
    "api_key": "bob_key_456"
  }
]
```

**Send Message (Authenticated):**
```bash
POST /messages
Content-Type: application/json
X-API-Key: alice_key_123

{
  "content": "Hello, how are you?"
}
```

**Response:**
```json
{
  "user_message": {
    "id": 1,
    "content": "Hello, how are you?",
    "is_from_user": true,
    "created_at": "2024-01-01T12:00:00"
  },
  "bot_message": {
    "id": 2,
    "content": "I'm here to help! What would you like to discuss?",
    "is_from_user": false,
    "created_at": "2024-01-01T12:00:01"
  }
}
```

## 👥 Default Users

The application comes with three pre-configured users:

| User | API Key | Description |
|------|---------|-------------|
| Alice | `alice_key_123` | Default user with initial messages |
| Bob | `bob_key_456` | Second user with separate thread |
| Charlie | `charlie_key_789` | Third user with separate thread |

## 🎯 Implementation Details

### Multi-User Authentication
- **API Key System**: Each user has a unique API key for authentication
- **Header-based Auth**: API keys sent in `X-API-Key` request header
- **User Validation**: Backend validates API keys against database
- **Session Independence**: Each request authenticated independently

### Frontend Component Architecture
- **UserSelector**: Displays available users for selection
- **ChatInterface**: Main chat interface with messages and input
- **API Utility**: Centralized API communication layer
- **Type Definitions**: Shared TypeScript types for type safety

### Error Handling
- **Frontend**: Try-catch blocks with user-friendly error messages
- **Backend**: HTTP status codes with descriptive error messages
- **API Layer**: Custom ApiError class for consistent error handling
- **Database**: Proper transaction handling with rollback on errors

### Performance Considerations
- **Database Indexing**: Primary keys and foreign keys for efficient queries
- **Async Operations**: Non-blocking database operations
- **Connection Pooling**: SQLAlchemy connection management
- **Frontend Optimization**: React key props and efficient re-renders
- **Type Safety**: TypeScript prevents runtime errors

## 🧪 Testing the Application

1. **Start the Application**: Follow setup instructions above
2. **Access Application**: Open http://localhost:3000
3. **Select User**: Choose Alice, Bob, or Charlie from the user selection screen
4. **Send Messages**: Type in the input field and press Enter
5. **Switch Users**: Click "Switch User" to test different user accounts
6. **Verify Persistence**: Refresh the page to see messages remain
7. **Check API**: Visit http://localhost:8000/docs for API testing

## 🔧 Development Notes

### Code Structure
```
├── backend/
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # SQLAlchemy database models
│   ├── db_engine.py     # Database connection setup
│   ├── seed.py          # Database seeding logic
│   ├── create_tables.py # Table creation script
│   └── tests/           # Pytest-based test suite
├── frontend/
│   └── app/
│       ├── page.tsx     # Main application container
│       ├── components/  # React components
│       │   ├── UserSelector.tsx
│       │   └── ChatInterface.tsx
│       ├── types/       # TypeScript type definitions
│       └── utils/       # API utility functions
└── docker-compose.yml   # Database service configuration
```

### Key Design Decisions

1. **Multi-User System**: API key authentication for user management
2. **Component Separation**: Clear separation between user selection and chat
3. **Type Safety**: Comprehensive TypeScript usage throughout
4. **Error Resilience**: Graceful error handling at all levels
5. **RESTful API**: Standard HTTP methods for clear API design

### Authentication Flow
```
1. Frontend fetches users from /users endpoint
2. User selects a user from the list
3. Frontend stores selected user's API key
4. All subsequent requests include X-API-Key header
5. Backend validates API key and returns user-specific data
```






