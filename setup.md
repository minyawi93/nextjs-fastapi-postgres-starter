# Chatbot Application Setup Guide

## Prerequisites
- Docker and Docker Compose installed
- Python 3.9+ installed
- Node.js 18+ installed

## Setup Steps

### 1. Start the Database
```bash
docker-compose up -d database
```

### 2. Set up the Backend
```bash
cd backend

# Install dependencies (using Poetry)
poetry install

# Create database tables
python create_tables.py

# Seed the database with users and initial data
python seed.py

# Start the backend server
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Set up the Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start the frontend server
npm run dev
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Features Implemented

- **Multi-User Support**: Three default users (Alice, Bob, Charlie) with unique API keys
- **API Key Authentication**: Secure authentication using API keys in request headers
- **User Selection Interface**: Choose which user to log in as
- **Message Threads**: Each user has a dedicated conversation thread
- **Real-time Chat**: Send messages and receive bot responses
- **Message Persistence**: All messages stored in PostgreSQL
- **Modern UI**: Clean, responsive chat interface
- **Loading States**: Visual feedback during API calls and message sending
- **Error Handling**: Graceful error handling with user-friendly messages
- **Type Safety**: Full TypeScript support with proper type definitions

## API Endpoints

### Public Endpoints
- `GET /users` - Get all available users (for user selection)

### Authenticated Endpoints (require X-API-Key header)
- `GET /users/me` - Get current user information
- `GET /threads/me` - Get user's chat thread with messages
- `POST /messages` - Send a message and get bot response

## Database Schema

- **User**: id, name, api_key (unique)
- **Thread**: id, user_id, created_at
- **Message**: id, thread_id, content, is_from_user, created_at

## Default Users

The application comes with three pre-configured users:

| User | API Key | Description |
|------|---------|-------------|
| Alice | `alice_key_123` | Default user with initial messages |
| Bob | `bob_key_456` | Second user with separate thread |
| Charlie | `charlie_key_789` | Third user with separate thread |

## Testing the Application

1. Open http://localhost:3000 in your browser
2. You'll see a user selection screen with Alice, Bob, and Charlie
3. Click on any user to log in as that person
4. You'll see their personal chat thread with any existing messages
5. Type a message in the input field and press Enter or click Send
6. The bot will respond with a random message
7. All messages are persisted and will remain after page refresh
8. Click "Switch User" to log in as a different user

## Frontend Architecture

### Component Structure
- **UserSelector**: Displays available users for selection
- **ChatInterface**: Main chat interface with messages and input
- **API Utility**: Centralized API communication layer
- **Type Definitions**: Shared TypeScript types for type safety

### Key Features
- **Multi-user Authentication**: Each user has their own API key
- **Error Handling**: Comprehensive error states and retry functionality
- **Responsive Design**: Works on desktop and mobile devices

## Backend Architecture

### Authentication
- **API Key Authentication**: Uses `X-API-Key` header for user identification
- **User Validation**: Backend validates API keys against database
- **Session Management**: Each request is authenticated independently

### Database Operations
- **Async SQLAlchemy**: Uses async database operations for better performance
- **Relationship Management**: Proper foreign key relationships between users, threads, and messages
- **Data Seeding**: Automatic creation of default users and initial messages

## Troubleshooting

### Common Issues

**Database Connection Issues**
- Ensure Docker is running: `docker ps`
- Restart database: `docker-compose restart database`
- Recreate tables: `python create_tables.py && python seed.py`

**Backend Server Issues**
- Use Poetry for dependencies: `poetry install`
- Check Python version: `python --version` (should be 3.9+)
- Verify port availability: `lsof -i :8000`

**Frontend Connection Issues**
- Check backend is running on http://localhost:8000
- Verify CORS is enabled in backend
- Check browser console for error messages

**Authentication Issues**
- Ensure API keys are being sent in `X-API-Key` header
- Verify user exists in database
- Check backend logs for authentication errors

### Debug Commands

```bash
# Check database status
docker-compose ps

# View backend logs
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test API endpoints
curl http://localhost:8000/users
curl -H "X-API-Key: alice_key_123" http://localhost:8000/users/me

# Reset database
docker-compose down
docker-compose up -d database
python create_tables.py
python seed.py
```

## Development Notes

- **Environment Variables**: Backend uses environment variables for configuration
- **Hot Reload**: Both frontend and backend support hot reloading during development
- **Type Safety**: Full TypeScript support with strict type checking
- **Error Boundaries**: Frontend includes error boundaries for graceful error handling
- **Testing**: Backend includes pytest-based test suite in `tests/` directory
