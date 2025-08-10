"use client";

import { useState, useEffect, useRef } from "react";
import { User, Message, Thread } from "../types";
import { api, ApiError } from "../utils/api";

interface ChatInterfaceProps {
  user: User;
  onSwitchUser: () => void;
}

export default function ChatInterface({ user, onSwitchUser }: ChatInterfaceProps) {
  const [thread, setThread] = useState<Thread | null>(null);
  const [newMessage, setNewMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch thread data when user is selected
  useEffect(() => {
    const fetchThread = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const threadData = await api.getThread(user.api_key);
        setThread(threadData);
        setIsAuthenticated(true);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(`Authentication failed: ${err.message}`);
        } else {
          setError("Error connecting to server");
        }
        setIsAuthenticated(false);
        console.error("Error fetching thread:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchThread();
  }, [user]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [thread?.messages]);

  const sendMessage = async () => {
    if (!newMessage.trim() || isLoading) return;

    setIsLoading(true);
    try {
      const data = await api.sendMessage(newMessage, user.api_key);
      
      // Update thread with new messages
      if (thread) {
        setThread({
          ...thread,
          messages: [...thread.messages, data.user_message, data.bot_message],
        });
      }
      
      setNewMessage("");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`Failed to send message: ${err.message}`);
      } else {
        setError("Error sending message");
      }
      console.error("Error sending message:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Loading screen while authenticating
  if (isLoading || !isAuthenticated || !thread) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="text-lg text-gray-900 mb-2">
            {isLoading ? "Loading..." : "Authenticating as {user.name}..."}
          </div>
          <div className="text-sm text-gray-600">
            Loading your conversation...
          </div>
          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">
              Chat with AI Assistant
            </h1>
            <p className="text-sm text-gray-600">
              Hello, {user.name}! (ID: {user.id})
            </p>
          </div>
          <button
            onClick={onSwitchUser}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            Switch User
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {thread.messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.is_from_user ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.is_from_user
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 border border-gray-300 text-black"
              }`}
            >
              <p className="text-sm font-medium">{message.content}</p>
              <p className={`text-xs mt-1 ${
                message.is_from_user ? "text-blue-100" : "text-gray-600"
              }`}>
                {new Date(message.created_at).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="flex space-x-4">
          <div className="flex-1">
            <textarea
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-black placeholder-gray-500"
              rows={1}
              disabled={isLoading}
            />
          </div>
          <button
            onClick={sendMessage}
            disabled={!newMessage.trim() || isLoading}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "Sending..." : "Send"}
          </button>
        </div>
        {error && (
          <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}
      </div>
    </div>
  );
}
