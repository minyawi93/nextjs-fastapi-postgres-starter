"""
Pytest configuration and fixtures for API testing
"""

import pytest
import requests
from typing import Dict, List

# Test configuration
BASE_URL = "http://localhost:8000"

# Test API keys
TEST_API_KEYS = {
    "alice": "alice_key_123",
    "bob": "bob_key_456", 
    "charlie": "charlie_key_789"
}

@pytest.fixture
def base_url() -> str:
    """Base URL for the API"""
    return BASE_URL

@pytest.fixture
def api_keys() -> Dict[str, str]:
    """Test API keys"""
    return TEST_API_KEYS

@pytest.fixture
def alice_headers(api_keys: Dict[str, str]) -> Dict[str, str]:
    """Headers for Alice's API key"""
    return {"X-API-Key": api_keys["alice"]}

@pytest.fixture
def bob_headers(api_keys: Dict[str, str]) -> Dict[str, str]:
    """Headers for Bob's API key"""
    return {"X-API-Key": api_keys["bob"]}

@pytest.fixture
def charlie_headers(api_keys: Dict[str, str]) -> Dict[str, str]:
    """Headers for Charlie's API key"""
    return {"X-API-Key": api_keys["charlie"]}

@pytest.fixture
def invalid_headers() -> Dict[str, str]:
    """Headers with invalid API key"""
    return {"X-API-Key": "invalid_key"}

@pytest.fixture
def json_headers() -> Dict[str, str]:
    """Headers for JSON requests"""
    return {"Content-Type": "application/json"}

def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
    config.addinivalue_line(
        "markers", "auth: marks tests as authentication tests"
    )
