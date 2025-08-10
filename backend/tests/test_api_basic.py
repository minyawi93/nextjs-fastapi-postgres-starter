"""
Basic API tests for the multi-user chatbot application
"""

import pytest
import requests
from typing import Dict

@pytest.mark.integration
@pytest.mark.api
class TestBasicAPI:
    """Basic API functionality tests"""
    
    def test_api_docs_accessible(self, base_url: str):
        """Test that API docs are accessible"""
        response = requests.get(f"{base_url}/docs")
        assert response.status_code == 200, "API docs should be accessible"
    
    def test_list_users(self, base_url: str):
        """Test listing all users (no auth required)"""
        response = requests.get(f"{base_url}/users")
        assert response.status_code == 200, "Should be able to list users"
        
        users = response.json()
        assert isinstance(users, list), "Users should be returned as a list"
        assert len(users) >= 1, "Should have at least one user"
        
        # Check user structure
        for user in users:
            assert "id" in user, "User should have id"
            assert "name" in user, "User should have name"
            assert "api_key" in user, "User should have api_key"
    
    def test_alice_authentication(self, base_url: str, alice_headers: Dict[str, str]):
        """Test Alice's authentication"""
        response = requests.get(f"{base_url}/users/me", headers=alice_headers)
        assert response.status_code == 200, "Alice should be able to authenticate"
        
        user_info = response.json()
        assert user_info["name"] == "Alice", "Should return Alice's info"
        assert "id" in user_info, "Should have user ID"
    
    def test_bob_authentication(self, base_url: str, bob_headers: Dict[str, str]):
        """Test Bob's authentication"""
        response = requests.get(f"{base_url}/users/me", headers=bob_headers)
        assert response.status_code == 200, "Bob should be able to authenticate"
        
        user_info = response.json()
        assert user_info["name"] == "Bob", "Should return Bob's info"
        assert "id" in user_info, "Should have user ID"
    
    def test_charlie_authentication(self, base_url: str, charlie_headers: Dict[str, str]):
        """Test Charlie's authentication"""
        response = requests.get(f"{base_url}/users/me", headers=charlie_headers)
        assert response.status_code == 200, "Charlie should be able to authenticate"
        
        user_info = response.json()
        assert user_info["name"] == "Charlie", "Should return Charlie's info"
        assert "id" in user_info, "Should have user ID"
    
    def test_invalid_api_key(self, base_url: str, invalid_headers: Dict[str, str]):
        """Test that invalid API key is rejected"""
        response = requests.get(f"{base_url}/users/me", headers=invalid_headers)
        assert response.status_code == 401, "Should reject invalid API key"
    
    def test_missing_api_key(self, base_url: str):
        """Test that missing API key is rejected"""
        response = requests.get(f"{base_url}/users/me")
        assert response.status_code == 422, "Should reject missing API key"
    
    def test_send_message_as_alice(self, base_url: str, alice_headers: Dict[str, str], json_headers: Dict[str, str]):
        """Test sending a message as Alice"""
        # Combine headers
        headers = {**alice_headers, **json_headers}
        
        message_data = {"content": "Hello from test!"}
        response = requests.post(f"{base_url}/messages", json=message_data, headers=headers)
        assert response.status_code == 200, "Should be able to send message"
        
        message_response = response.json()
        assert "user_message" in message_response, "Should return user message"
        assert "bot_message" in message_response, "Should return bot response"
        
        # Check user message
        user_msg = message_response["user_message"]
        assert user_msg["content"] == "Hello from test!", "User message should match"
        assert user_msg["is_from_user"] is True, "Should be marked as from user"
        
        # Check bot message
        bot_msg = message_response["bot_message"]
        assert len(bot_msg["content"]) > 0, "Bot should respond with content"
        assert bot_msg["is_from_user"] is False, "Should be marked as from bot"
