#!/usr/bin/env python3
"""
Simple test script for the multi-user API
"""

import requests
import json

# Hardcoded API keys for testing
ALICE_API_KEY = "alice_key_123"
BOB_API_KEY = "bob_key_456"
CHARLIE_API_KEY = "charlie_key_789"
BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Multi-User API")
    print("=" * 50)
    
    # Test 1: List all users (no auth required)
    print("\n1. 📋 Testing GET /users...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users:")
            for user in users:
                print(f"   👤 {user['name']} - API Key: {user['api_key']}")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Test Alice's authentication
    print(f"\n2. 🔐 Testing Alice's authentication...")
    try:
        headers = {"X-API-Key": ALICE_API_KEY}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Authenticated as: {user_info['name']} (ID: {user_info['id']})")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Test Bob's authentication
    print(f"\n3. 🔐 Testing Bob's authentication...")
    try:
        headers = {"X-API-Key": BOB_API_KEY}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Authenticated as: {user_info['name']} (ID: {user_info['id']})")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Test invalid API key
    print(f"\n4. 🚫 Testing invalid API key...")
    try:
        headers = {"X-API-Key": "invalid_key"}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly rejected invalid API key")
        else:
            print(f"❌ Should have rejected invalid key, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Send message as Alice
    print(f"\n5. 💬 Testing message sending as Alice...")
    try:
        headers = {
            "X-API-Key": ALICE_API_KEY,
            "Content-Type": "application/json"
        }
        message_data = {"content": "Hello from test script!"}
        response = requests.post(f"{BASE_URL}/messages", json=message_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            message_response = response.json()
            print(f"✅ Message sent successfully!")
            print(f"   User: {message_response['user_message']['content']}")
            print(f"   Bot: {message_response['bot_message']['content']}")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
