"use client";

import { useState, useEffect } from "react";
import { User } from "../types";
import { api, ApiError } from "../utils/api";

interface UserSelectorProps {
  onUserSelect: (user: User) => void;
  isLoading?: boolean;
}

export default function UserSelector({ onUserSelect, isLoading = false }: UserSelectorProps) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const usersData = await api.getUsers();
        setUsers(usersData);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(`Failed to fetch users: ${err.message}`);
        } else {
          setError("Error connecting to server");
        }
        console.error("Error fetching users:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="text-lg text-gray-900 mb-2">Loading users...</div>
          <div className="text-sm text-gray-600">Please wait</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
          <div className="text-center">
            <div className="text-red-600 text-lg mb-4">⚠️ Connection Error</div>
            <p className="text-gray-600 mb-6">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <h1 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          Welcome to ChatBot
        </h1>
        <p className="text-gray-600 mb-6 text-center">
          Please select a user to start chatting:
        </p>
        
        {users.length === 0 ? (
          <div className="text-center text-gray-500">
            No users available
          </div>
        ) : (
          <div className="space-y-3">
            {users.map((user) => (
              <button
                key={user.id}
                onClick={() => onUserSelect(user)}
                disabled={isLoading}
                className="w-full p-4 border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="flex items-center justify-between">
                  <span className="text-lg font-medium text-gray-900">
                    {user.name}
                  </span>
                  <span className="text-sm text-gray-500">
                    ID: {user.id}
                  </span>
                </div>
              </button>
            ))}
          </div>
        )}
        
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Note:</strong> Each user has their own conversation thread and API key for authentication.
          </p>
        </div>
      </div>
    </div>
  );
}
