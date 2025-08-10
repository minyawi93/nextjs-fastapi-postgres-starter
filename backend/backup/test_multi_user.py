#!/usr/bin/env python3
"""
Test script for multi-user API functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_multi_user_api():
    print("🧪 Testing Multi-User API with API Key Authentication")
    print("=" * 60)
    
    # Test 1: List all users
    print("\n1. 📋 Listing all users...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users:")
            for user in users:
                print(f"   👤 {user['name']} (ID: {user['id']}) - API Key: {user['api_key']}")
        else:
            print(f"❌ Failed to get users: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return
    
    # Test 2: Test each user's authentication
    print("\n2. 🔐 Testing authentication for each user...")
    for user in users:
        api_key = user['api_key']
        print(f"\n   Testing {user['name']} with API key: {api_key}")
        
        # Test getting user info
        headers = {"X-API-Key": api_key}
        try:
            response = requests.get(f"{BASE_URL}/users/me", headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                print(f"   ✅ User info: {user_info['name']} (ID: {user_info['id']})")
            else:
                print(f"   ❌ Failed to get user info: {response.status_code}")
                continue
        except Exception as e:
            print(f"   ❌ Error getting user info: {e}")
            continue
        
        # Test getting thread
        try:
            response = requests.get(f"{BASE_URL}/threads/me", headers=headers)
            if response.status_code == 200:
                thread_info = response.json()
                print(f"   ✅ Thread found with {len(thread_info['messages'])} messages")
            else:
                print(f"   ❌ Failed to get thread: {response.status_code}")
                continue
        except Exception as e:
            print(f"   ❌ Error getting thread: {e}")
            continue
        
        # Test sending a message
        try:
            message_data = {"content": f"Hello from {user['name']}!"}
            response = requests.post(
                f"{BASE_URL}/messages", 
                json=message_data, 
                headers=headers
            )
            if response.status_code == 200:
                message_response = response.json()
                print(f"   ✅ Message sent successfully!")
                print(f"      User: {message_response['user_message']['content']}")
                print(f"      Bot: {message_response['bot_message']['content']}")
            else:
                print(f"   ❌ Failed to send message: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error sending message: {e}")
    
    # Test 3: Test invalid API key
    print("\n3. 🚫 Testing invalid API key...")
    try:
        headers = {"X-API-Key": "invalid_key"}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        if response.status_code == 401:
            print("   ✅ Correctly rejected invalid API key")
        else:
            print(f"   ❌ Should have rejected invalid key, got: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing invalid key: {e}")
    
    # Test 4: Test missing API key
    print("\n4. 🚫 Testing missing API key...")
    try:
        response = requests.get(f"{BASE_URL}/users/me")
        if response.status_code == 422:  # Validation error for missing header
            print("   ✅ Correctly rejected missing API key")
        else:
            print(f"   ❌ Should have rejected missing key, got: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing missing key: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Multi-user API testing complete!")

if __name__ == "__main__":
    test_multi_user_api()
