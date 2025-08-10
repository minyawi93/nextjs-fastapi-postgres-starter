"""
Multi-user API tests for the chatbot application
"""

import pytest
import requests
import time
from typing import Dict, List

class TestMultiUserAPI:
    """Multi-user API functionality tests"""
    
    def test_list_all_users(self, base_url: str):
        """Test listing all users and verify structure"""
        response = requests.get(f"{base_url}/users")
        assert response.status_code == 200, "Should be able to list users"
        
        users = response.json()
        assert len(users) >= 3, "Should have at least 3 users (Alice, Bob, Charlie)"
        
        # Verify all expected users exist
        user_names = [user["name"] for user in users]
        assert "Alice" in user_names, "Alice should exist"
        assert "Bob" in user_names, "Bob should exist"
        assert "Charlie" in user_names, "Charlie should exist"
        
        # Verify user structure
        for user in users:
            assert "id" in user, "User should have id"
            assert "name" in user, "User should have name"
            assert "api_key" in user, "User should have api_key"
            assert len(user["api_key"]) > 0, "API key should not be empty"
    
    @pytest.mark.parametrize("user_name,api_key", [
        ("Alice", "alice_key_123"),
        ("Bob", "bob_key_456"),
        ("Charlie", "charlie_key_789")
    ])
    def test_user_authentication(self, base_url: str, user_name: str, api_key: str):
        """Test authentication for each user"""
        headers = {"X-API-Key": api_key}
        
        # Test getting user info
        response = requests.get(f"{base_url}/users/me", headers=headers)
        assert response.status_code == 200, f"{user_name} should be able to authenticate"
        
        user_info = response.json()
        assert user_info["name"] == user_name, f"Should return {user_name}'s info"
        assert "id" in user_info, "Should have user ID"
    
    @pytest.mark.parametrize("user_name,api_key", [
        ("Alice", "alice_key_123"),
        ("Bob", "bob_key_456"),
        ("Charlie", "charlie_key_789")
    ])
    def test_user_thread_access(self, base_url: str, user_name: str, api_key: str):
        """Test that each user can access their thread"""
        headers = {"X-API-Key": api_key}
        
        response = requests.get(f"{base_url}/threads/me", headers=headers)
        assert response.status_code == 200, f"{user_name} should be able to access thread"
        
        thread_info = response.json()
        assert "id" in thread_info, "Thread should have ID"
        assert "messages" in thread_info, "Thread should have messages"
        assert isinstance(thread_info["messages"], list), "Messages should be a list"
        assert len(thread_info["messages"]) >= 2, "Should have at least 2 initial messages"
    
    @pytest.mark.parametrize("user_name,api_key", [
        ("Alice", "alice_key_123"),
        ("Bob", "bob_key_456"),
        ("Charlie", "charlie_key_789")
    ])
    def test_user_message_sending(self, base_url: str, user_name: str, api_key: str):
        """Test that each user can send messages"""
        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        message_data = {"content": f"Hello from {user_name}!"}
        response = requests.post(f"{base_url}/messages", json=message_data, headers=headers)
        assert response.status_code == 200, f"{user_name} should be able to send message"
        
        message_response = response.json()
        assert "user_message" in message_response, "Should return user message"
        assert "bot_message" in message_response, "Should return bot response"
        
        # Verify user message
        user_msg = message_response["user_message"]
        assert user_msg["content"] == f"Hello from {user_name}!", "User message should match"
        assert user_msg["is_from_user"] is True, "Should be marked as from user"
        
        # Verify bot response
        bot_msg = message_response["bot_message"]
        assert len(bot_msg["content"]) > 0, "Bot should respond with content"
        assert bot_msg["is_from_user"] is False, "Should be marked as from bot"
    
    def test_invalid_api_key_rejection(self, base_url: str):
        """Test that invalid API keys are properly rejected"""
        invalid_keys = ["invalid_key", "wrong_key", "", "alice_key_999"]
        
        for invalid_key in invalid_keys:
            headers = {"X-API-Key": invalid_key}
            response = requests.get(f"{base_url}/users/me", headers=headers)
            assert response.status_code == 401, f"Should reject invalid key: {invalid_key}"
    
    def test_missing_api_key_rejection(self, base_url: str):
        """Test that missing API key is properly rejected"""
        # Test without any headers
        response = requests.get(f"{base_url}/users/me")
        assert response.status_code == 422, "Should reject missing API key"
        
        # Test with empty API key
        headers = {"X-API-Key": ""}
        response = requests.get(f"{base_url}/users/me", headers=headers)
        assert response.status_code == 401, "Should reject empty API key"
    
    def test_message_persistence(self, base_url: str, alice_headers: Dict[str, str], json_headers: Dict[str, str]):
        """Test that messages are persisted between requests"""
        headers = {**alice_headers, **json_headers}
        
        # Send a unique message
        unique_content = f"Persistence test message {time.time()}"
        message_data = {"content": unique_content}
        
        response = requests.post(f"{base_url}/messages", json=message_data, headers=headers)
        assert response.status_code == 200, "Should be able to send message"
        
        # Get thread to verify message was saved
        response = requests.get(f"{base_url}/threads/me", headers=alice_headers)
        assert response.status_code == 200, "Should be able to get thread"
        
        thread_info = response.json()
        messages = thread_info["messages"]
        
        # Find our message in the thread
        user_messages = [msg for msg in messages if msg["is_from_user"] and msg["content"] == unique_content]
        assert len(user_messages) == 1, "Message should be persisted in thread"
    
    def test_multiple_messages_same_user(self, base_url: str, bob_headers: Dict[str, str], json_headers: Dict[str, str]):
        """Test sending multiple messages as the same user"""
        headers = {**bob_headers, **json_headers}
        
        messages = [
            "First test message",
            "Second test message", 
            "Third test message"
        ]
        
        for i, content in enumerate(messages):
            message_data = {"content": content}
            response = requests.post(f"{base_url}/messages", json=message_data, headers=headers)
            assert response.status_code == 200, f"Should be able to send message {i+1}"
            
            message_response = response.json()
            assert message_response["user_message"]["content"] == content, f"Message {i+1} should match"
            assert len(message_response["bot_message"]["content"]) > 0, f"Bot should respond to message {i+1}"
    
    def test_empty_message_handling(self, base_url: str, charlie_headers: Dict[str, str], json_headers: Dict[str, str]):
        """Test handling of empty messages"""
        headers = {**charlie_headers, **json_headers}
        
        # Test empty string
        message_data = {"content": ""}
        response = requests.post(f"{base_url}/messages", json=message_data, headers=headers)
        assert response.status_code == 200, "Should handle empty message"
        
        # Test missing content field
        response = requests.post(f"{base_url}/messages", json={}, headers=headers)
        assert response.status_code == 422, "Should reject missing content field"
    
    def test_message_structure_validation(self, base_url: str, alice_headers: Dict[str, str], json_headers: Dict[str, str]):
        """Test that message responses have correct structure"""
        headers = {**alice_headers, **json_headers}
        
        message_data = {"content": "Structure test message"}
        response = requests.post(f"{base_url}/messages", json=message_data, headers=headers)
        assert response.status_code == 200, "Should be able to send message"
        
        message_response = response.json()
        
        # Check user message structure
        user_msg = message_response["user_message"]
        required_user_fields = ["id", "content", "is_from_user", "created_at"]
        for field in required_user_fields:
            assert field in user_msg, f"User message should have {field}"
        
        # Check bot message structure
        bot_msg = message_response["bot_message"]
        required_bot_fields = ["id", "content", "is_from_user", "created_at"]
        for field in required_bot_fields:
            assert field in bot_msg, f"Bot message should have {field}"
        
        # Check data types
        assert isinstance(user_msg["id"], int), "User message ID should be integer"
        assert isinstance(user_msg["content"], str), "User message content should be string"
        assert isinstance(user_msg["is_from_user"], bool), "User message is_from_user should be boolean"
        assert isinstance(bot_msg["id"], int), "Bot message ID should be integer"
        assert isinstance(bot_msg["content"], str), "Bot message content should be string"
        assert isinstance(bot_msg["is_from_user"], bool), "Bot message is_from_user should be boolean"
