# Frontend - Multi-User Chatbot

This is the Next.js frontend for the multi-user chatbot application with API key authentication.

## Features

- **Multi-User Support**: Switch between different users (Alice, Bob, Charlie)
- **API Key Authentication**: Each user has their own API key for secure access
- **Real-time Messaging**: Send and receive messages with the AI assistant
- **Persistent Conversations**: Each user maintains their own conversation thread
- **Modern UI**: Clean, responsive interface built with Tailwind CSS

## Project Structure

```
frontend/app/
├── components/
│   ├── UserSelector.tsx    # User selection interface
│   └── ChatInterface.tsx   # Main chat interface
├── types/
│   └── index.ts           # Shared TypeScript types
├── utils/
│   └── api.ts             # API utility functions
├── globals.css            # Global styles
├── layout.tsx             # Root layout
└── page.tsx               # Main page component
```

## Components

### UserSelector
- Fetches available users from the API
- Displays user selection interface
- Handles connection errors gracefully
- Provides retry functionality

### ChatInterface
- Manages user authentication
- Handles message sending and receiving
- Displays conversation history
- Provides user switching functionality

### API Utilities
- Centralized API calls
- Error handling with custom `ApiError` class
- Type-safe API responses

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set environment variables** (optional):
   ```bash
   # .env.local
   API_URL=http://localhost:8000
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Ensure backend is running**:
   ```bash
   # In backend directory
   poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage

1. **Select a User**: Choose from Alice, Bob, or Charlie
2. **Start Chatting**: Send messages and receive AI responses
3. **Switch Users**: Use the "Switch User" button to change users
4. **View History**: Each user maintains their own conversation thread

## Authentication

The frontend uses API key authentication:
- **Alice**: `alice_key_123`
- **Bob**: `bob_key_456`
- **Charlie**: `charlie_key_789`

API keys are automatically included in request headers for authenticated endpoints.

## User Interface

### User Selection Screen
- Clean, card-based layout
- User information display
- Error handling for connection issues
- Retry functionality

### Chat Interface
- Real-time message display
- User identification in header
- Message timestamps
- Loading states and error handling

## State Management

Uses React hooks for state management:
- `useState` for local component state
- `useEffect` for side effects and API calls
- `useRef` for DOM references (auto-scroll)

## Error Handling

Comprehensive error handling:
- Network connection errors
- API authentication failures
- Message sending failures
- User-friendly error messages
- Retry mechanisms



## API Integration

The frontend integrates with these backend endpoints:
- `GET /users` - Fetch available users
- `GET /users/me` - Get current user info
- `GET /threads/me` - Get user's conversation thread
- `POST /messages` - Send a message

All authenticated endpoints require the `X-API-Key` header.


