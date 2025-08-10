import { User, Thread } from "../types";

const apiUrl = process.env.API_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "ApiError";
  }
}

export const api = {
  // Fetch all users
  async getUsers(): Promise<User[]> {
    const response = await fetch(`${apiUrl}/users`);
    
    if (!response.ok) {
      throw new ApiError("Failed to fetch users", response.status);
    }
    
    return response.json();
  },

  // Get user's thread
  async getThread(apiKey: string): Promise<Thread> {
    const response = await fetch(`${apiUrl}/threads/me`, {
      headers: {
        "X-API-Key": apiKey,
      },
    });

    if (!response.ok) {
      throw new ApiError("Failed to fetch thread", response.status);
    }

    return response.json();
  },

  // Send a message
  async sendMessage(content: string, apiKey: string): Promise<{
    user_message: any;
    bot_message: any;
  }> {
    const response = await fetch(`${apiUrl}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": apiKey,
      },
      body: JSON.stringify({ content }),
    });

    if (!response.ok) {
      throw new ApiError("Failed to send message", response.status);
    }

    return response.json();
  },

  // Get user info
  async getUserInfo(apiKey: string): Promise<User> {
    const response = await fetch(`${apiUrl}/users/me`, {
      headers: {
        "X-API-Key": apiKey,
      },
    });

    if (!response.ok) {
      throw new ApiError("Failed to get user info", response.status);
    }

    return response.json();
  },
};
