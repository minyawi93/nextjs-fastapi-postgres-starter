"use client";

import { useState } from "react";
import UserSelector from "./components/UserSelector";
import ChatInterface from "./components/ChatInterface";
import { User } from "./types";

export default function Home() {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const handleUserSelect = (user: User) => {
    setSelectedUser(user);
  };

  const handleSwitchUser = () => {
    setSelectedUser(null);
  };

  if (!selectedUser) {
    return <UserSelector onUserSelect={handleUserSelect} />;
  }

  return <ChatInterface user={selectedUser} onSwitchUser={handleSwitchUser} />;
}
